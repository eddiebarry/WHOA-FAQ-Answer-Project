import requests, pdb, os, json, random
from dotenv import load_dotenv
load_dotenv()

urls = [
    os.getenv("BOTPRESS_ENDPOINT"),
    # os.getenv("BOTPRESS_STAGING_ENDPOINT"),
]

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
]

def test_conversation():
    for url in urls:
        print("testing ", url)
        
        for text in conversations:
            replies = []
            
            user_id = random.randint(0, 100000000)
            converse_api_url = url + "/api/v1/bots/" + \
                os.getenv("BOT_ID") + "/converse/" + str(user_id)

            for text_snippet, fixed_reply in text:
                data = {
                    "type": "text",
                    "text": text_snippet
                }

                r = requests.post(converse_api_url, data=data)
                data = r.json()

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
            #     print("good")
            # print("$DONE")

# test_conversation()