from flask_restx import fields

appointment_template = {
    "client": fields.Integer,
    "date": fields.Date,
    "time": fields.DateTime,
    "meeting_type": fields.String,
}

schedule_id_template = {
    "id": fields.Integer,
    "reason": fields.Integer,
}


def schedule_form(items):
    schedule_template = {
        "available date": fields.List(
            fields.Nested(items)
        )
    }
    return schedule_template
