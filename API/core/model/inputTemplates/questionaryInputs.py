from flask_restx import fields


questionary_add_template = {
    "question_stem": fields.String,
    "alternatives": fields.List(fields.String),
    "category": fields.String,
}

questionary_id_template = {
    "question_id": fields.Integer
}

question_answer_template = {
    "question_id": fields.Integer,
    "answer_id": fields.Integer,
}


def answer_form(items):
    answers_template = {
        "answers": fields.List(
            fields.Nested(items)
        )
    }
    return answers_template
