from flask import render_template
from app import appF, db
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

@appF.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@appF.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


if not appF.debug:
    if appF.config['MAIL_SERVER']:
        auth = None
        if appF.config['MAIL_USERNAME'] or appF.config['MAIL_PASSWORD']:
            auth = (appF.config['MAIL_USERNAME'], appF.config['MAIL_PASSWORD'])
        secure = None
        if appF.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(appF.config['MAIL_SERVER'], appF.config['MAIL_PORT']),
            fromaddr='no-reply@' + appF.config['MAIL_SERVER'],
            toaddrs=appF.config['ADMINS'], subject='Service Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        appF.logger.addHandler(mail_handler)

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/gss_service.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    appF.logger.addHandler(file_handler)

    appF.logger.setLevel(logging.INFO)
    appF.logger.info('Service startup')