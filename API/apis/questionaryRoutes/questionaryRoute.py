from flask import request
from flask_cors import cross_origin
from flask_login import login_required
from API.core.model.inputTemplates import (questionary_add_template, questionary_id_template,
                                           question_answer_template, answer_form)

from flask_restx import Namespace, Resource
from API.core.questionary import QuestionaryControl


api_questionary = Namespace('questionary', description="Endpoint to controlling questionary")

questionary_add_form = api_questionary.model("Questionary Add Form", questionary_add_template)
questionary_id_form = api_questionary.model("Questionary Id Form", questionary_id_template)
questionary_answer_form = api_questionary.model("Question Answer Form", question_answer_template)
answer_form = api_questionary.model("Answers Form", answer_form(questionary_answer_form))


@api_questionary.route("/add/")
class AddQuestion(Resource):
    @api_questionary.doc("End point for adding new question")
    @api_questionary.expect(questionary_add_form)
    @cross_origin()
    def post(self):
        try:
            data, status_code = QuestionaryControl.create_questionary(request.json)
            return data, status_code, {"Access-Control-Allow-Credentials": "true"}
        except Exception as e:
            print(e)
            return {"error": str(e)}, 500, {"Access-Control-Allow-Credentials": "true"}


@api_questionary.route("/get-questionary-info/")
class GetQuestionaryInfo(Resource):
    @api_questionary.doc("End point for getting questionary info")
    @cross_origin()
    def get(self):
        try:
            data, status_code = QuestionaryControl.view_questionary_list()
            return data, status_code, {"Access-Control-Allow-Credentials": "true"}
        except Exception as e:
            print(e)
            return {"error": str(e)}, 500, {"Access-Control-Allow-Credentials": "true"}


@api_questionary.route("/get-client-questions/")
class GetClientQuestions(Resource):
    @api_questionary.doc("End point for getting client set of questions")
    @cross_origin()
    def get(self):
        try:
            data, status_code = QuestionaryControl.get_client_questionary()
            return data, status_code, {"Access-Control-Allow-Credentials": "true"}
        except Exception as e:
            print(e)
            return {"error": str(e)}, 500, {"Access-Control-Allow-Credentials": "true"}


@api_questionary.route("/get-consultant-questions/")
class GetConsultantQuestions(Resource):
    @api_questionary.doc("End point for getting consultant set of questions")
    @cross_origin()
    def get(self):
        try:
            data, status_code = QuestionaryControl.get_consultant_questionary()
            return data, status_code, {"Access-Control-Allow-Credentials": "true"}
        except Exception as e:
            print(e)
            return {"error": str(e)}, 500, {"Access-Control-Allow-Credentials": "true"}


@api_questionary.route("/delete-question/")
class DeleteQuestion(Resource):
    @api_questionary.doc("End point for deleting a question")
    @api_questionary.expect(questionary_id_form)
    @cross_origin()
    def delete(self):
        try:
            question_id = request.json["question_id"]
            data, status_code = QuestionaryControl.delete_questionary(question_id)
            return data, status_code, {"Access-Control-Allow-Credentials": "true"}
        except Exception as e:
            print(e)
            return {"error": str(e)}, 500, {"Access-Control-Allow-Credentials": "true"}


@api_questionary.route("/submit-answer/")
class AnswerQuestion(Resource):
    @api_questionary.doc("End point for submitting an answer")
    @api_questionary.expect(answer_form)
    @cross_origin()
    def post(self):
        try:
            data, status_code = QuestionaryControl.answer_questions(request.json)
            return data, status_code, {"Access-Control-Allow-Credentials": "true"}
        except Exception as e:
            print(e)
            return {"error": str(e)}, 500, {"Access-Control-Allow-Credentials": "true"}

