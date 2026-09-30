"""
Tests for Alembic migrations and database seeder generation.
"""

import py_compile
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

from generators.project_packaging_generator import ProjectPackagingGenerator
from utils.database_manager import apply_migrations, seed_database


def test_generate_alembic_setup():
    with tempfile.TemporaryDirectory() as tmpdir:
        gen = ProjectPackagingGenerator(output_dir=tmpdir)

        # Mock blueprint with 2 entities
        mock_field1 = MagicMock(name="title", type="string")
        mock_field1.name = "title"
        mock_field1.type = "string"

        mock_field2 = MagicMock(name="price", type="float")
        mock_field2.name = "price"
        mock_field2.type = "float"

        mock_entity = MagicMock(name="Product")
        mock_entity.name = "Product"
        mock_entity.fields = [mock_field1, mock_field2]

        mock_bp = MagicMock()
        mock_bp.entities = [mock_entity]

        gen.generate_alembic_setup(project_name="Store API", blueprint=mock_bp)

        backend_dir = Path(tmpdir) / "backend"
        assert (backend_dir / "alembic.ini").exists()
        assert (backend_dir / "alembic" / "env.py").exists()
        assert (backend_dir / "alembic" / "script.py.mako").exists()

        initial_mig = backend_dir / "alembic" / "versions" / "001_initial_schema.py"
        assert initial_mig.exists()

        # Check Python compilation syntax
        py_compile.compile(str(initial_mig), doraise=True)
        py_compile.compile(str(backend_dir / "alembic" / "env.py"), doraise=True)

        mig_content = initial_mig.read_text(encoding="utf-8")
        assert "op.create_table(" in mig_content
        assert "'products'" in mig_content
        assert "sa.Column('title', sa.String()" in mig_content
        assert "sa.Column('price', sa.Float()" in mig_content
        assert "op.drop_table('products')" in mig_content


def test_generate_database_seeder():
    with tempfile.TemporaryDirectory() as tmpdir:
        gen = ProjectPackagingGenerator(output_dir=tmpdir)

        mock_field1 = MagicMock()
        mock_field1.name = "name"
        mock_field1.type = "string"

        mock_entity = MagicMock()
        mock_entity.name = "Customer"
        mock_entity.fields = [mock_field1]

        mock_bp = MagicMock()
        mock_bp.entities = [mock_entity]

        gen.generate_database_seeder(project_name="CRM Service", blueprint=mock_bp)

        seed_file = Path(tmpdir) / "backend" / "seed.py"
        assert seed_file.exists()

        # Check Python compilation syntax
        py_compile.compile(str(seed_file), doraise=True)

        seed_content = seed_file.read_text(encoding="utf-8")
        assert "def seed():" in seed_content
        assert "models.Customer" in seed_content
        assert "Customer #1" in seed_content


def test_database_manager_missing_files():
    with tempfile.TemporaryDirectory() as tmpdir:
        empty_dir = Path(tmpdir)
        mig_res = apply_migrations(empty_dir)
        assert mig_res["success"] is False
        assert "alembic.ini not found" in mig_res["stderr"]

        seed_res = seed_database(empty_dir)
        assert seed_res["success"] is False
        assert "seed.py not found" in seed_res["stderr"]
