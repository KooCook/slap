from slap_flask.database import db


def load_models(app):
    with app.app_context():
        db.database.create_all()
