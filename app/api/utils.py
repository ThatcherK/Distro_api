import os
from functools import wraps

from flask import current_app, request
from app.api.models import User
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def requires_admin_access(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        response_object = {"message": "Provide valid auth Token"}
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return response_object, 401
        auth_token = auth_header.split(" ")[1]
        user_id = User.decode_auth_token(auth_token)
        if isinstance(user_id, str):
            response_object = {
                "message": user_id
                }
            return response_object, 401
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return response_object, 401
        if user.role_id > 1:
            return {"message": "Requires admin access"}, 401
        return function(*args, **kwargs)

    return decorated_function

def validate_invite_user(function):
    """ decorator function to validate invite user json """

    @wraps(function)
    def decorating_function(*args, **kwargs):
        """ Flask validation of invite user json """
        if request.method == "POST":
            post_data = request.get_json()
            email = post_data.get("email")
            role_id = post_data.get("role_id")
            response_object = {
                    "status": "Fail",
                    "message": "Invalid payload",
                }
            if not post_data:
                return response_object, 400
            if email == None  or role_id == None:
                return response_object, 400
        return function(*args, **kwargs)

    return decorating_function

def send_invite_email(invite_code, email, frontend_url):
    message = Mail(
        from_email=f'{current_app.config.get("SENDGRID_SENDER_MAIL")}',
        to_emails=f"{email}",
        subject="DistroIQ Platform Invite",
        html_content=f"""<p>Hello,
        You have been invited to the DistroIQ platform with this code<br>
        <strong>{invite_code}</strong><br><br>Please copy the code, 
        follow this link {frontend_url} to sign up! </p>""",
    )
    try:
        sg = SendGridAPIClient(current_app.config.get("SENDGRID_API_KEY"))
        response = sg.send(message)

    except Exception as e:
        return repr(e)
