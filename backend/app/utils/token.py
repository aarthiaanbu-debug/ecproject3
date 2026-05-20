from itsdangerous import URLSafeTimedSerializer

SECRET_KEY = "resetsecret"

serializer = URLSafeTimedSerializer(
    SECRET_KEY
)


def generate_reset_token(email: str):

    return serializer.dumps(
        email,
        salt="password-reset"
    )


def verify_reset_token(token: str):

    try:

        email = serializer.loads(
            token,
            salt="password-reset",
            max_age=3600
        )

        return email

    except:
        return None