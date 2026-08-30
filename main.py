import os
from dotenv import load_dotenv
load_dotenv()

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from mcstatus import JavaServer
import requests
import re

app = App(token=os.getenv("SLACK_BOT_TOKEN"))

headers = {
        "Authorization": f"Bearer {os.getenv('HCCORE_API_KEY')}"
    }


@app.command("/player")
def player(ack, command, respond):
    ack()

    slack_id_re = re.search(r"([UW][A-Z0-9]+)", command["text"])

    if(slack_id_re):
        slack_id = slack_id_re.group(1)
    else:
        respond("bro pls tag someone not plain text it :bruhcat:", response_type="ephemeral")
        return

    hccore_api_response = requests.get(f"https://api.mc.hackclub.com/player?slack={slack_id}", headers=headers)
    hc_mc_server_infos = hccore_api_response.json()

    if "error" in hc_mc_server_infos:
        respond(hc_mc_server_infos["message"], response_type = "ephemeral")
        return
        
    mojang_api_response = requests.get(f"https://api.minecraftservices.com/minecraft/profile/lookup/{hc_mc_server_infos[0]['uuid']}")
    mojang_api_results = mojang_api_response.json()

    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "USER MINECRAFT INFO",
                "emoji": True
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
                    "text": f"*HC Minecraft Server Color: * {hc_mc_server_infos[0]["nick"]["color"]}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*HC Minecraft Server Nickname: * {hc_mc_server_infos[0]["nick"]["name"]}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Minecraft Nickname: * {mojang_api_results["name"]}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*UUID: * {hc_mc_server_infos[0]["uuid"]}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"<https://namemc.com/profile/{hc_mc_server_infos[0]['uuid']}|NAMEMC :mc:>"
                }
            ]
        }
    ]

    """ blocks = [
        {
            "type": "markdown",
            "text": "# USER MINECRAFT INFO\n\n---\n\n "
        },
        {
            "type": "rich_text",
            "elements": [
                {
                    "type": "rich_text_section",
                    "elements": [
                        {
                            "type": "text",
                            "text": "HC Minecraft Server Color: ",
                            "styles": {
                                "bold": True,
                                "italic": True
                            }
                        },
                        {
                            "type": "text",
                            "text": hc_mc_server_infos[0]["nick"]["color"]
                        },
                        {
                            "type": "text",
                            "text": "\nHC Minecraft Server Nickname: ",
                            "styles": {
                                "bold": True,
                                "italic": True
                            }
                        },
                        {
                            "type": "text",
                            "text": hc_mc_server_infos[0]["nick"]["name"]
                        },
                        {
                            "type": "text",
                            "text": "\nMinecraft Nickname: ",
                            "styles": {
                                "bold": True,
                                "italic": True
                            }
                        },
                        {
                            "type": "text",
                            "text": mojang_api_results["name"]
                        },
                        {
                            "type": "text",
                            "text": "\nUUID: ",
                            "styles": {
                                "bold": True,
                                "italic": True
                            }
                        },
                        {
                            "type": "text",
                            "text": hc_mc_server_infos[0]["uuid"]
                        },
                        {
                            "type": "text",
                            "text": f"\n[NAMEMC](https://namemc.com/profile/{hc_mc_server_infos[0]['uuid']}) :mc:"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"<https://namemc.com/profiles/{hc_mc_server_infos[0]['uuid']}|NAMEMC :mc:>"
                        }
                    ]
                }
            ]
        }

    ] """

    respond(blocks=blocks, response_type="in_channel")
    return

@app.command("/server-status")
def server(ack, respond):
    ack()

    server = JavaServer.lookup("mc.hackclub.com")
    server_status = server.status()

    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "HC MINECRAFT SERVER STATUS",
                "emoji": True,
            },
        },
        {
            "type": "divider",
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text" : f"*Online Players: * {server_status.players.online}"
                },
                {
                    "type":"mrkdwn",
                    "text": f"*Ping: * {round(server_status.latency)}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Version: * {server_status.version.name}"
                }
            ]
        }
    ]

    respond(blocks=blocks, response_type="in_channel")

@app.command("/api-health")
def api_health(ack, respond):
    ack()

    hccore_api_response = requests.get("https://api.mc.hackclub.com/health", headers=headers)
    hccore_api_health = hccore_api_response.json()

    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "HCCORE API HEALTH",
                "emoji": True
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
                    "text": f"*Status: * {hccore_api_health["status"]}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Version: * {hccore_api_health["version"]}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Is API Key Authorized? : * {hccore_api_health["authorized"]}"
                }
            ]
        }
    ]


    respond(blocks=blocks, response_type="in_channel")
    return

@app.event("app_mention")
def app_mention(say, body):
    say("Hiiii :hii: do you need smth?")

if __name__ == "__main__":
    handler = SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN"))
    handler.start()