import time
from locust import HttpUser, task, between
import requests, pdb, os, json, random

# host=http://ec2-52-212-213-246.eu-west-1.compute.amazonaws.com:3000

conversations = [
    [
        ("Hi","Virtual learning assistant"),
        ("Ask Questions about LXP", "type in your LXP related question"),
        ("tell me my agenda","any additional information you could help us with ?"),
        ("none","Could you show me where I can access my agenda"),
        ("Yes","Please ask another question"),
        ("Could you show me where I can access my agenda","Your calendar will be available in the next release of the LXP."),
        ("No","you like to provide feedback"),
        ("No","I hope i was helpful. Have a great day !!!")
    ],
]


class QuickstartUser(HttpUser):
    wait_time = between(4, 10)

    @task(1)
    def talk_to_bot(self):
        user_id = random.randint(0, 100000000)
        converse_api_url = "/api/v1/bots/" + \
                os.getenv("BOT_ID") + "/converse/" + str(user_id)
        text = conversations[user_id%len(conversations)]
        for text_snippet, fixed_reply in text:
            data = {
                "type": "text",
                "text": text_snippet
            }

            r = self.client.post(converse_api_url, data=data)

            # pdb.set_trace()
            data = r.json()
            print(data.keys())

            reply_text = ""
            for snippets in data["responses"]:
                if snippets["type"]=="text":
                    reply_text += snippets["text"]
                if snippets["type"]=="custom" \
                    and snippets["component"]=="QuickReplies":
                    if "wrapped" in snippets.keys() and \
                        "text" in snippets["wrapped"].keys():
                        reply_text += snippets["wrapped"]["text"]
            
            test = reply_text.lower()

            for x in fixed_reply.lower().split(" "):
                assert x in test, reply_text + '*'*80 + x