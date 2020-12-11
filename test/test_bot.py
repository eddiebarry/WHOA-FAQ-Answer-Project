import requests, pdb, os, json, random
from dotenv import load_dotenv
load_dotenv()

urls = [
    os.getenv("LOCAL_URL"),
    os.getenv("REMOTE_URL"),
]

urls = [
    # os.getenv("BOTPRESS_ENDPOINT")
    os.getenv("BOTPRESS_STAGING_ENDPOINT"),
]

conversations = [
    [
        ("Hi", "how can i help you today"),
        ("Ask Vaccine Questions","please type your query"),
        ("Do I need to pay for the hepatitis B vaccine?",
        "The hepatitis B vaccine is recommended and provided free to all children in BC as part of their routine childhood immunizations"),
        ("No","Would you like to ask another question"),
        ("No","I hope i was helpful"),
    ],
    [
        ("Hi", "how can i help you today"),
        ("Ask Vaccine Questions","please type your query"),
        ("I need help","What vaccine are you talking about"),
        ("please help me","Is there any additional information you could help us with"),
        ("I am lost","would you like to continue talking about the same question"),
        ("No","Would you like to ask another question"),
        ("No","I hope i was helpful"),
    ],
]

def test_conversation():
    for url in urls:
        user_id = random.randint(0, 100000000)
        converse_api_url = url + "/api/v1/bots/" + \
            os.getenv("BOT_ID") + "/converse/" + str(user_id)
        for text in conversations:
            replies = []
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