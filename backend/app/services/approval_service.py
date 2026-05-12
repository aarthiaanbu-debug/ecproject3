from app.models.approval import Approval


def get_approvals_service(db):
    return db.query(Approval).all()


def create_approval_service(db, data):
    approval = Approval(**data)
    db.add(approval)
    db.commit()
    db.refresh(approval)
    return approval