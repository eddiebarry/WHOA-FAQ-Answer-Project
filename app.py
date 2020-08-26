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
    global KEYWORD_EXTRACTOR

    # If first time being sent, calculate a unique id
    query = request.args['query']
    if request.args['user_id'] == "-1":
        unique_id = hashlib.sha512(query.encode()).hexdigest()
    else:
        unique_id = request.args['user_id']
  
    boosting_tokens = KEYWORD_EXTRACTOR.parse_regex_query(query)
    all_token_keys = set(boosting_tokens.keys()).\
        union(ID_KEYWORD_DICT[unique_id].keys())
    
    new_boosting_dict = defaultdict(list)
    for key in all_token_keys:
        # Add all the tokens present in the current query
        if key in boosting_tokens.keys():
            new_boosting_dict[key].extend(boosting_tokens[key])

        # Add all the tokens present in past queries
        if key in ID_KEYWORD_DICT[unique_id].keys():
            new_boosting_dict[key].extend(bID_KEYWORD_DICT[unique_id][key])

    original_stdout = sys.stdout 
    with open('log.txt', 'a') as f:
        sys.stdout = f # Change the standard output to the file we created.
        print("the query is ", query)
        print("the id is ", unique_id)
        print("the keywords are ", new_boosting_dict)
        sys.stdout = original_stdout
    
    ID_KEYWORD_DICT[unique_id] = new_boosting_dict
    

    # import pdb
    # pdb.set_trace()
    # Get response dict from question asker

    # process the query and send the closest question

    # If response contains all necessary keywords, ask query to 
    # search engine

    resp_json = {
            "ask_more_question": True,
            "what_to_say": "what disease are you talking about ?",
            "user_id": unique_id,
        }

    return jsonify(resp_json)

    

    

@app.route('/')
def hello_world():
    return 'Hello, World! Bye world, Hi world'
        

    

if __name__ == '__main__':
    INDEX = IndexFiles("./VaccineIndex.Index",StandardAnalyzer())
    
    QUERY_GEN = QueryGenerator(StandardAnalyzer())
    
    indexDir = INDEX.getIndexDir()
    SEARCH_ENGINE = SearchEngine(indexDir, rerank=True)
    
    extractor_json_path = \
        "./WHO-FAQ-Keyword-Engine/test_excel_data/curated_keywords.json"
    f = open(extractor_json_path,)
    jsonObj = json.load(f)
    KEYWORD_EXTRACTOR = KeywordExtract(jsonObj)
    
    ID_KEYWORD_DICT = defaultdict(dict)

    app.run(host='0.0.0.0', port = 5001)