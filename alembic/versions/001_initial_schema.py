"""Initial database schema migration

Revision ID: 001_initial_schema
Revises:
Create Date: 2026-10-07 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Users table
    op.create_table(
        'users',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('password_salt', sa.String(length=64), nullable=True),
        sa.Column('full_name', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # Birth Profiles table
    op.create_table(
        'birth_profiles',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('month', sa.Integer(), nullable=False),
        sa.Column('day', sa.Integer(), nullable=False),
        sa.Column('hour', sa.Integer(), nullable=False),
        sa.Column('minute', sa.Integer(), nullable=False),
        sa.Column('second', sa.Integer(), nullable=False),
        sa.Column('timezone_str', sa.String(length=100), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('place_name', sa.String(length=255), nullable=False),
        sa.Column('country', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_birth_profiles_user_id'), 'birth_profiles', ['user_id'], unique=False)
    op.create_index('ix_birth_profiles_user_id_id', 'birth_profiles', ['user_id', 'id'], unique=False)

    # Calculation Reports table
    op.create_table(
        'calculation_reports',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=False),
        sa.Column('birth_profile_id', sa.String(length=36), nullable=False),
        sa.Column('chart_hash', sa.String(length=64), nullable=False),
        sa.Column('master_evidence_json', sa.Text(), nullable=False),
        sa.Column('predictions_json', sa.Text(), nullable=False),
        sa.Column('svg_chart', sa.Text(), nullable=True),
        sa.Column('report_json', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['birth_profile_id'], ['birth_profiles.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_calculation_reports_birth_profile_id'), 'calculation_reports', ['birth_profile_id'], unique=False)
    op.create_index(op.f('ix_calculation_reports_chart_hash'), 'calculation_reports', ['chart_hash'], unique=False)
    op.create_index(op.f('ix_calculation_reports_user_id'), 'calculation_reports', ['user_id'], unique=False)
    op.create_index('ix_reports_user_id_id', 'calculation_reports', ['user_id', 'id'], unique=False)

    # AI Interpretations table
    op.create_table(
        'ai_interpretations',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=False),
        sa.Column('calculation_report_id', sa.String(length=36), nullable=False),
        sa.Column('domain', sa.String(length=50), nullable=False),
        sa.Column('prompt', sa.Text(), nullable=False),
        sa.Column('interpretation_text', sa.Text(), nullable=False),
        sa.Column('validation_status', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['calculation_report_id'], ['calculation_reports.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ai_interpretations_calculation_report_id'), 'ai_interpretations', ['calculation_report_id'], unique=False)
    op.create_index(op.f('ix_ai_interpretations_domain'), 'ai_interpretations', ['domain'], unique=False)
    op.create_index(op.f('ix_ai_interpretations_user_id'), 'ai_interpretations', ['user_id'], unique=False)

    # Saved Charts table
    op.create_table(
        'saved_charts',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=False),
        sa.Column('birth_profile_id', sa.String(length=36), nullable=False),
        sa.Column('chart_title', sa.String(length=255), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['birth_profile_id'], ['birth_profiles.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_saved_charts_birth_profile_id'), 'saved_charts', ['birth_profile_id'], unique=False)
    op.create_index(op.f('ix_saved_charts_user_id'), 'saved_charts', ['user_id'], unique=False)

    # Audit Records table
    op.create_table(
        'audit_records',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=False),
        sa.Column('action', sa.String(length=100), nullable=False),
        sa.Column('endpoint', sa.String(length=255), nullable=False),
        sa.Column('ip_address', sa.String(length=50), nullable=True),
        sa.Column('details_json', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_audit_records_action'), 'audit_records', ['action'], unique=False)
    op.create_index(op.f('ix_audit_records_user_id'), 'audit_records', ['user_id'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_audit_records_user_id'), table_name='audit_records')
    op.drop_index(op.f('ix_audit_records_action'), table_name='audit_records')
    op.drop_table('audit_records')

    op.drop_index(op.f('ix_saved_charts_user_id'), table_name='saved_charts')
    op.drop_index(op.f('ix_saved_charts_birth_profile_id'), table_name='saved_charts')
    op.drop_table('saved_charts')

    op.drop_index(op.f('ix_ai_interpretations_user_id'), table_name='ai_interpretations')
    op.drop_index(op.f('ix_ai_interpretations_domain'), table_name='ai_interpretations')
    op.drop_index(op.f('ix_ai_interpretations_calculation_report_id'), table_name='ai_interpretations')
    op.drop_table('ai_interpretations')

    op.drop_index('ix_reports_user_id_id', table_name='calculation_reports')
    op.drop_index(op.f('ix_calculation_reports_user_id'), table_name='calculation_reports')
    op.drop_index(op.f('ix_calculation_reports_chart_hash'), table_name='calculation_reports')
    op.drop_index(op.f('ix_calculation_reports_birth_profile_id'), table_name='calculation_reports')
    op.drop_table('calculation_reports')

    op.drop_index('ix_birth_profiles_user_id_id', table_name='birth_profiles')
    op.drop_index(op.f('ix_birth_profiles_user_id'), table_name='birth_profiles')
    op.drop_table('birth_profiles')

    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
