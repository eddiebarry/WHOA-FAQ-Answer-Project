import sys, os, lucene, json, pdb
import hashlib
sys.path.append('WHO-FAQ-Keyword-Engine')
sys.path.append('WHO-FAQ-Search-Engine')
sys.path.append('WHO-FAQ-Update-Engine')
sys.path.append('WHO-FAQ-Dialog-Manager')
sys.path.append('WHO-FAQ-Dialog-Manager/qna')

import flask
from flask import request, jsonify
from collections import defaultdict 
from threading import Thread

from keyword_extractor import KeywordExtract
from solr_search import SolrSearchEngine
from rerank.config import RE_RANK_ENDPOINT
from variation_generation.variation_generator import VariationGenerator
from query_generator import QueryGenerator
from index import IndexFiles
from org.apache.lucene.analysis.standard import StandardAnalyzer

from qna.common import preprocess, tokenize, porter_stemmer_instance
from qna.question_asker import QuestionAsker

from update_engine import UpdateEngine
from keyword_engine_manager import KeywordEngineManager
from qa_keyword_manager import  QAKeywordManager
from category_question_manager import CategoryQuestionManager


app = flask.Flask(__name__)
app.config["DEBUG"] = True
# app.config['JSON_AS_ASCII'] = False
# lucene.initVM(vmargs=['-Djava.awt.headless=true'])


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
    # global QUERY_GEN
    global SEARCH_ENGINE
    # vm_env = lucene.getVMEnv()
    # vm_env.attachCurrentThread()

    request_json = json.loads(request.data)
    if 'query' not in request_json.keys():
        return jsonify({"message":"request does not contain query"})
    
    # If first time being sent, calculate a unique id
    query_string = request_json['query'].lower()\
        .replace("?","")\
        .replace("-","")\
        .replace("not relevant","")\
        .replace("none","")

    if 'user_id' not in request_json.keys():
        return jsonify({"message":"request does not contain user id"})
    
    if request_json['user_id'] == "-1":
        unique_id = hashlib.sha512(query_string.encode()).hexdigest()
        # If question has already been answered allow new question to be asked
        ID_QUERY_DICT[unique_id] = query_string + " "
    else:
        unique_id = request_json['user_id']
        # Add entire conversation to search engine
        ID_QUERY_DICT[unique_id] += query_string.lower() + " " 

    # Extract keywords on the basis of the user input
    boosting_tokens = KEYWORD_EXTRACTOR.parse_regex_query(\
        query_string.lower())
    
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
        query, synonyms = SEARCH_ENGINE.build_query(ID_QUERY_DICT[unique_id], \
            ID_KEYWORD_DICT[unique_id], "OR_QUERY", field="question",\
            boost_val=2.0)
            
        hits = SEARCH_ENGINE.search(query, 
            project_id=UPDATE_ENGINE.qa_keyword_manager.latest_project_id,
            version_id=UPDATE_ENGINE.qa_keyword_manager.latest_version_id,\
            query_string=ID_QUERY_DICT[unique_id], \
            query_field="question*", top_n=50)
        
        what_to_say = {}
        for idx, doc in enumerate(hits[:5]):
            question_and_variation = doc[1].split(" ||| ")
            for var_idx, question_var in enumerate(question_and_variation[:3]):
                title = "question_"+str(idx)+"_variation_"+str(var_idx)
                what_to_say[title] = question_var
            
            score_title = "question_"+str(idx)+"_score"
            what_to_say[score_title] = doc[0]

            answer_title = "question_"+str(idx)+"_answer"
            what_to_say[answer_title] = question_and_variation[-1]
        
        # what_to_say += "The synonyms we extracted from the user question are :\n"
        syn_str = ""
        for syn in synonyms:
            if syn != "":
                syn_str += syn+" ,"
        what_to_say["synonyms"] = syn_str
        
        resp_json["what_to_say"] = what_to_say

        # Reset unique id query to sentinel value
        ID_QUERY_DICT[unique_id] = "-1"
        ID_KEYWORD_DICT[unique_id] = defaultdict(list)
    
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

@app.route('/api/v2/batch_keyword_extract', methods=['POST'])
def return_batch_keyword():
    """
    After the keyword engine is set up with a configuration file,
    this api extracts the keywords from the user query and returns them
    as a json object

    Inputs
    ------
    Expects a api call of the form : 
        localhost:5003/api/v2/batch_keyword_extract
        {
            num_questions : Integer,

            question_answer_list = [
                {
                    question : "abc",
                    answer : "def",
                    hash : sha512 hash of question+answer
                },
                ...
                ...
                {
                    question : "ghi",
                    answer : "jkl"
                    hash : sha512 hash of question+answer
                },
            ]
        }
    
    Query : String
        The string from which we need to extract keywords

    Outputs
    -------
    Json Object : 
        The form of the json object is as follows : -
        {
            questions_keywords_dict : {
                question_1_hash : {
                    category_1 : [
                        cat_1_keyword_1,
                        cat_1_keyword_2
                    ],
                    category_2 : [
                        cat_2_keyword_1,
                        cat_2_keyword_2
                    ],
                    category_3: [
                        cat_3_keyword_1,
                        cat_3_keyword_2
                    ]
                },
                ...
                question_n_hash : {
                    category_1 : [
                        cat_1_keyword_1,
                        cat_1_keyword_2
                    ],
                    category_2 : [
                        cat_2_keyword_1,
                        cat_2_keyword_2
                    ],
                    category_3: [
                        cat_3_keyword_1,
                        cat_3_keyword_2
                    ]
                }
            }
        }
            
    """
    global KEYWORD_EXTRACTOR
    global SEARCH_ENGINE

    request_json = json.loads(request.data)
    questions_keywords_list = []

    if 'question_answer_list' not in request_json.keys():
        return jsonify({"message":"request does not contain a question answer list"})

    for qa_pair in request_json['question_answer_list']:
        temp_keyword_dict = {}

        if 'question' not in qa_pair.keys():
            return jsonify({"message":"a qa pair does not have a question"})
        
        if 'answer' not in qa_pair.keys():
            return jsonify({"message":"a qa pair does not have an answer"})
        
        # If first time being sent, calculate a unique id
        query_string = qa_pair['question'].replace("?","") \
            + " " + qa_pair['answer'].replace("?","")

        # Get synonyms present in the query string
        synonyms = SEARCH_ENGINE.synonym_expander.return_synonyms(query_string)
        synonyms = [word.strip('"') for word in synonyms]

        query_string = query_string +" " + " ".join(x for x in synonyms)

        # Extract keywords on the basis of the user input
        boosting_tokens = KEYWORD_EXTRACTOR.parse_regex_query(query_string)

        if 'id' not in qa_pair.keys():
            return jsonify({"message":"a qa pair does not have an id"})

        temp_keyword_dict['id'] = qa_pair['id']
        temp_keyword_dict['keywords']=boosting_tokens

        questions_keywords_list.append(temp_keyword_dict)    
        # Logging
        original_stdout = sys.stdout 
        with open('keyword_log.txt', 'a') as f:
            sys.stdout = f # Change the standard output to the file we created.
            print('$'*80)
            print("The user query is ", query_string)
            print("The extracted tokens are ", boosting_tokens)
            print('$'*80)
            sys.stdout = original_stdout

    response = {
        "questions_keywords_list":questions_keywords_list
    }

    #TODO :  preprocess cleaned boosting tokens to line up with specified tokens
    return jsonify(response)

# Need json objects with variations
@app.route('/api/v2/train_bot_json_array', methods=['POST'])
def index_json_array():
    """
    This function takes a json array specified by the labelling web service 
    and add its to the search index

    Inputs
    ------
    Expects a api call with json data of the form : 
    {
        "project_id":A unique project id,
        "version_id":A unique version id,
        question_array : [
            {
                question : "ABC"
                answer : "DEF"
                category1 : ["cat_1_keyword_1", "cat_2_keyword_2", ...]
                category2 : ["cat_2_keyword_1", "cat_2_keyword_2", ...]
            },
            {
                question : "GHI"
                answer : "JKL"
                category3 : ["cat_1_keyword_1", "cat_2_keyword_2", ...]
                category4 : ["cat_2_keyword_1", "cat_2_keyword_2", ...]
            }
        ],
        keyword_directory : {
            category1 : ["cat_1_unique_kw_1", "cat_1_unique_kw_2", ...],
            category2 : ["cat_2_unique_kw_1", "cat_2_unique_kw_2", ...],
            category2 : ["cat_2_unique_kw_1", "cat_2_unique_kw_2", ...],
        },
        "previous_versions" : [
            1,
            2,
            3
        ]
    }

    Outputs
    -------
    Json Object : 
    The form of the json object is as follows : -
    {
        "project_id": project_id,
        "version_id": version_id,
        "status":"ok",
        "version_number": "1.0" - string
    }
    """
    global UPDATE_ENGINE

    request_json = json.loads(request.data)
    requires = [
            'project_id', 'version_id', 'question_list',
            'keyword_directory'
        ]
    for x in requires:
        if x not in request_json.keys():
            return jsonify({"message":"given request does not have a "+x })

    # Adding the files to the array
    question_list = request_json['question_list']
    project_id = request_json['project_id']
    version_id = request_json['version_id']

    if 'previous_versions' in request_json.keys():
        version_number = len(request_json['previous_versions']) + 1.0
        version_number = str(version_number)
        previous_versions = request_json['previous_versions']
    else:
        version_number = "1.0"
        previous_versions = []

    if type(project_id) != str:
        project_id = str(project_id)
    if type(version_id) != str:
        version_id = str(version_id)
    if type(version_number) != str:
        version_number = str(version_number)
    
    # TODO : check question list format
    keyword_dir = request_json['keyword_directory']
    KEYWORD_EXTRACTOR.config = keyword_dir
    KEYWORD_EXTRACTOR.dict = KEYWORD_EXTRACTOR.parse_config(keyword_dir)

    data_hash_string = project_id + version_id
    data_hash_id = hashlib.sha512(data_hash_string.encode())\
                        .hexdigest()
    
    project_info = [data_hash_id, project_id, version_id, \
        version_number, previous_versions]

    
    UPDATE_ENGINE.add_questions(question_list, project_info)

    response = {
        "project_id": project_id,
        "version_id": version_id,
        "status":"ok",
        "estimated_time": len(question_list)*3
    }

    return jsonify(response)

@app.route('/api/v2/get-bot-host')
def link_to_bot():
    request_json = json.loads(request.data)
    requires = [
            'project_id', 'version_id',
        ]
    for x in requires:
        if x not in request_json.keys():
            return jsonify({"message":"given request does not have a "+x })

    response = {
        "host_id": 'https://ec2-52-209-188-140.eu-west-1.compute.amazonaws.com',
        "bot_id": 'bot_test'
    }
    return jsonify(response)

@app.route('/')
def hello_world():
    return 'Hello, World! The service is up for serving qna to the bot :-)'
        

if __name__ == '__main__':
    SEARCH_ENGINE = SolrSearchEngine(
        rerank_endpoint=RE_RANK_ENDPOINT,
        variation_generator_config=[
            VariationGenerator(\
            path="./WHO-FAQ-Search-Engine/variation_generation/variation_generator_model_weights/model.ckpt-1004000",
            max_length=5),   #variation_generator
            # None,
            ["question"] #fields_to_expand
        ],
        synonym_config=[
            True, #use_wordnet
            True, #use_syblist
            "./WHO-FAQ-Search-Engine/synonym_expansion/syn_test.txt" #synlist path
        ],
        debug=True
    )
    
    extractor_json_path = \
        "./tests/unique_keywords.json"
    f = open(extractor_json_path,)
    jsonObj = json.load(f)
    KEYWORD_EXTRACTOR = KeywordExtract(jsonObj)
    
    ID_KEYWORD_DICT = defaultdict(dict)
    ID_QUERY_DICT = defaultdict(str)

    qa_config_path = "./tests/question_asker_config.json"
    use_question_predicter_config = [
            False, #Use question predictor
            "./WHO-FAQ-Dialog-Manager/qna/models.txt", #models path
            "./WHO-FAQ-Dialog-Manager/qna/vectoriser.txt" #tokeniser path
        ]
    QUESTION_ASKER = QuestionAsker(qa_config_path, show_options=True, \
        qa_keyword_path = extractor_json_path,
        use_question_predicter_config=use_question_predicter_config)

    # Setting up the update engine
    qa_keyword_manager = QAKeywordManager(
        search_engine=SEARCH_ENGINE,
    )
    keyword_engine_manager = KeywordEngineManager()
    category_question_manager = CategoryQuestionManager()
    UPDATE_ENGINE = UpdateEngine(
        keyword_engine_manager=keyword_engine_manager,
        qa_keyword_manager=qa_keyword_manager,
        category_question_manager=category_question_manager
    )

    app.run(host='0.0.0.0', port = 5007)