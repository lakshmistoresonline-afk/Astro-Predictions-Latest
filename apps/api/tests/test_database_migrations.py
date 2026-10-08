"""
Test Suite for Alembic Database Migration Script Execution & Rollback.
"""
import os
import pytest
from alembic.config import Config
from alembic import command

def test_alembic_upgrade_and_downgrade(tmp_path):
    """Verifies that Alembic upgrade head and downgrade base execute cleanly on an empty database."""
    test_db_file = str(tmp_path / "test_migration.db")
    test_db_url = f"sqlite:///{test_db_file}"

    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", test_db_url)

    # Upgrade to head on empty database
    command.upgrade(alembic_cfg, "head")

    # Downgrade to base
    command.downgrade(alembic_cfg, "base")

    # Upgrade back to head
    command.upgrade(alembic_cfg, "head")
