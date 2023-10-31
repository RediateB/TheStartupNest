from flask import request, abort
from flask_cors import cross_origin
from flask_login import login_required, current_user
from flask_restx import Namespace, Resource

from API.core.appointment import AppointmentControl
from API.core.model.inputTemplates import (appointment_template, schedule_form, schedule_id_template)
from API.core.middelware import ALC

api_appointment = Namespace("appointment", description="Endpoint to controlling appointment")
schedule_id_form = api_appointment.model("schedule Id Form", schedule_id_template)
available_data = api_appointment.model("Available Date Form", appointment_template)
schedules_form = api_appointment.model("Schedule Form", schedule_form(available_data))


@api_appointment.route("/")
class GetAppointments(Resource):
    @api_appointment.doc("End point for getting available date for appointment")
    @login_required
    @cross_origin()
    def get(self):
        try:
            data, status_code = AppointmentControl.get_consultant_schedule()
            return data, status_code, {"Access-Control-Allow-Credentials": "true"}
        except Exception as e:
            print(e)
            return {"error": str(e)}, 500, {"Access-Control-Allow-Credentials": "true"}


@api_appointment.route("/create-schedule/")
class CreateSchedule(Resource):
    @api_appointment.doc("End point for creating available date schedule")
    @api_appointment.expect(schedules_form)
    @login_required
    @cross_origin()
    def post(self):
        try:
            if (ALC.has_owner_privilege() or
                    ALC.has_administrator_privilege() or
                    ALC.has_consultant_privilege()):
                data, status_code = AppointmentControl.create_appointment(request.json)
                return data, status_code, {"Access-Control-Allow-Credentials": "true"}
            else:
                abort(401)
        except Exception as e:
            print(e)
            return {"error": str(e)}, 500, {"Access-Control-Allow-Credentials": "true"}


@api_appointment.route("/book-appointment/")
class BookAppointment(Resource):
    @api_appointment.doc("End point for booking available date")
    @api_appointment.expect(schedule_id_form)
    @login_required
    @cross_origin()
    def post(self):
        try:
            if (ALC.has_owner_privilege() or
                    ALC.has_administrator_privilege() or
                    ALC.has_customer_privilege()):
                data, status_code = AppointmentControl.choose_appointment(request.json)
                return data, status_code, {"Access-Control-Allow-Credentials": "true"}
            else:
                abort(401)
        except Exception as e:
            print(e)
            return {"error": str(e)}, 500, {"Access-Control-Allow-Credentials": "true"}


@api_appointment.route("/edit-schedule/")
class EditSchedule(Resource):
    @api_appointment.doc("End point for editing schedule")
    @login_required
    @cross_origin()
    def put(self):
        try:
            if (ALC.has_owner_privilege() or
                    ALC.has_administrator_privilege() or
                    ALC.has_consultant_privilege()):
                data, status_code = AppointmentControl.edit_appointment()
                return data, status_code, {"Access-Control-Allow-Credentials": "true"}
            else:
                abort(401)
        except Exception as e:
            print(e)
            return {"error": str(e)}, 500, {"Access-Control-Allow-Credentials": "true"}


@api_appointment.route("/cancel-booking/")
class CancelBooking(Resource):
    @api_appointment.doc("End point for cancel schedule booking")
    @api_appointment.expect(schedule_id_form)
    @login_required
    @cross_origin()
    def put(self):
        try:
            if (ALC.has_owner_privilege() or
                    ALC.has_administrator_privilege() or
                    ALC.has_consultant_privilege() or
                    ALC.has_customer_privilege()
            ):
                data, status_code = AppointmentControl.cancel_appointment(request.json)
                return data, status_code, {"Access-Control-Allow-Credentials": "true"}
            else:
                abort(401)
        except Exception as e:
            print(e)
            return {"error": str(e)}, 500, {"Access-Control-Allow-Credentials": "true"}


@api_appointment.route("/view-upcoming-schedule/")
class ViewUpcomingSchedule(Resource):
    @api_appointment.doc("End point for viewing upcoming schedule")
    @login_required
    @cross_origin()
    def get(self):
        try:
            if (ALC.has_owner_privilege() or
                    ALC.has_administrator_privilege() or
                    ALC.has_consultant_privilege() or
                    ALC.has_customer_privilege()
            ):
                if current_user.role.value == "User":
                    data, status_code = AppointmentControl.client_view_upcoming_appointment()
                    return data, status_code, {"Access-Control-Allow-Credentials": "true"}
                elif current_user.role.value == "Consultant":
                    data, status_code = AppointmentControl.consultant_view_upcoming_appointment()
                    return data, status_code, {"Access-Control-Allow-Credentials": "true"}
                else:
                    raise KeyError
            else:
                abort(401)
        except Exception as e:
            print(e)
            return {"error": str(e)}, 500, {"Access-Control-Allow-Credentials": "true"}
