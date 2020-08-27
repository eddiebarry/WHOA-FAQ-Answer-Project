import sys, os, lucene, json
import hashlib
sys.path.append('WHO-FAQ-Keyword-Engine')
sys.path.append('WHO-FAQ-Search-Engine')
sys.path.append('WHO-FAQ-Update-Engine')
sys.path.append('WHO-FAQ-Dialog-Manager')

import flask
from flask import request, jsonify
from collections import defaultdict 

from keyword_extractor import KeywordExtract
from search import SearchEngine
from query_generator import QueryGenerator
from index import IndexFiles
from org.apache.lucene.analysis.standard import StandardAnalyzer
# TODO : Fix naming
from QNA.question_asker import QuestionAsker


app = flask.Flask(__name__)
app.config["DEBUG"] = True
lucene.initVM(vmargs=['-Djava.awt.headless=true'])


# TODO : Document
# defines what kind of query we are serving
    # qna / location finding / connecting to human
@app.route('/api/v2/qna_test', methods=['GET'])
def answer_question_test():
    global num_encountered
    # Save a reference to the original standard output
    original_stdout = sys.stdout 
    with open('log.txt', 'a') as f:
        sys.stdout = f # Change the standard output to the file we created.
        print(request.args)
        print(request.args['user_id'])
        sys.stdout = original_stdout

    if request.args['user_id'] == "100200":
        num_encountered += 1
        print(num_encountered)
    
    if num_encountered <2:
        resp_json = {
            "ask_more_question": True,
            "what_to_say": "what disease are you talking about ?",
            "user_id": "100200",
        }
    else:
        resp_json = {
            "ask_more_question": False,
            "what_to_say": "what disease are you talking about ?",
            "user_id": "100200",
        }

    return jsonify(resp_json)

    # request will have user query and sentinel value

    # process the query and send the closest question


# defines what kind of query we are serving
    # qna / location finding / connecting to human
@app.route('/api/v2/qna', methods=['GET'])
def answer_question():
    global ID_KEYWORD_DICT
    global ID_QUERY_DICT
    global KEYWORD_EXTRACTOR
    global QUESTION_ASKER
    global QUERY_GEN
    global SEARCH_ENGINE
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()

    # If first time being sent, calculate a unique id
    query_string = request.args['query'].replace("?","")
    if request.args['user_id'] == "-1":
        unique_id = hashlib.sha512(query_string.encode()).hexdigest()
        ID_QUERY_DICT[unique_id] = query_string
    else:
        unique_id = request.args['user_id']
  
    # Extract keywords on the basis of the user input
    boosting_tokens = KEYWORD_EXTRACTOR.parse_regex_query(query_string)
    
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
        unique_id, new_boosting_dict)
    
    query = None
    # If no more questions need to be asked, isolate the search results and return
    if should_search:
        query = QUERY_GEN.build_query(ID_QUERY_DICT[unique_id], \
            ID_KEYWORD_DICT[unique_id], "OR_QUERY", field="Master_Question",\
            boost_val=2.0)
        hits = SEARCH_ENGINE.search(query, \
            query_string=ID_QUERY_DICT[unique_id], \
            query_field="Master_Question", top_n=10)

        what_to_say = ""
        for doc in hits:
            what_to_say += "\ncontents : " + doc[1] + "\nscore : "+str(doc[0]) \
            + "\n\n\n" 
        
        resp_json["what_to_say"] = what_to_say
    
        # Logging
        original_stdout = sys.stdout 
        with open('log.txt', 'a') as f:
            sys.stdout = f # Change the standard output to the file we created.
            print("The user question is ", ID_QUERY_DICT[unique_id])
            print("The generated lucene query is ", query)
            print("The results of the search are ", hits)
            sys.stdout = original_stdout

    return jsonify(resp_json)    

@app.route('/')
def hello_world():
    return 'Hello, World! Bye world, Hi world'
        

if __name__ == '__main__':
    INDEX = IndexFiles("./VaccineIndex.Index",StandardAnalyzer())
    INDEX.indexFolder("./WHO-FAQ-Keyword-Engine/test_excel_data/json_data")

    QUERY_GEN = QueryGenerator(StandardAnalyzer())
    
    indexDir = INDEX.getIndexDir()
    SEARCH_ENGINE = SearchEngine(indexDir, rerank=False)
    
    extractor_json_path = \
        "./WHO-FAQ-Keyword-Engine/test_excel_data/curated_keywords.json"
    f = open(extractor_json_path,)
    jsonObj = json.load(f)
    KEYWORD_EXTRACTOR = KeywordExtract(jsonObj)
    
    ID_KEYWORD_DICT = defaultdict(dict)
    ID_QUERY_DICT = defaultdict(str)

    qa_config_path = "./WHO-FAQ-Dialog-Manager/QNA/question_asker_config.json"
    QUESTION_ASKER = QuestionAsker(qa_config_path)

    app.run(host='0.0.0.0', port = 5001)