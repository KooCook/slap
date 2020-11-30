from flask_sqlalchemy import SQLAlchemy
from slap_flask.settings import DATABASE_URI


class Database:
    def __init__(self):
        self.database = SQLAlchemy()

    @property
    def base(self):
        return self.database

    def connect_app(self, app):
        """Link the core application to the database."""
        app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
        self.database.pool_size = 80
        self.database.init_app(app)
        app.app_context().push()
        with app.app_context():
            self.database.create_all()
            return app


db = Database()
