import json, os


base_dir = "./intermediate_results/emoji_data_improved_formatted"

questions = {}
questions['data'] = []

for x in os.listdir(base_dir):
    if x.endswith(".json"):
        new_list = []
        filename = os.path.join(base_dir,x)
        f = open(filename,)
        jsonObj = json.load(f)
        f.close()
        new_obj = {
            "type":"Text",
            "value":jsonObj['question']
        }
        new_list.append(new_obj)

        questions['data'].append(new_list)

json_file_name = "./chatito.json"
with open(json_file_name , 'w') as json_file:
    json.dump(questions, json_file, sort_keys=True)