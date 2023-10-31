from flask import request
from flask_cors import cross_origin
from flask_login import login_required, current_user

from flask_restx import Namespace, Resource

from API.core.model.enumTypes import UserTypeEnum
from API.core.model.inputTemplates import (signup_template, update_password_template,
                                           update_details_template, account_id_template)

from API.core.account import AccountControl

api_account = Namespace('account', description="Endpoint to controlling accounts ")

signup_form = api_account.model('New User Form', signup_template)
password_update_form = api_account.model('Password Update Form', update_password_template)
update_details_form = api_account.model('Detail Update Form', update_details_template)
account_id_form = api_account.model('Account Id Form', account_id_template)


@api_account.route("/add-new/client/")
class NewUserProfile(Resource):
    @api_account.doc("End point for add new user into the system")
    @api_account.expect(signup_form)
    @cross_origin()
    def post(self,):
        """
        End point for add new user into the system
        """
        try:
            data, status_code = AccountControl.create_account(request.json, UserTypeEnum.USER)
            return data, status_code, {"Access-Control-Allow-Credentials": "true"}
        except Exception as e:
            return {"error": str(e)}, 500


@api_account.route("/add-new/consultant/")
class NewUserProfile(Resource):
    @api_account.doc("End point for add new consultant into the system")
    @api_account.expect(signup_form)
    @cross_origin()
    def post(self, role):
        """
        End point for add new consultant into the system
        """
        try:
            data, status_code = AccountControl.create_account(request.json, UserTypeEnum.CONSULTANT)
            return data, status_code, {"Access-Control-Allow-Credentials": "true"}
        except Exception as e:
            return {"error": str(e)}, 500


@api_account.route("/")
class GetSelfProfile(Resource):
    @api_account.doc("End point for getting self profile details")
    @cross_origin()
    @login_required
    def get(self):
        """
        End point for getting self profile details
        """
        data, status_code = AccountControl.get_account()
        return data, status_code, {"Access-Control-Allow-Credentials": "true"}


@api_account.route("/consultant/")
class GetConsultantProfile(Resource):
    @api_account.doc("End point for getting all consultant profiles")
    @cross_origin()
    @login_required
    def get(self):
        """
        End point for getting all consultant profiles
        """
        data, status_code = AccountControl.get_consultants()
        return data, status_code, {"Access-Control-Allow-Credentials": "true"}


@api_account.route("/update-password/")
class UpdatePassword(Resource):
    @api_account.doc("End point for Updating your password")
    @api_account.expect(password_update_form)
    @cross_origin()
    def put(self):
        """
        End point for Updating self password
        """
        data, status_code = AccountControl.update_password(request.json)
        return data, status_code, {"Access-Control-Allow-Credentials": "true"}


@api_account.route("/update-details/")
class UpdateDetails(Resource):
    @api_account.doc("End point for Updating your account Details")
    @api_account.expect(update_details_form)
    @cross_origin()
    def put(self):
        """
        End point for Updating self password
        """
        data, status_code = AccountControl.update_details(request.json)
        return data, status_code, {"Access-Control-Allow-Credentials": "true"}


@api_account.route("/delete-account/")
class UpdateDetails(Resource):
    @api_account.doc("End point for Deleting your account")
    @api_account.expect(update_details_form)
    @cross_origin()
    def delete(self):
        """
        End point for Deleting self Details
        """
        data, status_code = AccountControl.delete_account()
        return data, status_code, {"Access-Control-Allow-Credentials": "true"}


@api_account.route("/approve/")
class ApproveConsultant(Resource):
    @api_account.doc("End point for Approving consultant account")
    @api_account.expect(account_id_form)
    @cross_origin()
    def put(self):
        """
        End point for Approving consultant account
        """
        data, status_code = AccountControl.approve_consultant(request.json)
        return data, status_code, {"Access-Control-Allow-Credentials": "true"}
