# Player Finder

This is a slack bot that gives you all information about a minecraft player who joined hackclubs minecraft server just with a slack mention, hackclubs minecraft server status, hccore api and api key status that as much as my creativity allowed

## Tech Stack

- Python
- uv
- HCCORE API
- slack_bolt
- mcstatus

---

# Usage

You can use it with 3 slash commands **/player lookup <@slack-mention>**, **/server-status** and **/api-health**

---

The **/player lookup <@slack-mention>** give you informations like **HC Minecraft Server Color**, **Minecraft Nickname**, **HC Minecraft Server Nickanme**, **UUID** and **NAMEMC Link**.

**example:** /player lookup @Ghost of NovaEntity

![image](https://cdn.hackclub.com/01a051bc-7857-7549-b15f-55e3d9b8b78c/image.png)

---

The **/server-status** gives you informations about hackclubs minecraft server like **Online players**, **Server Version** and **Ping**

![image](https://cdn.hackclub.com/01a051c0-33ae-7048-8fa3-b34918f738dc/image.png)

---

The **/api-health** gives you informations about hccore api and your hccore api key like **Status**, **API Version** and **Is API Key Authorized**

![image](https://cdn.hackclub.com/01a051b9-1e64-7c61-b431-c4551b5e185b/image.png)

**AND IF YOU WANT TO USE THIS DONT FORGET TO UPDATE ".env.example" AND RENAME IT AS ".env" !!!**

---

# Sum

I really enjoyed doing this project, i learned how to use requests, slack bolt for python (i already knew it in typescript) and the mcstatus library and i think i will keep doing slack bots with python from now on.
