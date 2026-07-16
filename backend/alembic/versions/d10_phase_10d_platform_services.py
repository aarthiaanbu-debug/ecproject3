"""Phase 10D platform services.

Revision ID: d10_phase_10d
Revises: c10_phase_10c
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "d10_phase_10d"
down_revision: Union[str, Sequence[str], None] = "c10_phase_10c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "workflow_definitions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tenant_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=180), nullable=False),
        sa.Column("workflow_type", sa.String(length=40), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_workflow_definitions_id"), "workflow_definitions", ["id"], unique=False)
    op.create_index(op.f("ix_workflow_definitions_tenant_id"), "workflow_definitions", ["tenant_id"], unique=False)
    op.create_index(op.f("ix_workflow_definitions_name"), "workflow_definitions", ["name"], unique=False)
    op.create_index(op.f("ix_workflow_definitions_workflow_type"), "workflow_definitions", ["workflow_type"], unique=False)
    op.create_index(op.f("ix_workflow_definitions_is_active"), "workflow_definitions", ["is_active"], unique=False)

    op.create_table(
        "workflow_rules",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("workflow_id", sa.Integer(), nullable=False),
        sa.Column("trigger_event", sa.String(length=100), nullable=False),
        sa.Column("condition_type", sa.String(length=80), nullable=False),
        sa.Column("condition_value", sa.String(length=255), nullable=False),
        sa.Column("action_type", sa.String(length=80), nullable=False),
        sa.Column("action_value", sa.Text(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["workflow_id"], ["workflow_definitions.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_workflow_rules_id"), "workflow_rules", ["id"], unique=False)
    op.create_index(op.f("ix_workflow_rules_workflow_id"), "workflow_rules", ["workflow_id"], unique=False)
    op.create_index(op.f("ix_workflow_rules_trigger_event"), "workflow_rules", ["trigger_event"], unique=False)

    op.create_table(
        "workflow_executions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("workflow_id", sa.Integer(), nullable=False),
        sa.Column("entity_type", sa.String(length=40), nullable=False),
        sa.Column("entity_id", sa.Integer(), nullable=False),
        sa.Column("execution_status", sa.String(length=40), nullable=False),
        sa.Column("details", sa.Text(), nullable=True),
        sa.Column("executed_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["workflow_id"], ["workflow_definitions.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_workflow_executions_id"), "workflow_executions", ["id"], unique=False)
    op.create_index(op.f("ix_workflow_executions_workflow_id"), "workflow_executions", ["workflow_id"], unique=False)
    op.create_index(op.f("ix_workflow_executions_entity_type"), "workflow_executions", ["entity_type"], unique=False)
    op.create_index(op.f("ix_workflow_executions_entity_id"), "workflow_executions", ["entity_id"], unique=False)
    op.create_index(op.f("ix_workflow_executions_execution_status"), "workflow_executions", ["execution_status"], unique=False)
    op.create_index(op.f("ix_workflow_executions_executed_at"), "workflow_executions", ["executed_at"], unique=False)

    op.create_table(
        "notification_rules",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tenant_id", sa.Integer(), nullable=False),
        sa.Column("event_type", sa.String(length=120), nullable=False),
        sa.Column("notification_type", sa.String(length=40), nullable=False),
        sa.Column("recipient_role", sa.String(length=80), nullable=True),
        sa.Column("message_template", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_notification_rules_id"), "notification_rules", ["id"], unique=False)
    op.create_index(op.f("ix_notification_rules_tenant_id"), "notification_rules", ["tenant_id"], unique=False)
    op.create_index(op.f("ix_notification_rules_event_type"), "notification_rules", ["event_type"], unique=False)
    op.create_index(op.f("ix_notification_rules_is_active"), "notification_rules", ["is_active"], unique=False)

    op.create_table(
        "saved_searches",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tenant_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=180), nullable=False),
        sa.Column("query_json", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_saved_searches_id"), "saved_searches", ["id"], unique=False)
    op.create_index(op.f("ix_saved_searches_tenant_id"), "saved_searches", ["tenant_id"], unique=False)
    op.create_index(op.f("ix_saved_searches_user_id"), "saved_searches", ["user_id"], unique=False)

    op.create_table(
        "knowledge_categories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tenant_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=180), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_knowledge_categories_id"), "knowledge_categories", ["id"], unique=False)
    op.create_index(op.f("ix_knowledge_categories_tenant_id"), "knowledge_categories", ["tenant_id"], unique=False)
    op.create_index(op.f("ix_knowledge_categories_name"), "knowledge_categories", ["name"], unique=False)

    op.create_table(
        "knowledge_articles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tenant_id", sa.Integer(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=True),
        sa.Column("title", sa.String(length=220), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("tags", sa.String(length=500), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("created_by", sa.Integer(), nullable=False),
        sa.Column("is_archived", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["category_id"], ["knowledge_categories.id"]),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_knowledge_articles_id"), "knowledge_articles", ["id"], unique=False)
    op.create_index(op.f("ix_knowledge_articles_tenant_id"), "knowledge_articles", ["tenant_id"], unique=False)
    op.create_index(op.f("ix_knowledge_articles_category_id"), "knowledge_articles", ["category_id"], unique=False)
    op.create_index(op.f("ix_knowledge_articles_title"), "knowledge_articles", ["title"], unique=False)
    op.create_index(op.f("ix_knowledge_articles_tags"), "knowledge_articles", ["tags"], unique=False)
    op.create_index(op.f("ix_knowledge_articles_is_archived"), "knowledge_articles", ["is_archived"], unique=False)

    op.create_table(
        "custom_forms",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tenant_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=180), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("request_type", sa.String(length=40), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_custom_forms_id"), "custom_forms", ["id"], unique=False)
    op.create_index(op.f("ix_custom_forms_tenant_id"), "custom_forms", ["tenant_id"], unique=False)
    op.create_index(op.f("ix_custom_forms_name"), "custom_forms", ["name"], unique=False)
    op.create_index(op.f("ix_custom_forms_request_type"), "custom_forms", ["request_type"], unique=False)
    op.create_index(op.f("ix_custom_forms_is_active"), "custom_forms", ["is_active"], unique=False)

    op.create_table(
        "custom_form_fields",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("form_id", sa.Integer(), nullable=False),
        sa.Column("field_name", sa.String(length=160), nullable=False),
        sa.Column("field_type", sa.String(length=40), nullable=False),
        sa.Column("validation_rules", sa.JSON(), nullable=True),
        sa.Column("is_required", sa.Boolean(), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["form_id"], ["custom_forms.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_custom_form_fields_id"), "custom_form_fields", ["id"], unique=False)
    op.create_index(op.f("ix_custom_form_fields_form_id"), "custom_form_fields", ["form_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_custom_form_fields_form_id"), table_name="custom_form_fields")
    op.drop_index(op.f("ix_custom_form_fields_id"), table_name="custom_form_fields")
    op.drop_table("custom_form_fields")
    op.drop_index(op.f("ix_custom_forms_is_active"), table_name="custom_forms")
    op.drop_index(op.f("ix_custom_forms_request_type"), table_name="custom_forms")
    op.drop_index(op.f("ix_custom_forms_name"), table_name="custom_forms")
    op.drop_index(op.f("ix_custom_forms_tenant_id"), table_name="custom_forms")
    op.drop_index(op.f("ix_custom_forms_id"), table_name="custom_forms")
    op.drop_table("custom_forms")
    op.drop_index(op.f("ix_knowledge_articles_is_archived"), table_name="knowledge_articles")
    op.drop_index(op.f("ix_knowledge_articles_tags"), table_name="knowledge_articles")
    op.drop_index(op.f("ix_knowledge_articles_title"), table_name="knowledge_articles")
    op.drop_index(op.f("ix_knowledge_articles_category_id"), table_name="knowledge_articles")
    op.drop_index(op.f("ix_knowledge_articles_tenant_id"), table_name="knowledge_articles")
    op.drop_index(op.f("ix_knowledge_articles_id"), table_name="knowledge_articles")
    op.drop_table("knowledge_articles")
    op.drop_index(op.f("ix_knowledge_categories_name"), table_name="knowledge_categories")
    op.drop_index(op.f("ix_knowledge_categories_tenant_id"), table_name="knowledge_categories")
    op.drop_index(op.f("ix_knowledge_categories_id"), table_name="knowledge_categories")
    op.drop_table("knowledge_categories")
    op.drop_index(op.f("ix_saved_searches_user_id"), table_name="saved_searches")
    op.drop_index(op.f("ix_saved_searches_tenant_id"), table_name="saved_searches")
    op.drop_index(op.f("ix_saved_searches_id"), table_name="saved_searches")
    op.drop_table("saved_searches")
    op.drop_index(op.f("ix_notification_rules_is_active"), table_name="notification_rules")
    op.drop_index(op.f("ix_notification_rules_event_type"), table_name="notification_rules")
    op.drop_index(op.f("ix_notification_rules_tenant_id"), table_name="notification_rules")
    op.drop_index(op.f("ix_notification_rules_id"), table_name="notification_rules")
    op.drop_table("notification_rules")
    op.drop_index(op.f("ix_workflow_executions_executed_at"), table_name="workflow_executions")
    op.drop_index(op.f("ix_workflow_executions_execution_status"), table_name="workflow_executions")
    op.drop_index(op.f("ix_workflow_executions_entity_id"), table_name="workflow_executions")
    op.drop_index(op.f("ix_workflow_executions_entity_type"), table_name="workflow_executions")
    op.drop_index(op.f("ix_workflow_executions_workflow_id"), table_name="workflow_executions")
    op.drop_index(op.f("ix_workflow_executions_id"), table_name="workflow_executions")
    op.drop_table("workflow_executions")
    op.drop_index(op.f("ix_workflow_rules_trigger_event"), table_name="workflow_rules")
    op.drop_index(op.f("ix_workflow_rules_workflow_id"), table_name="workflow_rules")
    op.drop_index(op.f("ix_workflow_rules_id"), table_name="workflow_rules")
    op.drop_table("workflow_rules")
    op.drop_index(op.f("ix_workflow_definitions_is_active"), table_name="workflow_definitions")
    op.drop_index(op.f("ix_workflow_definitions_workflow_type"), table_name="workflow_definitions")
    op.drop_index(op.f("ix_workflow_definitions_name"), table_name="workflow_definitions")
    op.drop_index(op.f("ix_workflow_definitions_tenant_id"), table_name="workflow_definitions")
    op.drop_index(op.f("ix_workflow_definitions_id"), table_name="workflow_definitions")
    op.drop_table("workflow_definitions")
