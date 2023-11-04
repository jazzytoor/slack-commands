import awsgi
from app import flask_app


def lambda_handler(event, context):
    return awsgi.response(flask_app, event, context)
