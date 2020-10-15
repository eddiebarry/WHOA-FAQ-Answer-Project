import pandas as pd
import sys, os, lucene, json
import hashlib
sys.path.append('../WHO-FAQ-Keyword-Engine')
sys.path.append('../WHO-FAQ-Search-Engine')
sys.path.append('../WHO-FAQ-Update-Engine')
sys.path.append('../WHO-FAQ-Dialog-Manager')

from index import IndexFiles
from org.apache.lucene.analysis.standard import StandardAnalyzer

# Add all the newly created jsons to the index

if __name__ == "__main__":
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    # create new files needed
    indexDir = "./intermediate_results/json_folder_with_variations_1500/"
    oneVariationRemovedDataStore = "./intermediate_results/json_folder_with_no_variations/"
    
    new_data = []
    for filename in sorted(os.listdir(indexDir)):
        if not filename.endswith('.json'):
            continue

        jsonpath = os.path.join(indexDir,filename)
        if os.path.isfile(jsonpath):
            try:
                print("analyszing", filename)
                f = open(jsonpath,)
                jsonObj = json.load(f)

                user_question = jsonObj.pop('Master Question variation 2')
                
                # Debugging
                jsonObj.pop('Master Question variation 0')
                jsonObj.pop('Master Question variation 1')
                
                master_question = jsonObj['Master Question']

                new_data.append([user_question, master_question])

                json_name = hashlib.sha512(\
                        jsonObj['Master Question'].encode()\
                    ).hexdigest()
                json_file_name = os.path.join(\
                    oneVariationRemovedDataStore, json_name + ".json")

                print("writing", json_file_name)
                with open(json_file_name , 'w') as json_file:
                    json.dump(jsonObj, json_file,\
                        indent = 4, sort_keys=True)

            except Exception as e:
                    print( "Failed in reading / writing json:", e)
    
    new_df = pd.DataFrame(new_data, \
        columns = ["User Question", "Master Question"])
    
    master_qa_path = "./intermediate_results/qa_user_list_1500.csv"
    new_df.to_csv(master_qa_path)

    index_with_variations_dir = \
        "./intermediate_results/VariationIndex1500.Index"
    
    Index = IndexFiles(index_with_variations_dir,StandardAnalyzer())
    Index.indexFolder(oneVariationRemovedDataStore)
    Index.print_all_contents()