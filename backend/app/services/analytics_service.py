from app.models.task import Task


def get_analytics_service(db):

    tasks = db.query(Task).all()

    return {
        "total": len(tasks),
        "todo": len([t for t in tasks if t.status == "todo"]),
        "inprogress": len([t for t in tasks if t.status == "inprogress"]),
        "done": len([t for t in tasks if t.status == "done"])
    }