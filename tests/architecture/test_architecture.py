# Tema: verificación automática de fronteras, dependencias y ausencia de ciclos.

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "src"
FEATURE_ROOT = ROOT / "institution" / "hexagonal"


def imports(path: Path) -> list[str]:
    modules = []
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.Import):
            modules.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            assert node.level == 0, f"Use explicit imports: {path}"
            modules.append(node.module or "")
    return modules


def test_domain_and_application_do_not_depend_on_frameworks() -> None:
    for layer in ["domain", "application"]:
        assert (FEATURE_ROOT / layer).is_dir()
        for path in (FEATURE_ROOT / layer).rglob("*.py"):
            for module in imports(path):
                assert not module.startswith(
                    (
                        "fastapi",
                        "pydantic",
                        "sqlalchemy",
                        "src.institution.hexagonal.infrastructure",
                    )
                ), path
                if layer == "domain":
                    assert not module.startswith("src.institution.hexagonal.application"), path


def test_ports_only_use_domain_models_and_standard_types() -> None:
    for path in (FEATURE_ROOT / "application" / "port").rglob("*.py"):
        assert all(
            module.startswith(("typing", "src.institution.hexagonal.domain"))
            for module in imports(path)
        ), path


def test_adapters_do_not_depend_on_each_other() -> None:
    for direction, opposite in [("input", "output"), ("output", "input")]:
        for path in (FEATURE_ROOT / "infrastructure" / direction).rglob("*.py"):
            for module in imports(path):
                assert not module.startswith(
                    f"src.institution.hexagonal.infrastructure.{opposite}"
                ), path
                if module.startswith("src.institution.hexagonal.application"):
                    assert module.startswith(
                        f"src.institution.hexagonal.application.port.{direction}"
                    ), path


def test_no_import_cycles() -> None:
    modules = {
        ".".join(path.relative_to(ROOT.parent).with_suffix("").parts): path
        for path in ROOT.rglob("*.py")
    }
    graph = {
        module: [dependency for dependency in imports(path) if dependency in modules]
        for module, path in modules.items()
    }
    visited: set[str] = set()
    visiting: set[str] = set()

    def visit(module: str) -> None:
        assert module not in visiting, f"Import cycle at {module}"
        if module in visited:
            return
        visiting.add(module)
        for dependency in graph[module]:
            visit(dependency)
        visiting.remove(module)
        visited.add(module)

    for module in graph:
        visit(module)


def test_component_tests_follow_source_structure() -> None:
    tests_root = Path(__file__).resolve().parents[1]
    for feature in ["institution/hexagonal", "education/clean", "shared"]:
        feature_tests = tests_root / feature
        assert feature_tests.is_dir()
        for path in feature_tests.rglob("test_*.py"):
            relative = path.relative_to(tests_root)
            source_file = ROOT / relative.parent / path.name.removeprefix("test_")
            assert source_file.is_file(), f"Test has no matching source component: {path}"


def test_clean_dependency_rule() -> None:
    clean_root = ROOT / "education" / "clean"
    allowed = {
        "domain": ("src.education.clean.domain",),
        "application": ("src.education.clean.domain", "src.education.clean.application"),
    }
    for layer, prefixes in allowed.items():
        assert (clean_root / layer).is_dir()
        for path in (clean_root / layer).rglob("*.py"):
            for module in imports(path):
                assert not module.startswith(("fastapi", "pydantic", "sqlalchemy")), path
                if module.startswith("src."):
                    assert module.startswith(prefixes), path


def test_clean_has_only_planned_layers() -> None:
    clean_root = ROOT / "education" / "clean"
    directories = {
        path.name for path in clean_root.iterdir() if path.is_dir() and path.name != "__pycache__"
    }
    assert directories == {"domain", "application", "infrastructure", "presentation"}


def test_clean_repositories_do_not_confirm_transactions() -> None:
    directory = ROOT / "education/clean/infrastructure/repository"
    for path in directory.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                assert node.func.attr not in {"commit", "rollback", "begin"}, path


def test_presentation_only_wires_infrastructure_in_dependencies() -> None:
    presentation = ROOT / "education/clean/presentation"
    for path in presentation.rglob("*.py"):
        if path.parent.name == "dependency":
            continue
        for module in imports(path):
            assert not module.startswith(("src.education.clean.infrastructure", "sqlalchemy")), path


def test_clean_does_not_import_hexagonal_implementation() -> None:
    for path in (ROOT / "education" / "clean").rglob("*.py"):
        assert not any(module.startswith("src.institution") for module in imports(path)), path
