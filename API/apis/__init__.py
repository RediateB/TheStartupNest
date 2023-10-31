from flask import Blueprint, request
from flask_restx import Api

from API.apis.questionaryRoutes import questionary_ns
from API.apis.sessionRoutes import session_ns
from API.apis.accountRoutes import account_ns
from API.apis.appointmentRoutes import appointment_ns


blueprint_v1 = Blueprint('api_v1', __name__)
api_v1 = Api(
    blueprint_v1,
    title='StartUpNest API',
    version='1.0',
    description='StartUpNest is a mobile application that uses AI to detect and diagnose leaf disease',
)

api_v1.add_namespace(session_ns)
api_v1.add_namespace(account_ns)
api_v1.add_namespace(questionary_ns)
api_v1.add_namespace(appointment_ns)
