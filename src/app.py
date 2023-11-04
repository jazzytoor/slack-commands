from flask import Flask, request
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

flask_app = Flask(__name__)
bolt_app = App()
handler = SlackRequestHandler(bolt_app)


@bolt_app.middleware
def log_request(logger, body, next):
    logger.debug(body)
    return next()


@bolt_app.event("app_mention")
def event_test(body, say, logger):
    logger.info(body)
    say("")


# @bolt_app.command("/<>")
# def command(ack, body, respond):
#     ack()
#     respond("<>")


@flask_app.route("/commands", methods=["POST"])
def slack_events():
    return handler.handle(request)
