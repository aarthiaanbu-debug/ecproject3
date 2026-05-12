from app.models.comment import Comment


def get_comments_service(db, task_id):
    return db.query(Comment).filter(Comment.task_id == task_id).all()


def add_comment_service(db, task_id, content):
    comment = Comment(task_id=task_id, content=content)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment