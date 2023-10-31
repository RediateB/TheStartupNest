import os
from flask import request
from flask_cors import cross_origin
from flask_login import login_required

from flask_restx import Namespace, Resource
from API.core.model.inputTemplates import (login_template)

from API.core.session import SessionControl

api_session = Namespace('session', description="Endpoint to controlling session")

login_form = api_session.model('Login Form', login_template)


@api_session.route("/login/")
class Login(Resource):
    @api_session.doc("End point for signing into the system")
    @cross_origin()
    @api_session.expect(login_form)
    def post(self):
        try:
            data, status_code = SessionControl.signin_user(request.json)
            return data, status_code, {"Access-Control-Allow-Credentials": "true"}
        except Exception as e:
            print(e)
            return {"error": str(e)}, 500, {"Access-Control-Allow-Credentials": "true"}


@api_session.route("/logout/")
class Logout(Resource):
    @api_session.doc("End point for signing out of the system")
    @cross_origin()
    @login_required
    def post(self):
        try:
            data, status_code = SessionControl.sign_out_user()
            return data, status_code, {"Access-Control-Allow-Credentials": "true"}
        except Exception as e:
            return {"error": str(e)}, 500, {"Access-Control-Allow-Credentials": "true"}


@api_session.route("/check-auth/")
class Profile(Resource):
    @api_session.doc("End point for checking if user is authenticated")
    @cross_origin()
    @login_required
    def get(self):
        try:
            return {"result": "logged in"}, 200, {"Access-Control-Allow-Credentials": "true"}
        except Exception as e:
            return {"error": str(e)}, 500, {"Access-Control-Allow-Credentials": "true"}
