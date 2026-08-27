import os
from dotenv import load_dotenv
load_dotenv()

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import requests
import re

app = App(token=os.getenv("SLACK_BOT_TOKEN"))

@app.command("/player")
def main_command(ack, command, respond, say):
    ack()

    slack_id_re = re.search(r"([UW][A-Z0-9]+)", command["text"])

    if(slack_id_re):
        slack_id = slack_id_re.group(1)
    else:
        respond("bro pls tag some not plain text it :bruhcat:")
        return

    headers = {
        "Authorization": f"Bearer {os.getenv("HCCORE_API_KEY")}"
    }

    response = requests.get(f"https://api.mc.hackclub.com/player?slack={slack_id}", headers=headers)
    hc_mc_server_infos = response.json()
    if "error" in hc_mc_server_infos:
        respond(hc_mc_server_infos["message"], response_type = "ephemral")
        return

    mojang_api_response = requests.get(f"https://api.minecraftservices.com/minecraft/profile/lookup/{hc_mc_server_infos[0]["uuid"]}")
    mojang_api_results = mojang_api_response.json()
    respond(f"""*HC Minecraft Server Nickname:* {hc_mc_server_infos[0]["nick"]["name"]}
*HC Minecraft Server Color:* {hc_mc_server_infos[0]["nick"]["color"]}
*Minecraft Name:* {mojang_api_results["name"]}
*UUID:* {hc_mc_server_infos[0]["uuid"]}
<https://namemc.com/profile/{hc_mc_server_infos[0]["uuid"]}|*NAMEMC*>""")


@app.event("app_mention")
def app_mention(respond, body):
    respond("Hiiii :hii: do you need smth?")

if __name__ == "__main__":
    handler = SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN"))
    handler.start()