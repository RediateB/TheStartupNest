from flask import Flask
from API.core.model.databaseModel import AccountModel
from API.extension import sql_db, migrate, login_manager, flask_bcrypt
from config import Config

from flask_restx import Resource, Api
from API.core.questionary import QuestionaryControl

app = Flask(__name__)
api = Api(app)

app.config.from_object(Config)
login_manager.init_app(app)
sql_db.init_app(app)
migrate.init_app(app, sql_db)
flask_bcrypt.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    from API.dbSession import Session

    with Session() as session:
        try:
            return (
                session.query(AccountModel)
                .filter(AccountModel.alternative_id == user_id)
                .first()
            )
        except:
            pass


from API.apis import blueprint_v1 as api_v1

app.register_blueprint(api_v1, url_prefix="/startup-nest-api/api/v1/")

if __name__ == '__main__':
    # uwsgi.run()
    app.run(host="0.0.0.0", port=5050, debug=True)
