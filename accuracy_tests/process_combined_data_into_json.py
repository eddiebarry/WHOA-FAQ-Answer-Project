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

f = open('/usr/src/WHOA-FAQ-Answer-Project/accuracy_tests/emoji_qna_combined.json','r')
question = json.load(f)
f.close()


final_dir = "/usr/src/WHOA-FAQ-Answer-Project/accuracy_tests/intermediate_results/emoji_data_chitchat_combined"

for x in question:

    obj = {
        "answer": question[x],
        "answer_formatted": question[x],
        "question": x,
        "question_variation_0": x,
        "question_variation_1": x,
        "question_variation_2": x,
        "type": "chitchat"
    }
    json_name = hashlib.sha512(x.encode()).hexdigest()

    json_file_name = os.path.join(final_dir,json_name+".json")

    with open(json_file_name , 'w') as json_file:
        json.dump(obj, json_file, indent = 4, sort_keys=True)
