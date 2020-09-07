import sys, os, lucene, json
import hashlib
sys.path.append('../WHO-FAQ-Keyword-Engine')
sys.path.append('../WHO-FAQ-Search-Engine')
sys.path.append('../WHO-FAQ-Update-Engine')
sys.path.append('../WHO-FAQ-Dialog-Manager')

from variation_generation.variation_generator import VariationGenerator

# Go through all the files, create a csv of question and 
# the corresponding master question and the new json which must be indexed

def get_json_obj_with_variations(jsonObj, \
    fields_to_expand, variation_generator):
    # import pdb
    # pdb.set_trace()
    new_json_obj = {}
    for x in jsonObj.keys():
        if x.replace(" ","_") in fields_to_expand:
            variations = variation_generator.get_variations(jsonObj[x])

            for idx, variation in enumerate(variations):
                field_name = x + " variation "+str(idx)
                new_json_obj[field_name] = variation

        new_json_obj[x]=jsonObj[x]
    
    return new_json_obj

if __name__ == "__main__":
    indexDir = "./test_data/json_folder_data"
    newIndexStore = "./intermediate_results/json_folder_with_variations/"
    variation_generation_model_weights = "../WHO-FAQ-Search-Engine/variation_generation/variation_generator_model_weights/model.ckpt-1004000"
    variation_generator = VariationGenerator(\
        path=variation_generation_model_weights)

    fields_to_expand = ["Master_Question"]

    for filename in sorted(os.listdir(indexDir)):
        if not filename.endswith('.json'):
            continue

        jsonpath = os.path.join(indexDir,filename)
        if os.path.isfile(jsonpath):
            try:
                print("analyszing", filename)
                f = open(jsonpath,)
                jsonObj = json.load(f)

                new_json_obj = get_json_obj_with_variations(\
                    jsonObj, fields_to_expand, variation_generator)

                json_name = hashlib.sha512(\
                        new_json_obj['Master Question'].encode()\
                    ).hexdigest()
                json_file_name = os.path.join(\
                    newIndexStore, json_name + ".json")

                print("writing", json_file_name)
                with open(json_file_name , 'w') as json_file:
                    json.dump(new_json_obj, json_file,\
                        indent = 4, sort_keys=True)

            except Exception as e:
                print( "Failed in reading / writing json:", e)