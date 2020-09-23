import sys, os, lucene, json
import hashlib
sys.path.append('WHO-FAQ-Keyword-Engine')
sys.path.append('WHO-FAQ-Search-Engine')
sys.path.append('WHO-FAQ-Update-Engine')
sys.path.append('WHO-FAQ-Dialog-Manager')
sys.path.append('WHO-FAQ-Dialog-Manager/QNA')

import flask
from flask import request, jsonify
from collections import defaultdict 

from keyword_extractor import KeywordExtract
from search import SearchEngine
from query_generator import QueryGenerator
from index import IndexFiles
from org.apache.lucene.analysis.standard import StandardAnalyzer
# TODO : Fix naming
from QNA.common import preprocess, tokenize, porter_stemmer_instance
from QNA.question_asker import QuestionAsker


app = flask.Flask(__name__)
app.config["DEBUG"] = True
lucene.initVM(vmargs=['-Djava.awt.headless=true'])


# TODO : Document
# TODO : Make this function stateless
@app.route('/api/v2/qna', methods=['GET'])
def answer_question():
    """
    This api answers questions

    Inputs
    ------
    Expects a api call of the form : ""
    
    Query : String
        The string from which we need to extract keywords

    Outputs
    -------
    Json Object : 
        The form of the json object is as follows : -
    """
    global ID_KEYWORD_DICT
    global ID_QUERY_DICT
    global KEYWORD_EXTRACTOR
    global QUESTION_ASKER
    global QUERY_GEN
    global SEARCH_ENGINE
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()

    # If first time being sent, calculate a unique id
    query_string = request.args['query'].lower()\
        .replace("?","")\
        .replace("-","")\
        .replace("not relevant","")\
        .replace("none","")
    if request.args['user_id'] == "-1":
        unique_id = hashlib.sha512(query_string.encode()).hexdigest()
        ID_QUERY_DICT[unique_id] = query_string
    else:
        unique_id = request.args['user_id']
    
    # If question has already been answered allow new question to be asked
    if ID_QUERY_DICT[unique_id] == "-1":
        ID_QUERY_DICT[unique_id] = query_string
    else:
        # Add entire conversation to search engine
        ID_QUERY_DICT[unique_id] += query_string.lower()

    # Extract keywords on the basis of the user input
    boosting_tokens = KEYWORD_EXTRACTOR.parse_regex_query(\
        query_string.lower())
    
    import pdb
    pdb.set_trace()
    
    # Make a set of all fields which have had keywords detected
    all_token_keys = set(boosting_tokens.keys()).\
        union(ID_KEYWORD_DICT[unique_id].keys())
    
    # Create a combined dictinary of old keywords and new keywords
    new_boosting_dict = defaultdict(list)
    for key in all_token_keys:
        # Add all the tokens present in the current query
        if key in boosting_tokens.keys():
            new_boosting_dict[key].extend(boosting_tokens[key])

        # Add all the tokens present in past queries
        if key in ID_KEYWORD_DICT[unique_id].keys():
            new_boosting_dict[key].extend(ID_KEYWORD_DICT[unique_id][key])
    
    # Store the newly created keyword dictionary in global memory
    ID_KEYWORD_DICT[unique_id] = new_boosting_dict

    # Identify wether more questions need to be asked or not
    # TODO : Ask question only once
    should_search, resp_json = QUESTION_ASKER.process(\
        unique_id, new_boosting_dict,ID_QUERY_DICT[unique_id])
    
    query = None
    # If no more questions need to be asked, isolate the search results and return
    if should_search:
        query, synonyms = QUERY_GEN.build_query(ID_QUERY_DICT[unique_id], \
            ID_KEYWORD_DICT[unique_id], "OR_QUERY", field="Master_Question",\
            boost_val=2.0)
        hits = SEARCH_ENGINE.search(query, \
            query_string=ID_QUERY_DICT[unique_id], \
            query_field="Master_Question*", top_n=10)

        what_to_say = ""
        for doc in hits[:5]:
            what_to_say += "\noriginal question : " + doc[1] +  \
            "\nscore : "+str(doc[0]) + "\n" + "-"*20 + "\n"
        what_to_say += "The synonyms we extracted from the user question are :\n"
        for syn in synonyms:
            if syn != "":
                what_to_say += syn + "\n"
        
        resp_json["what_to_say"] = what_to_say

        # Reset unique id query to sentinel value
        ID_QUERY_DICT[unique_id] = "-1"
    
        # Logging
        original_stdout = sys.stdout 
        with open('log.txt', 'a') as f:
            sys.stdout = f # Change the standard output to the file we created.
            print('$'*80)
            print("unique id", unique_id)
            print("The user question is ", ID_QUERY_DICT[unique_id])
            print("The generated lucene query is ", query)
            print("The results of the search are ", hits)
            print('$'*80)
            sys.stdout = original_stdout

    return jsonify(resp_json)


@app.route('/api/v2/keyword_extract', methods=['GET'])
def return_keyword():
    """
    After the keyword engine is set up with a configuration file,
    this api extracts the keywords from the user query and returns them
    as a json object

    Inputs
    ------
    Expects a api call of the form : ""
    
    Query : String
        The string from which we need to extract keywords

    Outputs
    -------
    Json Object : 
        The form of the json object is as follows : -
            
    """
    global KEYWORD_EXTRACTOR

    # If first time being sent, calculate a unique id
    query_string = request.args['query'].replace("?","")

    # Extract keywords on the basis of the user input
    boosting_tokens = KEYWORD_EXTRACTOR.parse_regex_query(query_string)    
    
    # Logging
    original_stdout = sys.stdout 
    with open('keyword_log.txt', 'a') as f:
        sys.stdout = f # Change the standard output to the file we created.
        print('$'*80)
        print("The user query is ", query_string)
        print("The extracted tokens are ", boosting_tokens)
        print('$'*80)
        sys.stdout = original_stdout

    #TODO :  preprocess cleaned boosting tokens to line up with specified tokens
    return jsonify(boosting_tokens)

@app.route('/api/v2/index_json_array', methods=['PUT'])
def index_json_array():
    """
    This function takes a json array specified by the labelling web service 
    and add its to the search index

    Inputs
    ------
    Expects a api call of the form : ""
    
    jsonArray : Array of Json Objects
        This array consists of the json objects that we want to index
        The array is of the form :
            {
                "QA_Pairs":[
                    {
                        "Subject - Person": "Child",
                        "Subject 1 - Immunization": "Immunization General",
                        "Subject 2 - Vaccination / General": "",
                        "Who is writing this": "Parent"
                    },
                    {
                        "Subject 1 - Immunization": "Immunization Required",
                        "Subject 2 - Vaccination / General": "",
                        "Subject Sex": "Male",
                        "Vaccine": "Varicella (Chickenpox)",
                        "Who is writing this": "Unknown "
                    },
                    {
                        "Disease 1": "Chickenpox",
                        "Keyword": "Shingles vaccines",
                        "Subject - Person": "",
                        "Subject 1 - Immunization": "Immunization Required",
                        "Subject 2 - Vaccination / General": "Vaccine Cost",
                        "Who is writing this": "Adult"
                    }
                ]
            }

    Outputs
    -------
    Json Object : 
        The form of the json object is as follows : -

    """
    global INDEX

    # Adding the files to the array
    jsonArray - request.args['Json_Array']
    INDEX.index_json_array(jsonArray)

    # Logging
    original_stdout = sys.stdout 
    with open('json_array_log.txt', 'a') as f:
        sys.stdout = f # Change the standard output to the file we created.
        print('$'*80)
        print("The recieved json array is is : \n", jsonArray)
        print('$'*80)
        sys.stdout = original_stdout

    #TODO :  preprocess
    return jsonify(boosting_tokens)

@app.route('/')
def hello_world():
    return 'Hello, World! Bye world, Hi world'
        

if __name__ == '__main__':
    INDEX = IndexFiles("./VaccineIndex.Index",StandardAnalyzer())
    
    INDEX.indexFolder("./metrics/intermediate_results/json_folder_with_variations_1500")

    QUERY_GEN = QueryGenerator(StandardAnalyzer(),\
        synonym_config=[
            True, #use_wordnet
            True, #use_syblist
            "./WHO-FAQ-Search-Engine/synonym_expansion/synlist.txt" #synlist path
        ], debug=True)
    
    indexDir = INDEX.getIndexDir()
    SEARCH_ENGINE = SearchEngine(indexDir, rerank=True, debug=True)
    
    extractor_json_path = \
        "./WHO-FAQ-Keyword-Engine/test_excel_data/curated_keywords_1500.json"
    f = open(extractor_json_path,)
    jsonObj = json.load(f)
    KEYWORD_EXTRACTOR = KeywordExtract(jsonObj)
    
    ID_KEYWORD_DICT = defaultdict(dict)
    ID_QUERY_DICT = defaultdict(str)

    qa_config_path = "./WHO-FAQ-Dialog-Manager/QNA/question_asker_test_config.json"
    use_question_predicter_config = [
            False, #Use question predictor
            "./WHO-FAQ-Dialog-Manager/QNA/models.txt", #models path
            "./WHO-FAQ-Dialog-Manager/QNA/vectoriser.txt" #tokeniser path
        ]
    QUESTION_ASKER = QuestionAsker(qa_config_path, show_options=True, \
        qa_keyword_path = extractor_json_path,
        use_question_predicter_config=use_question_predicter_config)

    app.run(host='0.0.0.0', port = 5003)