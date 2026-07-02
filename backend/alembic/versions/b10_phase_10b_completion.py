"""Phase 10B collaboration completion.

Revision ID: b10_phase_10b
Revises: a791e497c55a
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b10_phase_10b"
down_revision: Union[str, Sequence[str], None] = "a791e497c55a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("workspaces") as batch:
        batch.create_foreign_key("fk_workspaces_creator", "users", ["created_by"], ["id"])
    with op.batch_alter_table("workspace_members") as batch:
        batch.create_foreign_key("fk_workspace_members_workspace", "workspaces", ["workspace_id"], ["id"])
        batch.create_foreign_key("fk_workspace_members_user", "users", ["user_id"], ["id"])
        batch.create_unique_constraint("uq_workspace_member", ["workspace_id", "user_id"])
    with op.batch_alter_table("channels") as batch:
        batch.create_foreign_key("fk_channels_workspace", "workspaces", ["workspace_id"], ["id"])
        batch.create_foreign_key("fk_channels_creator", "users", ["created_by"], ["id"])
    with op.batch_alter_table("channel_members") as batch:
        batch.create_foreign_key("fk_channel_members_channel", "channels", ["channel_id"], ["id"])
        batch.create_foreign_key("fk_channel_members_user", "users", ["user_id"], ["id"])
        batch.create_unique_constraint("uq_channel_member", ["channel_id", "user_id"])
    with op.batch_alter_table("workspace_messages") as batch:
        batch.add_column(sa.Column("edited_at", sa.DateTime(), nullable=True))
        batch.create_foreign_key("fk_workspace_messages_user", "users", ["user_id"], ["id"])

    with op.batch_alter_table("channel_messages") as batch:
        batch.add_column(sa.Column("parent_message_id", sa.Integer(), nullable=True))
        batch.create_foreign_key(
            "fk_channel_messages_parent",
            "channel_messages",
            ["parent_message_id"],
            ["id"],
        )
        batch.create_foreign_key("fk_channel_messages_sender", "users", ["sender_id"], ["id"])

    with op.batch_alter_table("channel_tasks") as batch:
        batch.add_column(sa.Column("due_date", sa.DateTime(), nullable=True))
        batch.create_foreign_key("fk_channel_tasks_creator", "users", ["created_by"], ["id"])
        batch.create_foreign_key("fk_channel_tasks_assignee", "users", ["assigned_to"], ["id"])

    with op.batch_alter_table("workspace_tasks") as batch:
        batch.create_foreign_key("fk_workspace_tasks_creator", "users", ["created_by"], ["id"])
        batch.create_foreign_key("fk_workspace_tasks_assignee", "users", ["assigned_to"], ["id"])

    for table_name in ("task_documents", "approval_documents"):
        with op.batch_alter_table(table_name) as batch:
            batch.add_column(
                sa.Column("document_type", sa.String(length=100), nullable=False, server_default="OTHER")
            )
            batch.create_foreign_key(
                f"fk_{table_name}_uploader", "users", ["uploaded_by"], ["id"]
            )
            batch.add_column(sa.Column("file_size", sa.Integer(), nullable=False, server_default="0"))
            batch.add_column(
                sa.Column(
                    "mime_type",
                    sa.String(length=255),
                    nullable=False,
                    server_default="application/octet-stream",
                )
            )


def downgrade() -> None:
    for table_name in ("approval_documents", "task_documents"):
        with op.batch_alter_table(table_name) as batch:
            batch.drop_constraint(f"fk_{table_name}_uploader", type_="foreignkey")
            batch.drop_column("mime_type")
            batch.drop_column("file_size")
            batch.drop_column("document_type")

    with op.batch_alter_table("channel_tasks") as batch:
        batch.drop_constraint("fk_channel_tasks_assignee", type_="foreignkey")
        batch.drop_constraint("fk_channel_tasks_creator", type_="foreignkey")
        batch.drop_column("due_date")

    with op.batch_alter_table("workspace_tasks") as batch:
        batch.drop_constraint("fk_workspace_tasks_assignee", type_="foreignkey")
        batch.drop_constraint("fk_workspace_tasks_creator", type_="foreignkey")

    with op.batch_alter_table("channel_messages") as batch:
        batch.drop_constraint("fk_channel_messages_sender", type_="foreignkey")
        batch.drop_constraint("fk_channel_messages_parent", type_="foreignkey")
        batch.drop_column("parent_message_id")

    with op.batch_alter_table("workspace_messages") as batch:
        batch.drop_constraint("fk_workspace_messages_user", type_="foreignkey")
        batch.drop_column("edited_at")

    with op.batch_alter_table("channel_members") as batch:
        batch.drop_constraint("uq_channel_member", type_="unique")
        batch.drop_constraint("fk_channel_members_user", type_="foreignkey")
        batch.drop_constraint("fk_channel_members_channel", type_="foreignkey")
    with op.batch_alter_table("channels") as batch:
        batch.drop_constraint("fk_channels_creator", type_="foreignkey")
        batch.drop_constraint("fk_channels_workspace", type_="foreignkey")
    with op.batch_alter_table("workspace_members") as batch:
        batch.drop_constraint("uq_workspace_member", type_="unique")
        batch.drop_constraint("fk_workspace_members_user", type_="foreignkey")
        batch.drop_constraint("fk_workspace_members_workspace", type_="foreignkey")
    with op.batch_alter_table("workspaces") as batch:
        batch.drop_constraint("fk_workspaces_creator", type_="foreignkey")
