from fastapi import Depends, HTTPException

from app.utils.deps import get_current_user


def role_required(allowed_roles: list):

    def checker(
        current_user = Depends(
            get_current_user
        )
    ):

        if current_user.role not in allowed_roles:

            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )

        return current_user

    return checker