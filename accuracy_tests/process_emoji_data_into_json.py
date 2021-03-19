import pandas as pd
import json
import hashlib
import re
import os
import pdb

"""
This file processes the data given by the vaccine team into json objects that 
we can add to the search index
"""

xl = pd.read_csv("/usr/src/WHOA-FAQ-Answer-Project/accuracy_tests/emoji_qa_modified.csv")

def return_type(string):
    pos_type = ["agenda","learning","course discovery","profile"]
    type_detected = ""
    for x in pos_type:
        if x in string:
            type_detected += " " + x
    
    if type_detected == "":
        type_detected = "profile"
        # print(string, "failed")

    return type_detected.strip()

for idx,x in xl.iterrows():
    # object_dict = dict(x)

    # pdb.set_trace()
    # break
    for question in x['Question'].split('/'):
        # pdb.set_trace()
        if type(x['Edited Answer']) != str:
            break

        question = question.strip()
        object_dict = {
            "answer": x['Edited Answer'],
            "answer_formatted": x['Edited Answer'],
            "question": question,
            "question_variation_0": question,
            "question_variation_1": question,
            "question_variation_2": question,
        }
        
        # try:
        object_dict['type'] = return_type(question + " " + x['Edited Answer'])
        # except:
        #     pdb.set_trace()

        json_name = hashlib.sha512(question.encode()).hexdigest()
        json_file_name = "/usr/src/WHOA-FAQ-Answer-Project/accuracy_tests/intermediate_results/emoji_data_improved_formatted/" + json_name+".json"
        
        with open(json_file_name , 'w') as json_file:
            json.dump(object_dict, json_file, indent = 4, sort_keys=True)

dir_ = "/usr/src/WHOA-FAQ-Answer-Project/accuracy_tests/intermediate_results/vla_data_formatted"
final_dir = "/usr/src/WHOA-FAQ-Answer-Project/accuracy_tests/intermediate_results/emoji_data_improved_formatted"
for x in os.listdir(dir_):
    if x.endswith(".json"):
        full_path = os.path.join(dir_,x)
        f = open(full_path,'r')
        question = json.load(f)
        f.close()

        if question['type']=="learning":
            question['answer'] = "Try clicking on the “My Learning” tab on the left side of the navigation window to access your learning content 🎓."
            question['answer_formatted'] = "Try clicking on the “My Learning” tab on the left side of the navigation window to access your learning content 🎓."
        
        if question['type']=="profile":
            if "password" in question['question']:
                question['answer'] = "You can change your Password in the Profile Section  👉 Account Preferences under Signing & Security ⚙️. Make sure you the password includes special characters (such as & and $) to make it more secure 🔒"
                question['answer_formatted'] = "You can change your Password in the Profile Section  👉 Account Preferences under Signing & Security ⚙️. Make sure you the password includes special characters (such as & and $) to make it more secure 🔒"

            else:
                question['answer'] = "Right next to your name on the top left sidebar you will find a default avatar picture 🏞 . Click on that avatar to edit your profile! ⚙️"
                question['answer_formatted'] = "Right next to your name on the top left sidebar you will find a default avatar picture 🏞 . Click on that avatar to edit your profile! ⚙️"
               
        if question['type']=="agenda":
            question['answer'] = "I promise it’s coming. 💫We are still working on your calendar. 🗓 It will be available in the next release. 🎓"
            question['answer_formatted'] = "I promise it’s coming. 💫We are still working on your calendar. 🗓 It will be available in the next release. 🎓"

        if question['type']=="course discovery":
            question['answer'] = "Feeling adventurous? 🔍Try clicking on “Discover Learning” on the top of your home screen.  We regularly update learning programmes 📚and publish new content there 😊."
            question['answer_formatted'] = "Feeling adventurous? 🔍Try clicking on “Discover Learning” on the top of your home screen.  We regularly update learning programmes 📚and publish new content there 😊."


        json_file_name = os.path.join(final_dir,x)
        with open(json_file_name , 'w') as json_file:
            json.dump(question, json_file, indent = 4, sort_keys=True)
