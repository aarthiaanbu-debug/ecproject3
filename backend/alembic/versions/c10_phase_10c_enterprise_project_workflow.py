"""Phase 10C enterprise project workflow.

Revision ID: c10_phase_10c
Revises: b10_phase_10b
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c10_phase_10c"
down_revision: Union[str, Sequence[str], None] = "b10_phase_10b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "teams",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tenant_id", sa.Integer(), nullable=False),
        sa.Column("workspace_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("lead_user_id", sa.Integer(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"]),
        sa.ForeignKeyConstraint(["lead_user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["workspace_id"], ["workspaces.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("workspace_id", "name", name="uq_team_workspace_name"),
    )
    op.create_index(op.f("ix_teams_id"), "teams", ["id"], unique=False)
    op.create_index(op.f("ix_teams_tenant_id"), "teams", ["tenant_id"], unique=False)
    op.create_index(op.f("ix_teams_workspace_id"), "teams", ["workspace_id"], unique=False)

    op.create_table(
        "projects",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tenant_id", sa.Integer(), nullable=False),
        sa.Column("workspace_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=180), nullable=False),
        sa.Column("slug", sa.String(length=180), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("owner_user_id", sa.Integer(), nullable=True),
        sa.Column("start_date", sa.DateTime(), nullable=True),
        sa.Column("end_date", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"]),
        sa.ForeignKeyConstraint(["owner_user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["workspace_id"], ["workspaces.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("workspace_id", "slug", name="uq_project_workspace_slug"),
    )
    op.create_index(op.f("ix_projects_id"), "projects", ["id"], unique=False)
    op.create_index(op.f("ix_projects_tenant_id"), "projects", ["tenant_id"], unique=False)
    op.create_index(op.f("ix_projects_workspace_id"), "projects", ["workspace_id"], unique=False)

    op.create_table(
        "team_members",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tenant_id", sa.Integer(), nullable=False),
        sa.Column("workspace_id", sa.Integer(), nullable=False),
        sa.Column("team_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("role", sa.String(length=80), nullable=False),
        sa.Column("allocation_percent", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("joined_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["team_id"], ["teams.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["workspace_id"], ["workspaces.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("team_id", "user_id", name="uq_team_member"),
    )
    op.create_index(op.f("ix_team_members_id"), "team_members", ["id"], unique=False)
    op.create_index(op.f("ix_team_members_team_id"), "team_members", ["team_id"], unique=False)
    op.create_index(op.f("ix_team_members_tenant_id"), "team_members", ["tenant_id"], unique=False)
    op.create_index(op.f("ix_team_members_workspace_id"), "team_members", ["workspace_id"], unique=False)

    op.create_table(
        "project_teams",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tenant_id", sa.Integer(), nullable=False),
        sa.Column("workspace_id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("team_id", sa.Integer(), nullable=False),
        sa.Column("role", sa.String(length=80), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.ForeignKeyConstraint(["team_id"], ["teams.id"]),
        sa.ForeignKeyConstraint(["workspace_id"], ["workspaces.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("project_id", "team_id", name="uq_project_team"),
    )
    op.create_index(op.f("ix_project_teams_id"), "project_teams", ["id"], unique=False)
    op.create_index(op.f("ix_project_teams_project_id"), "project_teams", ["project_id"], unique=False)
    op.create_index(op.f("ix_project_teams_team_id"), "project_teams", ["team_id"], unique=False)
    op.create_index(op.f("ix_project_teams_tenant_id"), "project_teams", ["tenant_id"], unique=False)
    op.create_index(op.f("ix_project_teams_workspace_id"), "project_teams", ["workspace_id"], unique=False)

    op.create_table(
        "project_documents",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tenant_id", sa.Integer(), nullable=False),
        sa.Column("workspace_id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("file_name", sa.String(length=255), nullable=False),
        sa.Column("file_path", sa.String(length=500), nullable=True),
        sa.Column("document_type", sa.String(length=80), nullable=False),
        sa.Column("uploaded_by", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.ForeignKeyConstraint(["uploaded_by"], ["users.id"]),
        sa.ForeignKeyConstraint(["workspace_id"], ["workspaces.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_project_documents_id"), "project_documents", ["id"], unique=False)
    op.create_index(op.f("ix_project_documents_project_id"), "project_documents", ["project_id"], unique=False)
    op.create_index(op.f("ix_project_documents_tenant_id"), "project_documents", ["tenant_id"], unique=False)
    op.create_index(op.f("ix_project_documents_workspace_id"), "project_documents", ["workspace_id"], unique=False)

    op.create_table(
        "meetings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tenant_id", sa.Integer(), nullable=False),
        sa.Column("workspace_id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=True),
        sa.Column("team_id", sa.Integer(), nullable=True),
        sa.Column("title", sa.String(length=180), nullable=False),
        sa.Column("agenda", sa.Text(), nullable=True),
        sa.Column("meeting_type", sa.String(length=80), nullable=False),
        sa.Column("location", sa.String(length=255), nullable=True),
        sa.Column("starts_at", sa.DateTime(), nullable=False),
        sa.Column("ends_at", sa.DateTime(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("created_by", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"]),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.ForeignKeyConstraint(["team_id"], ["teams.id"]),
        sa.ForeignKeyConstraint(["workspace_id"], ["workspaces.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_meetings_id"), "meetings", ["id"], unique=False)
    op.create_index(op.f("ix_meetings_project_id"), "meetings", ["project_id"], unique=False)
    op.create_index(op.f("ix_meetings_team_id"), "meetings", ["team_id"], unique=False)
    op.create_index(op.f("ix_meetings_tenant_id"), "meetings", ["tenant_id"], unique=False)
    op.create_index(op.f("ix_meetings_workspace_id"), "meetings", ["workspace_id"], unique=False)

    op.create_table(
        "meeting_attendees",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tenant_id", sa.Integer(), nullable=False),
        sa.Column("meeting_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("response_status", sa.String(length=50), nullable=False),
        sa.Column("is_required", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["meeting_id"], ["meetings.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("meeting_id", "user_id", name="uq_meeting_attendee"),
    )
    op.create_index(op.f("ix_meeting_attendees_id"), "meeting_attendees", ["id"], unique=False)
    op.create_index(op.f("ix_meeting_attendees_meeting_id"), "meeting_attendees", ["meeting_id"], unique=False)
    op.create_index(op.f("ix_meeting_attendees_tenant_id"), "meeting_attendees", ["tenant_id"], unique=False)

    op.create_table(
        "meeting_notes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tenant_id", sa.Integer(), nullable=False),
        sa.Column("meeting_id", sa.Integer(), nullable=False),
        sa.Column("author_id", sa.Integer(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("decisions", sa.Text(), nullable=True),
        sa.Column("action_items", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["author_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["meeting_id"], ["meetings.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_meeting_notes_id"), "meeting_notes", ["id"], unique=False)
    op.create_index(op.f("ix_meeting_notes_meeting_id"), "meeting_notes", ["meeting_id"], unique=False)
    op.create_index(op.f("ix_meeting_notes_tenant_id"), "meeting_notes", ["tenant_id"], unique=False)

    op.create_table(
        "ai_meeting_summaries",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tenant_id", sa.Integer(), nullable=False),
        sa.Column("meeting_id", sa.Integer(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("key_decisions", sa.Text(), nullable=True),
        sa.Column("action_items", sa.Text(), nullable=True),
        sa.Column("generated_by", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["generated_by"], ["users.id"]),
        sa.ForeignKeyConstraint(["meeting_id"], ["meetings.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("meeting_id", name="uq_ai_summary_meeting"),
    )
    op.create_index(op.f("ix_ai_meeting_summaries_id"), "ai_meeting_summaries", ["id"], unique=False)
    op.create_index(op.f("ix_ai_meeting_summaries_meeting_id"), "ai_meeting_summaries", ["meeting_id"], unique=False)
    op.create_index(op.f("ix_ai_meeting_summaries_tenant_id"), "ai_meeting_summaries", ["tenant_id"], unique=False)

    with op.batch_alter_table("channels") as batch:
        batch.add_column(sa.Column("project_id", sa.Integer(), nullable=True))
        batch.create_foreign_key("fk_channels_project", "projects", ["project_id"], ["id"])

    with op.batch_alter_table("tasks") as batch:
        batch.add_column(sa.Column("project_id", sa.Integer(), nullable=True))
        batch.add_column(sa.Column("team_id", sa.Integer(), nullable=True))
        batch.create_foreign_key("fk_tasks_project", "projects", ["project_id"], ["id"])
        batch.create_foreign_key("fk_tasks_team", "teams", ["team_id"], ["id"])


def downgrade() -> None:
    with op.batch_alter_table("tasks") as batch:
        batch.drop_constraint("fk_tasks_team", type_="foreignkey")
        batch.drop_constraint("fk_tasks_project", type_="foreignkey")
        batch.drop_column("team_id")
        batch.drop_column("project_id")

    with op.batch_alter_table("channels") as batch:
        batch.drop_constraint("fk_channels_project", type_="foreignkey")
        batch.drop_column("project_id")

    op.drop_index(op.f("ix_ai_meeting_summaries_tenant_id"), table_name="ai_meeting_summaries")
    op.drop_index(op.f("ix_ai_meeting_summaries_meeting_id"), table_name="ai_meeting_summaries")
    op.drop_index(op.f("ix_ai_meeting_summaries_id"), table_name="ai_meeting_summaries")
    op.drop_table("ai_meeting_summaries")
    op.drop_index(op.f("ix_meeting_notes_tenant_id"), table_name="meeting_notes")
    op.drop_index(op.f("ix_meeting_notes_meeting_id"), table_name="meeting_notes")
    op.drop_index(op.f("ix_meeting_notes_id"), table_name="meeting_notes")
    op.drop_table("meeting_notes")
    op.drop_index(op.f("ix_meeting_attendees_tenant_id"), table_name="meeting_attendees")
    op.drop_index(op.f("ix_meeting_attendees_meeting_id"), table_name="meeting_attendees")
    op.drop_index(op.f("ix_meeting_attendees_id"), table_name="meeting_attendees")
    op.drop_table("meeting_attendees")
    op.drop_index(op.f("ix_meetings_workspace_id"), table_name="meetings")
    op.drop_index(op.f("ix_meetings_tenant_id"), table_name="meetings")
    op.drop_index(op.f("ix_meetings_team_id"), table_name="meetings")
    op.drop_index(op.f("ix_meetings_project_id"), table_name="meetings")
    op.drop_index(op.f("ix_meetings_id"), table_name="meetings")
    op.drop_table("meetings")
    op.drop_index(op.f("ix_project_documents_workspace_id"), table_name="project_documents")
    op.drop_index(op.f("ix_project_documents_tenant_id"), table_name="project_documents")
    op.drop_index(op.f("ix_project_documents_project_id"), table_name="project_documents")
    op.drop_index(op.f("ix_project_documents_id"), table_name="project_documents")
    op.drop_table("project_documents")
    op.drop_index(op.f("ix_project_teams_workspace_id"), table_name="project_teams")
    op.drop_index(op.f("ix_project_teams_tenant_id"), table_name="project_teams")
    op.drop_index(op.f("ix_project_teams_team_id"), table_name="project_teams")
    op.drop_index(op.f("ix_project_teams_project_id"), table_name="project_teams")
    op.drop_index(op.f("ix_project_teams_id"), table_name="project_teams")
    op.drop_table("project_teams")
    op.drop_index(op.f("ix_team_members_workspace_id"), table_name="team_members")
    op.drop_index(op.f("ix_team_members_tenant_id"), table_name="team_members")
    op.drop_index(op.f("ix_team_members_team_id"), table_name="team_members")
    op.drop_index(op.f("ix_team_members_id"), table_name="team_members")
    op.drop_table("team_members")
    op.drop_index(op.f("ix_projects_workspace_id"), table_name="projects")
    op.drop_index(op.f("ix_projects_tenant_id"), table_name="projects")
    op.drop_index(op.f("ix_projects_id"), table_name="projects")
    op.drop_table("projects")
    op.drop_index(op.f("ix_teams_workspace_id"), table_name="teams")
    op.drop_index(op.f("ix_teams_tenant_id"), table_name="teams")
    op.drop_index(op.f("ix_teams_id"), table_name="teams")
    op.drop_table("teams")
