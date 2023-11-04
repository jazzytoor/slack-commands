from flask import Flask, request
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
import requests
import logging

flask_app = Flask(__name__)
bolt_app = App()
handler = SlackRequestHandler(bolt_app)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


@bolt_app.event("app_mention")
def event_test(body, say, logger):
    logger.debug(body)

    say("Hey! How can I help? :thinking_face:")


@bolt_app.command("/motivate")
def motivate_command(ack, respond):
    ack()

    quote = requests.get("https://zenquotes.io/api/today")
    if quote.status_code == 200:
        respond(f"*{quote.json()[0]['q']}*")
    else:
        respond("No quote! :cry:")


@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)
