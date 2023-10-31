from flask_restx import fields

signup_template = {
    "username": fields.String,
    "firstName": fields.String,
    "lastName": fields.String,
    "email": fields.String,
    "password": fields.String,
}

login_template = {
    "username": fields.String,
    "password": fields.String,
}

update_password_template = {
    "current_pass": fields.String,
    "new_pass": fields.String,
    "new_pass_2": fields.String,
}

update_details_template = {
    "username": fields.String,
    "firstName": fields.String,
    "lastName": fields.String,
    "email": fields.String,
}

account_id_template = {
    "account_id": fields.Integer
}