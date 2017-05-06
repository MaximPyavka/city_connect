from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from city_connect.models.user import User
from datetime import datetime
from city_connect.app import app, db

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def create_admin():
    """Creates the admin user"""
    db.session.add(User(
        email = "ad@min.com",
        password = "admin",
        admin = True,
        confirmed = True,
        confirmed_on = datetime.now())
    )
    db.session.commit()

@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()


if __name__ == '__main__':
    manager.run()
