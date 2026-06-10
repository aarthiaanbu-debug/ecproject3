from sqlalchemy import inspect, text

from app.database import engine


def add_missing_columns():
    inspector = inspect(engine)

    ensure_columns(
        inspector,
        "audit_logs",
        {
            "user_id": "INTEGER",
            "user": "VARCHAR",
            "action": "VARCHAR",
            "details": "TEXT",
            "module_name": "VARCHAR",
            "action_type": "VARCHAR",
            "record_id": "INTEGER",
            "old_data": "TEXT",
            "new_data": "TEXT",
            "ip_address": "VARCHAR",
            "user_agent": "VARCHAR",
            "created_at": "DATETIME",
        },
    )
    ensure_columns(
        inspector,
        "organizations",
        {
            "domain": "VARCHAR",
            "plan": "VARCHAR DEFAULT 'basic'",
            "is_active": "INTEGER DEFAULT 1",
            "created_at": "DATETIME",
        },
    )
    ensure_columns(
        inspector,
        "users",
        {
            "organization_id": "INTEGER",
        },
    )
    ensure_columns(
        inspector,
        "tasks",
        {
            "organization_id": "INTEGER",
            "priority": "VARCHAR DEFAULT 'medium'",
            "deadline": "DATETIME",
            "created_at": "DATETIME",
            "completed_at": "DATETIME",
            "sla_status": "VARCHAR",
            "sla_due_time": "DATETIME",
            "is_sla_breached": "BOOLEAN DEFAULT 0",
        },
    )
    ensure_columns(
        inspector,
        "approvals",
        {
            "sla_status": "VARCHAR",
            "sla_due_time": "DATETIME",
            "is_escalated": "BOOLEAN DEFAULT 0",
            "current_escalation_to": "INTEGER",
        },
    )
    ensure_columns(
        inspector,
        "notifications",
        {
            "user_id": "INTEGER",
            "notification_type": "VARCHAR DEFAULT 'general'",
            "priority": "VARCHAR DEFAULT 'normal'",
        },
    )


def ensure_columns(inspector, table_name, columns):
    if not inspector.has_table(table_name):
        return

    existing = {column["name"] for column in inspector.get_columns(table_name)}

    with engine.begin() as connection:
        for column_name, column_type in columns.items():
            if column_name not in existing:
                connection.execute(
                    text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")
                )
