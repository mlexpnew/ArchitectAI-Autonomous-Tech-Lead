"""
Test Generator

Generates basic pytest smoke tests for dynamically
generated FastAPI CRUD endpoints.
"""

from pathlib import Path

from generators.writer import FileWriter


class TestGenerator:

    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)

    def generate(self, entities):

        tests_dir = (
            self.output_dir
            / "backend"
            / "tests"
        )

        tests_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        # ---------------------------------------------
        # conftest.py
        # ---------------------------------------------

        conftest = '''"""
Pytest configuration for generated backend.
"""

import pytest

from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():

    with TestClient(app) as test_client:
        yield test_client
'''

        FileWriter.write(
            tests_dir / "conftest.py",
            conftest,
        )

        # ---------------------------------------------
        # Generate one test file per entity
        # ---------------------------------------------

        for entity in entities:

            self.generate_entity_test(
                entity,
                tests_dir,
            )

        print("✅ Generated Backend Tests")

    def generate_entity_test(
        self,
        entity,
        tests_dir: Path,
    ):

        name = entity.name
        lower = name.lower()
        endpoint = f"/{lower}s/"

        code = f'''"""
{name} API Smoke Tests
"""


def test_{lower}_get_all(client):

    response = client.get(
        "{endpoint}"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_{lower}_not_found(client):

    response = client.get(
        "{endpoint}999999"
    )

    assert response.status_code == 404
'''

        FileWriter.write(
            tests_dir
            / f"test_{lower}.py",
            code,
        )

        print(
            f"✅ Generated {name} Tests"
        )