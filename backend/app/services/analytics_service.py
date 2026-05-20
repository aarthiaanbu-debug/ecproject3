from app.models.task import Task
from app.models.task import Task
from app.models.user import User
from datetime import datetime
from app.cache.redis_cache import redis_client

def get_analytics_service(db):

    tasks = db.query(Task).all()

    return {
        "total": len(tasks),
        "todo": len([t for t in tasks if t.status == "todo"]),
        "inprogress": len([t for t in tasks if t.status == "inprogress"]),
        "done": len([t for t in tasks if t.status == "done"])
    }
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