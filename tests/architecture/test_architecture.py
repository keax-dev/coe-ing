# Tema: verificación automática de fronteras, dependencias y ausencia de ciclos.

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "src"


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
        for path in (ROOT / layer).rglob("*.py"):
            for module in imports(path):
                assert not module.startswith(
                    ("fastapi", "pydantic", "sqlalchemy", "src.infrastructure")
                ), path
                if layer == "domain":
                    assert not module.startswith("src.application"), path


def test_ports_only_use_domain_models_and_standard_types() -> None:
    for path in (ROOT / "application" / "port").rglob("*.py"):
        assert all(module.startswith(("typing", "src.domain")) for module in imports(path)), path


def test_adapters_do_not_depend_on_each_other() -> None:
    for direction, opposite in [("input", "output"), ("output", "input")]:
        for path in (ROOT / "infrastructure" / direction).rglob("*.py"):
            for module in imports(path):
                assert not module.startswith(f"src.infrastructure.{opposite}"), path
                if module.startswith("src.application"):
                    assert module.startswith(f"src.application.port.{direction}"), path


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
    for layer in ["domain", "application", "infrastructure"]:
        for path in (tests_root / layer).rglob("test_*.py"):
            relative = path.relative_to(tests_root)
            source_file = ROOT / relative.parent / path.name.removeprefix("test_")
            assert source_file.is_file(), f"Test has no matching source component: {path}"
