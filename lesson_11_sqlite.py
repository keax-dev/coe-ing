# Tema: SQL parametrizado, operaciones CRUD y transacciones SQLite.

import sqlite3
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory


def main() -> None:
    with TemporaryDirectory() as directory:
        database = Path(directory) / "students.db"
        # closing cierra la conexión; el contexto propio de sqlite confirma o revierte escrituras.
        with closing(sqlite3.connect(database)) as connection:
            with connection:
                connection.execute(
                    "CREATE TABLE students (name TEXT PRIMARY KEY, "
                    "score INTEGER NOT NULL CHECK (score BETWEEN 0 AND 100))"
                )
                # Los valores se pasan separados del SQL, sin concatenar texto del usuario.
                connection.executemany(
                    "INSERT INTO students VALUES (?, ?)", [("Alex", 85), ("Sam", 92)]
                )
            print(
                "Created records:",
                connection.execute("SELECT * FROM students ORDER BY name").fetchall(),
            )
            with connection:
                connection.execute(
                    "UPDATE students SET score = ? WHERE name = ?", (90, "Alex")
                )
            print(
                "Updated score:",
                connection.execute(
                    "SELECT score FROM students WHERE name = ?", ("Alex",)
                ).fetchone(),
            )

            try:
                with connection:
                    # El segundo nombre ya existe: tampoco debe guardarse el primer registro del lote.
                    connection.executemany(
                        "INSERT INTO students VALUES (?, ?)",
                        [("Robin", 80), ("Alex", 95)],
                    )
            except sqlite3.IntegrityError:
                print("Batch rejected; all changes in the batch were rolled back.")
            print(
                "Count after rollback:",
                connection.execute("SELECT COUNT(*) FROM students").fetchone()[0],
            )

            with connection:
                cursor = connection.execute(
                    "DELETE FROM students WHERE name = ?", ("Sam",)
                )
                print("Deleted rows:", cursor.rowcount)
            print(
                "Final records:",
                connection.execute("SELECT * FROM students").fetchall(),
            )
    print("Temporary database removed:", not database.exists())


if __name__ == "__main__":
    main()
