from API.core.model.databaseModel import (Stem, Answer, Question)
from API.core.model.enumTypes import QuestionCategory
from API.core.model.helperUtils import InvalidUserInput
from API.dbSession import Session


class QuestionaryControl:
    @staticmethod
    def create_questionary(incoming_data):
        try:
            with Session() as session:
                # Create a stem for the multiple-choice question.
                incoming_question_stem = incoming_data.get("question_stem")
                incoming_alternatives = incoming_data.get("alternatives")
                incoming_category = incoming_data.get("category")

                if ([incoming_category, incoming_alternatives, incoming_question_stem].__contains__(None) or
                        len(incoming_alternatives) < 2):
                    raise InvalidUserInput(message="Required Field Missing")

                stem = Stem(questionStems=str(incoming_question_stem))

                # Create multiple answer choices for the question.
                answers = []
                for incoming_alternative in incoming_alternatives:
                    alternative = Answer(answer=incoming_alternative)
                    answers.append(alternative)

                # Create the question and associate it with the stem and answer choices.
                question = Question(
                    category=QuestionCategory.CLIENT_QUIZ,
                    question_stem=stem,
                    alternatives=answers
                )

                # Add the instances to the session.
                session.add(stem)
                session.add(question)

                for answer in answers:
                    session.add(answer)
                # Commit the changes to the database.
                session.commit()
                return "True", 200
        except InvalidUserInput as err:
            return {"error": err.message}, 400
        except Exception:
            raise

    @staticmethod
    def view_questionary_list():
        try:
            with Session() as session:
                consultant_questionary_set = session.query(Question).filter(
                    Question.category == QuestionCategory.CONSULTANT_QUIZ).all()
                client_questionary_set = session.query(Question).filter(
                    Question.category == QuestionCategory.CLIENT_QUIZ).all()
                result = {
                    "consultant questions": len(consultant_questionary_set),
                    "client questions": len(client_questionary_set)
                }
                return {"summary": result}, 200
        except InvalidUserInput as err:
            return {"error": err.message}, 400
        except Exception:
            raise

    @staticmethod
    def edit_questionary():
        try:
            pass
        except InvalidUserInput as err:
            return {"error": err.message}, 400
        except Exception:
            raise

    @staticmethod
    def delete_questionary(question_id):
        try:
            with Session() as session:
                question = session.query(Question).filter(Question.id == question_id).first()
                if question:
                    session.delete(question)
                    session.commit()
                    return {"result": "Question deleted successfully"}, 201
                else:
                    raise InvalidUserInput(message="Question not found")
        except InvalidUserInput as err:
            return {"error": err.message}, 400
        except Exception:
            raise

    @staticmethod
    def get_client_questionary():
        try:
            with Session() as session:
                question_queryset = session.query(Question).filter(
                    Question.category == QuestionCategory.CLIENT_QUIZ).all()

                question_set = []

                for question in question_queryset:
                    alternatives = []

                    for answer in question.alternatives:
                        alternative = {
                            "option": answer.answer,
                            "id": answer.id
                        }
                        alternatives.append(alternative)
                    data = {
                        "question": question.question_stem.questionStems,
                        "alternatives": alternatives,
                        "id": question.id,
                    }
                    question_set.append(data)

                return question_set, 200

        except InvalidUserInput as err:
            return {"error": err.message}, 400
        except Exception:
            raise

    @staticmethod
    def get_consultant_questionary():
        try:
            with Session() as session:
                question_queryset = session.query(Question).filter(
                    Question.category == QuestionCategory.CONSULTANT_QUIZ).all()

                question_set = []

                for question in question_queryset:
                    alternatives = []

                    for answer in question.alternatives:
                        alternative = {
                            "option": answer.answer,
                            "id": answer.id
                        }
                        alternatives.append(alternative)
                    data = {
                        "question": question.question_stem.questionStems,
                        "alternatives": alternatives,
                        "id": question.id,
                    }
                    question_set.append(data)

                return question_set, 200

        except InvalidUserInput as err:
            return {"error": err.message}, 400
        except Exception:
            raise

    @staticmethod
    def answer_questions(incoming_data):
        try:
            if not incoming_data.get("answers"):
                raise InvalidUserInput(message="Missing required field")

            with Session() as session:
                question_answer_pair = []
                for answers in incoming_data.get("answers"):
                    if [answers.get("question_id"), answers.get("answer_id")].__contains__(None):
                        raise InvalidUserInput(message="Missing required field")

                    question = session.query(Question).filter(Question.id == answers.get("question_id")).first()
                    answer = session.query(Answer).filter(Answer.id == answers.get("answer_id")).first()
                    if [answer, question].__contains__(None):
                        raise InvalidUserInput("Invalid Answer")
                    pair = tuple([question.question_stem.questionStems, answer.answer])
                    question_answer_pair.append(pair)

                return question_answer_pair, 200
        except InvalidUserInput as err:
            return {"error": err.message}, 400
        except Exception:
            raise
