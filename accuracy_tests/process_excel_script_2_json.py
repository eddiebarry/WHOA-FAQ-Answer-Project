"""
Converting the LXP-related Q&A pairs in the Excel script created by designers
to a JSON file containing all such LXP-related Q&A pairs, so that they can be
added to the search index.
"""


from hashlib import sha512
from json import dump as json_dump, load as json_load
from os import getcwd
from os.path import join as os_join
from typing import Callable, List

from openpyxl import load_workbook


# defininf category keywords:

def clean_category_keywords(original: List[str]) -> List[str]:
    """
    Remove emojis and other special characters, split extreme
    whitespaces/newlines and turn into lowercase each string of the list.
    """
    clean = []
    for keyword in original:
        keyword = keyword.strip()
        keyword = ''.join([i if ord(i) < 128 else '' for i in keyword])
        keyword = keyword.strip()
        keyword = keyword.lower()
        clean.append(keyword)
    return clean

types_filename = os_join(
    getcwd(),
    "data",
    "unique_keywords",
    "4_0_unique_keywords.json"
)
with open(types_filename, 'r', encoding='utf-8') as file:
    keyword_categories = json_load(file)["type"]

# cleaning categorie keyword names to the bare minimum for better matching:
KEYWORD_CATEGORIES = clean_category_keywords(keyword_categories)

DEFAULT_KEYWORD_CATEGORY = "something else"  # "None"


def excel_2_json_wrapper() -> Callable:
    """
    Wrapper setting the function docstring as the module docstring.
    """

    def excel_2_json_inner(dataset_file_path: str, script_path: str) -> None:
        """
        Docstring overwritten by module docstring.
        """

        # loading the script:
        workbook = load_workbook(filename=script_path)

        # reading the script while writing the resulting JSON objects of Q&A
        # pairs:

        sheet = workbook['LXP']

        # iterating through row cells of the first column - the first row
        # cell contains a header:
        for question_variants, answer, keywords in\
                zip(sheet['A'][1:], sheet['B'][1:], sheet['C'][1:]):

            # skipping empty cells:
            if question_variants.value is None or answer.value is None or\
                    keywords.value is None:
                continue

            # removing evantual initial/final whitespaces:
            answer = answer.value.strip()

            # preprocessing keywords coherently with references:
            keywords = keywords.value
            keywords = keywords.split(",")
            keywords = clean_category_keywords(keywords)

            # extracting questions in the current row cell - i.e. variations
            # of the same base question:
            for question in question_variants.value.split('/'):

                # removing evantual initial/final whitespaces:
                question = question.strip()

                # turning the question variation and the respective answer to
                # a JSON dictionary to be saved:
                object_dict = {
                    "answer": answer,
                    "answer_formatted": answer,
                    "question": question,
                    "question_variation_0": question,
                    "question_variation_1": question,
                    "question_variation_2": question,
                }

                # associating the category extracted from the keywords as type
                # or, in case none exists, a default category as type - when
                # multiple categories are present among the keyworks, the
                # script is ambiguously defined, so a random one is picked:
                if keywords != "" and type(keywords) == list:
                    for keyword in keywords:
                        if keyword in KEYWORD_CATEGORIES:
                            object_dict['type'] = keyword
                            break
                if 'type' not in object_dict:
                    object_dict['type'] = DEFAULT_KEYWORD_CATEGORY


                json_name = sha512(question.encode()).hexdigest()
                json_file_name = os_join(
                    getcwd(),  # /usr/src/WHOA-FAQ-Answer-Project
                    "accuracy_tests",
                    "intermediate_results",
                    "script_data_directly_from_designers",
                    json_name + ".json"
                )
                
                # saving the JSON object as a JSON file:
                with open(json_file_name , 'w') as file:
                    json_dump(object_dict, file, indent=4, sort_keys=True)

    # adding the docstring:
    excel_2_json_inner.__doc__ = __doc__

    return excel_2_json_inner


excel_2_json = excel_2_json_wrapper()


if __name__ == "__main__":

    OUTPUT_FILE_PATH = os_join(
        getcwd(),
        "dataset",
        "LXP_related",
        "directly_from_our_script.json"
    )
    SCRIPT_PATH = os_join(
        getcwd(),  # /usr/src/WHOA-FAQ-Answer-Project
        "accuracy_tests",
        "Script-updated-database_updated_date_07-05-2021_time_11-36-18.xlsx"
    )

    excel_2_json(
        dataset_file_path=OUTPUT_FILE_PATH,
        script_path=SCRIPT_PATH
    )

# import pandas as pd
# import json
# import hashlib
# import re
# import os

# xl = pd.read_csv("/usr/src/WHOA-FAQ-Answer-Project/accuracy_tests/emoji_qa_modified.csv")

# def return_type(string):
#     # pos_type = ["agenda","learning","course discovery","profile"]
#     pos_type = KEYWORDS
#     type_detected = ""
#     for x in pos_type:
#         if x in string:
#             type_detected += " " + x
    
#     if type_detected == "":
#         type_detected = "profile"
#         # print(string, "failed")

#     return type_detected.strip()

# for idx, x in xl.iterrows():
#     # object_dict = dict(x)

#     for question in x['Question'].split('/'):
#         if type(x['Edited Answer']) != str:
#             break

#         question = question.strip()

        # object_dict = {
        #     "answer": x['Edited Answer'],
        #     "answer_formatted": x['Edited Answer'],
        #     "question": question,
        #     "question_variation_0": question,
        #     "question_variation_1": question,
        #     "question_variation_2": question,
        # }
        
        # object_dict['type'] = return_type(question + " " + x['Edited Answer'])

        # json_name = hashlib.sha512(question.encode()).hexdigest()
        # json_file_name = os_join(
        #     getcwd(),  # corresponding to /usr/src/WHOA-FAQ-Answer-Project
        #     "accuracy_tests",
        #     "intermediate_results",
        #     "script_data_directly_from_designers",
        #     json_name + ".json"
        # )
        
        # with open(json_file_name , 'w') as json_file:
        #     json.dump(object_dict, json_file, indent = 4, sort_keys=True)

# dir_ = "/usr/src/WHOA-FAQ-Answer-Project/accuracy_tests/intermediate_results/vla_data_formatted"
# final_dir = "/usr/src/WHOA-FAQ-Answer-Project/accuracy_tests/intermediate_results/emoji_data_improved_formatted"
# for x in os.listdir(dir_):
#     if x.endswith(".json"):
#         full_path = os.path.join(dir_,x)
#         f = open(full_path,'r')
#         question = json.load(f)
#         f.close()

#         if question['type']=="learning":
#             question['answer'] = "Try clicking on the “My Learning” tab on the left side of the navigation window to access your learning content 🎓."
#             question['answer_formatted'] = "Try clicking on the “My Learning” tab on the left side of the navigation window to access your learning content 🎓."
        
#         if question['type']=="profile":
#             if "password" in question['question']:
#                 question['answer'] = "You can change your Password in the Profile Section  👉 Account Preferences under Signing & Security ⚙️. Make sure you the password includes special characters (such as & and $) to make it more secure 🔒"
#                 question['answer_formatted'] = "You can change your Password in the Profile Section  👉 Account Preferences under Signing & Security ⚙️. Make sure you the password includes special characters (such as & and $) to make it more secure 🔒"

#             else:
#                 question['answer'] = "Right next to your name on the top left sidebar you will find a default avatar picture 🏞 . Click on that avatar to edit your profile! ⚙️"
#                 question['answer_formatted'] = "Right next to your name on the top left sidebar you will find a default avatar picture 🏞 . Click on that avatar to edit your profile! ⚙️"
               
#         if question['type']=="agenda":
#             question['answer'] = "I promise it’s coming. 💫We are still working on your calendar. 🗓 It will be available in the next release. 🎓"
#             question['answer_formatted'] = "I promise it’s coming. 💫We are still working on your calendar. 🗓 It will be available in the next release. 🎓"

#         if question['type']=="course discovery":
#             question['answer'] = "Feeling adventurous? 🔍Try clicking on “Discover Learning” on the top of your home screen.  We regularly update learning programmes 📚and publish new content there 😊."
#             question['answer_formatted'] = "Feeling adventurous? 🔍Try clicking on “Discover Learning” on the top of your home screen.  We regularly update learning programmes 📚and publish new content there 😊."


#         json_file_name = os.path.join(final_dir,x)
#         with open(json_file_name , 'w') as json_file:
#             json.dump(question, json_file, indent = 4, sort_keys=True)
