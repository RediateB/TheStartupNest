from datetime import datetime
from flask_login import current_user
from API.dbSession import Session
from API.core.model.databaseModel import (ConsultantClientPair, Appointment)
from API.core.model.helperUtils import InvalidUserInput
from API.core.model.enumTypes import MeetingType


class AppointmentControl:
    @staticmethod
    def create_appointment(incoming_data):
        try:
            if not incoming_data.get("available date") or len(incoming_data.get("available date")) < 1:
                raise InvalidUserInput(message="Required Field Missing!")
            for appoint_dates in incoming_data.get("available date"):
                client_id = appoint_dates.get("client")
                selected_date = appoint_dates.get("date")
                selected_time = appoint_dates.get("time")
                meeting_type = appoint_dates.get("meeting_type")

                if [
                    client_id, selected_date, selected_time,
                    meeting_type
                ].__contains__(None):
                    raise InvalidUserInput("Required Field Missing!")
                with Session() as session:
                    check_pair = session.query(ConsultantClientPair).filter(
                        ConsultantClientPair.consultant == current_user.id,
                        ConsultantClientPair.client == client_id
                    ).first()

                    if not check_pair:
                        raise InvalidUserInput(message="Invalid Consultant Client Pair")

                    date_format = "%Y-%m-%d"
                    time_format = "%H:%M:%S"
                    new_appointment = Appointment(
                        consultant=current_user,
                        client=client_id,
                        date=datetime.strptime(selected_date, date_format),
                        time=datetime.strptime(selected_time, time_format),
                        meeting_type=MeetingType(meeting_type)
                    )
                    session.add(new_appointment)
                    session.commit()

                return {"result": "Appointment created successful"}, 200
        except InvalidUserInput as err:
            return {"error": err.message}, 400
        except Exception:
            raise

    @staticmethod
    def choose_appointment(incoming_data):
        try:
            schedule_id = incoming_data.get("id")
            if not schedule_id:
                raise InvalidUserInput(message="Required field missing")
            with Session() as session:
                schedule = session.query(Appointment).filter(
                    Appointment.id == schedule_id,
                    Appointment.client == current_user.id,
                ).first()
                if not schedule:
                    raise InvalidUserInput(message="Invalid schedule")
                if schedule.booked:
                    raise InvalidUserInput(message="Appointment already booked")

                schedule.booked = True
                session.commit()
                return {"result": "Appointment booked successfully"}, 200
        except InvalidUserInput as err:
            return {"error": err.message}, 400
        except Exception:
            raise

    @staticmethod
    def get_consultant_schedule():
        try:
            with Session() as session:
                schedules = session.query(Appointment).filter(
                    Appointment.client == current_user.id).all()
                available_date = []
                if not schedules:
                    return "No available date found for meeting", 201
                for schedule in schedules:
                    data = {
                        "id": schedule.id,
                        "date": schedule.date.strftime("%Y-%m-%d"),
                        "time": schedule.time.strftime("%H:%M:%S"),
                        "type": schedule.meeting_type.value
                    }
                    available_date.append(data)

                return {"result": {"available dates": available_date}}, 200
        except InvalidUserInput as err:
            return {"error": err.message}, 400
        except Exception:
            raise

    @staticmethod
    def edit_appointment():
        try:
            pass
        except InvalidUserInput as err:
            return {"error": err.message}, 400
        except Exception:
            raise

    @staticmethod
    def cancel_appointment(incoming_data):
        try:
            schedule_id = incoming_data.get("id")
            reason = incoming_data.get("reason")
            if [schedule_id, reason].__contains__(None):
                raise InvalidUserInput(message="Required field missing")
            with Session() as session:
                schedule = session.query(Appointment).filter(
                    Appointment.id == schedule_id,
                    Appointment.client == current_user.id,
                ).first()
                if not schedule:
                    raise InvalidUserInput(message="Invalid schedule")
                if schedule.booked:
                    raise InvalidUserInput(message="Appointment already booked")

                schedule.booked = True
                schedule.canceled = True
                schedule.cancellation_reason = str(reason)
                session.commit()
                return {"result": "Appointment canceled successfully"}, 200

        except InvalidUserInput as err:
            return {"error": err.message}, 400
        except Exception:
            raise

    @staticmethod
    def client_view_upcoming_appointment():
        try:
            with Session() as session:
                schedules = session.query(Appointment).filter(
                    Appointment.client == current_user.id,
                    Appointment.booked == True,
                    Appointment.canceled == False
                ).all()
                appointments = []

                for schedule in schedules:
                    data = {
                        "id": schedule.id,
                        "date": schedule.date.strftime("%Y-%m-%d"),
                        "time": schedule.time.strftime("%H:%M:%S"),
                        "type": schedule.meeting_type.value
                    }
                    appointments.append(data)

                return {"result": {"upcoming appointments": appointments}}, 200
        except InvalidUserInput as err:
            return {"error": err.message}, 400
        except Exception:
            raise

    @staticmethod
    def consultant_view_upcoming_appointment():
        try:
            with Session() as session:
                schedules = session.query(Appointment).filter(
                    Appointment.consultant == current_user.id,
                    Appointment.booked == True,
                    Appointment.canceled == False
                ).all()
                appointments = []

                for schedule in schedules:
                    data = {
                        "id": schedule.id,
                        "date": schedule.date.strftime("%Y-%m-%d"),
                        "time": schedule.time.strftime("%H:%M:%S"),
                        "type": schedule.meeting_type.value
                    }
                    appointments.append(data)

                return {"result": {"upcoming appointments": appointments}}, 200
        except InvalidUserInput as err:
            return {"error": err.message}, 400
        except Exception:
            raise
