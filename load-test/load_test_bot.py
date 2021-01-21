import time
from locust import HttpUser, task, between
import requests, pdb, os, json, random

# host=https://botpress-chitchat-project-interakt-staging.apps.prod.lxp.academy.who.int

conversations = [
    [
        ("Hi","may i know your name"),
        ("no", "we will not use your name how can i help you today"),
        ("Ask Vaccine Questions","please type your vaccination related question"),
        ("Do I need to pay for the hepatitis B vaccine?",
        "The hepatitis B vaccine is recommended and provided free to all children in BC as part of their routine childhood immunizations"),
        ("No","Would you like to ask another question"),
        ("No","I hope i was helpful"),
    ],
    [
        ("Hi", "may i know your name"),
        ("no", "we will not use your name how can i help you today"),
        ("Ask Vaccine Questions","please type your vaccination related question"),
        ("I need help","What topic is this most"),
        ("please help me", "What vaccine are you"),
        ("I am lost","For whom is this question"),
        ("save me !!!","Is there any additional information you"),
        ("none","Hi, I need to get a copy of my child record of immunization I hope the response answers your questions"),
        ("No","Would you like to ask another question"),
        ("No","I hope i was helpful"),
    ],
    [
        ("Hi","may i know your name"),
        ("emma", "emma nice to meet you how can i help you today"),
        ("Ask Vaccine Questions","please type your vaccination related question"),
        ("Do I need to pay for the hepatitis B vaccine?",
        "The hepatitis B vaccine is recommended and provided free to all children in BC as part of their routine childhood immunizations"),
        ("No","Would you like to ask another question"),
        ("No","I hope i was helpful"),
    ],
    [
        ("Hi", "may i know your name"),
        ("emma", "emma nice to meet you how can i help you today"),
        ("Ask Vaccine Questions","please type your vaccination related question"),
        ("I need help","What topic is this most"),
        ("please help me", "What vaccine are you"),
        ("I am lost","For whom is this question"),
        ("save me !!!","Is there any additional information you"),
        ("none","Hi, I need to get a copy of my child record of immunization I hope the response answers your questions"),
        ("No","Would you like to ask another question"),
        ("No","I hope i was helpful"),
    ],
    # Testing of no idea about this functionality
    [
        ("Hi", "may i know your name"),
        ("emma", "emma nice to meet you how can i help you today"),
        ("Ask Vaccine Questions","please type your vaccination related question"),
        ("I need directions to lisbon","What topic is this most related to ?"),
        ("none", "What vaccine are you talking about ?"),
        ("none","For whom is this question"),
        ("none","Is there any additional information you"),
        ("none","We currently do not have information about your query. We will update our bot"),
        ("No","Would you like to ask another question"),
        ("No","I hope i was helpful"),
    ],
    # Testing the name functionality
    [
        ("Hi", "may i know your name"),
        ("i am bernardo", "Okay bernardo nice to meet you"),
    ],
    [
        ("Hi", "may i know your name"),
        ("i am called bernardo", "Okay bernardo nice to meet you"),
    ],
    [
        ("Hi", "may i know your name"),
        ("my name is bernardo", "Okay bernardo nice to meet you"),
    ],
    [
        ("Hi", "may i know your name"),
        ("Hi, my name is bernardo", "Okay bernardo nice to meet you"),
    ],
    [
        ("Hi", "may i know your name"),
        ("hi my name is bernardo", "Okay bernardo nice to meet you"),
    ],
    [
        ("Hi", "may i know your name"),
        ("bernardo", "Okay bernardo nice to meet you"),
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