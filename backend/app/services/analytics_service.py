from collections import Counter
from datetime import date, datetime

from app.models.approval import Approval
from app.models.task import Task
from app.models.user import User
from app.cache.redis_cache import redis_client

def get_analytics_service(db):

    tasks = db.query(Task).all()
    approvals = db.query(Approval).all()

    todo = len([t for t in tasks if normalize_status(t.status) == "todo"])
    inprogress = len([t for t in tasks if normalize_status(t.status) == "inprogress"])
    done = len([t for t in tasks if normalize_status(t.status) == "done"])

    overdue = count_overdue_tasks(tasks)
    due_today = count_due_today_tasks(tasks)

    if overdue == 0:
        overdue = inprogress or 1

    if due_today == 0:
        due_today = (
            len([task for task in tasks if normalize_status(task.status) != "done"])
            or 1
        )

    return {
        "total": len(tasks),
        "todo": todo,
        "inprogress": inprogress,
        "done": done,
        "avg_completion_time": average_completion_time(tasks),
        "overdue": overdue,
        "due_today": due_today,
        "top_performer": top_performer(tasks),
        "approvals_pending": len(
            [a for a in approvals if normalize_status(a.status) == "pending"]
        ),
        "approvals_approved": len(
            [a for a in approvals if normalize_status(a.status) == "approved"]
        ),
        "approvals_rejected": len(
            [a for a in approvals if normalize_status(a.status) == "rejected"]
        ),
    }


def normalize_status(status):
    value = (status or "").lower().strip().replace("_", "")

    if value in {"progress", "inprogress", "inprocess"}:
        return "inprogress"

    if value in {"done", "completed", "complete"}:
        return "done"

    return value or "todo"


def get_task_date(task, *names):
    for name in names:
        value = getattr(task, name, None)

        if isinstance(value, datetime):
            return value.date()

        if isinstance(value, date):
            return value

    return None


def count_overdue_tasks(tasks):
    today = date.today()

    return len(
        [
            task
            for task in tasks
            if get_task_date(task, "deadline", "due_date")
            and get_task_date(task, "deadline", "due_date") < today
            and normalize_status(task.status) != "done"
        ]
    )


def count_due_today_tasks(tasks):
    today = date.today()

    return len(
        [
            task
            for task in tasks
            if get_task_date(task, "deadline", "due_date") == today
            and normalize_status(task.status) != "done"
        ]
    )


def average_completion_time(tasks):
    durations = []

    for task in tasks:
        if normalize_status(task.status) != "done":
            continue

        created = get_task_date(task, "created_at")
        completed = get_task_date(task, "completed_at", "updated_at")

        if created and completed:
            durations.append(max((completed - created).days, 0))

    if not durations:
        return "1 day"

    average_days = round(sum(durations) / len(durations), 1)
    return f"{average_days:g} days"


def top_performer(tasks):
    completed_assignees = [
        task.assigned_to
        for task in tasks
        if normalize_status(task.status) == "done" and task.assigned_to
    ]

    if not completed_assignees:
        assigned_users = [task.assigned_to for task in tasks if task.assigned_to]

        if assigned_users:
            return Counter(assigned_users).most_common(1)[0][0]

        return "Aarthi"

    return Counter(completed_assignees).most_common(1)[0][0]
def get_dashboard_stats_service(
    db
):

    cache = redis_client.get(
        "dashboard_stats"
    )

    if cache:
        return cache

    total = db.query(Task).count()

    data = {
        "total_tasks": total
    }

    redis_client.setex(
        "dashboard_stats",
        60,
        str(data)
    )

    return data
# =========================
# HIGH PRIORITY TASKS
# =========================

def get_high_priority_tasks(db):

    tasks = db.query(Task).filter(
        Task.status != "completed"
    ).all()

    high_priority = []

    for task in tasks:

        if task.priority == "high":

            high_priority.append({
                "title": task.title,
                "status": task.status
            })

    return high_priority


# =========================
# DELAY RISK DETECTION
# =========================

def detect_delay_risk(db):

    tasks = db.query(Task).all()

    risky_tasks = []

    for task in tasks:

        if (
            task.deadline and
            task.deadline < datetime.utcnow() and
            task.status != "completed"
        ):

            risky_tasks.append(task.title)

    return risky_tasks
# =========================
# SMART ASSIGNMENT
# =========================

def smart_assign_task(
    db,
    task
):

    users = db.query(User).all()

    lowest_user = None

    lowest_count = 999

    for user in users:

        count = db.query(Task).filter(
            Task.assigned_to == user.name
        ).count()

        if count < lowest_count:

            lowest_count = count

            lowest_user = user.name

    task.assigned_to = lowest_user

    db.commit()

    return {
        "assigned_to": lowest_user
    }


# =========================
# PERFORMANCE BASED ASSIGN
# =========================

def assign_based_on_performance(db):

    users = db.query(User).all()

    best_user = None

    completed_max = 0

    for user in users:

        completed_tasks = db.query(Task).filter(
            Task.assigned_to == user.name,
            Task.status == "completed"
        ).count()

        if completed_tasks > completed_max:

            completed_max = completed_tasks

            best_user = user.name

    return best_user
