from app import appF, db
from app.models import User


@appF.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}


if __name__ == "__main__":
    appF.run()
