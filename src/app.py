from flask import Flask, request
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from helpers import aws
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


@bolt_app.command("/aws-get-resources")
def aws_get_resources(ack, body, client):
    ack()
    user = body["user_id"]

    logger.debug(body)

    regions = aws.get_all_regions()

    client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            "title": {
                "type": "plain_text",
                "text": "AWS Resources Manager",
                "emoji": True
            },
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Hi <@{user}>!*"
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "block_id": "region",
                    "text": {
                        "type": "mrkdwn",
                        "text": ":world_map: *List of regions*\nChoose where you want list the resources from"
                    },
                    "accessory": {
                        "type": "static_select",
                        "action_id": "region",
                        "options": [
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": region,
                                    "emoji": True
                                },
                                "value": region
                            } for region in regions
                        ]
                    }
                }
            ]
        }
    )


@bolt_app.action("region")
def handle_region(ack, body, action, client):
    ack()
    user = body["user"]["id"]
    region = action["selected_option"]["value"]

    client.views_update(
        view_id=body["view"]["id"],
        hash=body["view"]["hash"],
        view={
            "type": "modal",
            "title": {
                "type": "plain_text",
                "text": "AWS Resources Manager",
                "emoji": True
            },
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Hi <@{user}>!*"
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f":world_map: *Region*: {region}"
                        }
                    ]
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": ":hammer: *List of services*\nChoose which service you want to list for"
                    },
                    "accessory": {
                        "type": "static_select",
                        "action_id": "service",
                        "options": [
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "s3",
                                    "emoji": True
                                },
                                "value": f"s3|{region}"
                            }
                        ]
                    }
                }
            ]
        }
    )


@bolt_app.action("service")
def handle_service(ack, body, action, client):
    ack()
    service = action["selected_option"]["value"].split("|")[0]
    region = action["selected_option"]["value"].split("|")[1]
    resources = aws.get_tagged_resources(region, service)

    client.views_update(
        view_id=body["view"]["id"],
        hash=body["view"]["hash"],
        view={
            "type": "modal",
            "title": {
                "type": "plain_text",
                "text": "AWS Resources Manager",
                "emoji": True
            },
            "blocks": [
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": ":cloud: *Resources*:"
                        }
                    ]
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": resource
                        } for resource in resources
                    ] if resources else [
                        {
                            "type": "mrkdwn",
                            "text": "No resources found"
                        }
                    ]
                }
            ]
        }
    )


@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)
