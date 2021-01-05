#TODO : FIX imports to follow pep8 sorted order
import sys, os, json, pdb, requests, random
from similarity.ngram import NGram
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
from rerank.rerank_config import RE_RANK_ENDPOINT
from variation_generation.variation_generator import VariationGenerator

from qna.common import preprocess, tokenize, porter_stemmer_instance
from qna.question_asker import QuestionAsker

from update_engine import UpdateEngine
from keyword_engine_manager import KeywordEngineManager
from qa_keyword_manager import  QAKeywordManager
from category_question_manager import CategoryQuestionManager
from data.helpers import populate_1500_questions


# SETUP
SEARCH_ENGINE = SolrSearchEngine(
    rerank_endpoint=RE_RANK_ENDPOINT+"/api/v1/reranking",
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
    debug=True,
    use_markdown=True
)

extractor_json_path = \
    "./accuracy_tests/unique_keywords.json"
f = open(extractor_json_path,)
jsonObj = json.load(f)
KEYWORD_EXTRACTOR = KeywordExtract(jsonObj)

ID_KEYWORD_DICT = defaultdict(dict)
ID_QUERY_DICT = defaultdict(str)

qa_config_path = "./accuracy_tests/question_asker_config.json"
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

app = flask.Flask(__name__)
app.config["DEBUG"] = False
app.config['sim'] = NGram(2)
app.config['ID_KEYWORD_DICT']=ID_KEYWORD_DICT
app.config['ID_QUERY_DICT']=ID_QUERY_DICT
app.config['KEYWORD_EXTRACTOR']=KEYWORD_EXTRACTOR
app.config['QUESTION_ASKER']=QUESTION_ASKER
app.config['SEARCH_ENGINE']=SEARCH_ENGINE
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
    Expects a api call of the form : 
    {
            query : String,
            user_id : String
    }
    
    query : String
        The string from which we need to extract keywords and use for QA
    user_id : String
        A unique identifier assigned by the system

    Outputs
    -------
    Json Object : 
        The form of the json object is as follows : -
    """

    request_json = json.loads(request.data, strict=False)
    if 'query' not in request_json.keys():
        return jsonify({"message":"request does not contain query"})
    
    # If first time being sent, calculate a unique id
    query_string = request_json['query'].lower()\
        .replace("?","")\
        .replace("-","")\
        .replace("not relevant","")\
        .replace("none","")\
        .replace("\n"," ")

    if 'user_id' not in request_json.keys():
        return jsonify({"message":"request does not contain user id"})

    first_user_entry = False
    # print(request_json['user_id'][:10])
    if request_json['user_id'] == "-1":
        unique_id = hashlib.sha512((query_string + str(random.randint(0, 100000000))).encode()).hexdigest()
        # If question has already been answered allow new question to be asked
        app.config['ID_QUERY_DICT'][unique_id] = query_string + " "
        first_user_entry = True
    else:
        unique_id = request_json['user_id']
        if app.config['ID_QUERY_DICT'][unique_id] == '-1':
            first_user_entry = True
            app.config['ID_QUERY_DICT'][unique_id] = ""
        # Add entire conversation to search engine
        app.config['ID_QUERY_DICT'][unique_id] += query_string.lower() + " " 
    # print(unique_id[:10])

    # Extract keywords on the basis of the user input
    boosting_tokens = app.config['KEYWORD_EXTRACTOR'].parse_regex_query(\
        query_string.lower())
    
    # Make a set of all fields which have had keywords detected
    all_token_keys = set(boosting_tokens.keys()).\
        union(app.config['ID_KEYWORD_DICT'][unique_id].keys())
    
    # Create a combined dictinary of old keywords and new keywords
    new_boosting_dict = defaultdict(list)
    for key in all_token_keys:
        # Add all the tokens present in the current query
        if key in boosting_tokens.keys():
            new_boosting_dict[key].extend(boosting_tokens[key])

        # Add all the tokens present in past queries
        if key in app.config['ID_KEYWORD_DICT'][unique_id].keys():
            new_boosting_dict[key].extend(app.config['ID_KEYWORD_DICT'][unique_id][key])

    # Store the newly created keyword dictionary in global memory
    app.config['ID_KEYWORD_DICT'][unique_id] = new_boosting_dict

    # Identify wether more questions need to be asked or not
    # # TODO : Ask question only once
    should_search, resp_json = app.config['QUESTION_ASKER'].process(\
        unique_id, new_boosting_dict, app.config['ID_QUERY_DICT'][unique_id])

    resp_json["show_direct_answer"] = False

    if should_search or resp_json["first_question"] or first_user_entry:
        print("searching index")
        query = None
        query, synonyms = app.config['SEARCH_ENGINE'].build_query(app.config['ID_QUERY_DICT'][unique_id], \
            app.config['ID_KEYWORD_DICT'][unique_id], "OR_QUERY", field="question",\
            boost_val=2.0)
            
        hits = app.config['SEARCH_ENGINE'].search(query, 
            project_id=UPDATE_ENGINE.qa_keyword_manager.latest_project_id,
            version_id=UPDATE_ENGINE.qa_keyword_manager.latest_version_id,\
            query_string=app.config['ID_QUERY_DICT'][unique_id], \
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
            sim_score = app.config['sim'].distance(question_and_variation[0],app.config['ID_QUERY_DICT'][unique_id])
            
            if sim_score<0.25:
                print("similar enough")
                resp_json["show_direct_answer"] = True
                resp_json["ask_more_question"]=False
                what_to_say[answer_title] = question_and_variation[-1]
            else:
                print("not similar",sim_score)
                what_to_say[answer_title] = question_and_variation[-2]

    if resp_json["show_direct_answer"] or not resp_json["ask_more_question"]:
        # what_to_say += "The synonyms we extracted from the user question are :\n"
        syn_str = ""
        for syn in synonyms:
            if syn != "":
                syn_str += syn+" ,"
        what_to_say["synonyms"] = syn_str
        resp_json["what_to_say"] = what_to_say

        # Logging
        # original_stdout = sys.stdout 
        # with open('./logs/log.txt', 'a') as f:
        #     sys.stdout = f # Change the standard output to the file we created.
        #     print('$'*80)
        #     print("unique id", unique_id)
        #     print("The user question is ", app.config['ID_QUERY_DICT'][unique_id])
        #     print("The generated lucene query is ", query)
        #     print("The results of the search are ", hits)
        #     print('$'*80)
        #     sys.stdout = original_stdout

        # # Reset unique id query to sentinel value
        app.config['ID_QUERY_DICT'][unique_id] = "-1"
        # ID_KEYWORD_DICT[unique_id] = defaultdict(list)

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
    # global KEYWORD_EXTRACTOR
    # global SEARCH_ENGINE

    request_json = json.loads(request.data, strict=False)
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
        synonyms = app.config['SEARCH_ENGINE'].synonym_expander.return_synonyms(query_string)
        synonyms = [word.strip('"') for word in synonyms]

        query_string = query_string +" " + " ".join(x for x in synonyms)

        # Extract keywords on the basis of the user input
        boosting_tokens = app.config['KEYWORD_EXTRACTOR'].parse_regex_query(query_string)

        if 'id' not in qa_pair.keys():
            return jsonify({"message":"a qa pair does not have an id"})

        temp_keyword_dict['id'] = qa_pair['id']
        temp_keyword_dict['keywords']=boosting_tokens

        questions_keywords_list.append(temp_keyword_dict)    
        # Logging
        original_stdout = sys.stdout 
        with open('./logs/keyword_log.txt', 'a') as f:
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

    request_json = json.loads(request.data, strict=False)
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

    question_list = add_formatting(question_list)
    
    # TODO : check question list format
    keyword_dir = request_json['keyword_directory']
    app.config['KEYWORD_EXTRACTOR'].config = keyword_dir
    app.config['KEYWORD_EXTRACTOR'].dict = app.config['KEYWORD_EXTRACTOR'].parse_config(keyword_dir)

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

@app.route('/api/v2/get-bot-host', methods=['GET'])
def link_to_bot():
    request_json = json.loads(request.data, strict=False)
    requires = [
            'project_id', 'version_id',
        ]
    for x in requires:
        if x not in request_json.keys():
            return jsonify({"message":"given request does not have a "+x })

    response = {
        "host_id": os.getenv('BOTPRESS_ENDPOINT'),
        "bot_id": os.getenv('BOT_ID')
    }
    return jsonify(response)

def add_formatting(question_list):
    # iterate over questions in question list
    # format if necessary
    for questions in question_list:
        if "answer_formatted" not in questions.keys() \
            and "answer" in questions.keys():
            try:
                url = "http://18.203.115.216:5000"
                base_url= url + "/api/v2/summariser"
                data = {
                    "body":questions["answer"],
                }
                r = requests.get(base_url, data=json.dumps(data))
                data = r.json()
                questions["answer_formatted"] = data['markdown_text']
            except:
                questions["answer_formatted"] = questions["answer"]
                print("failed in init")
    return question_list

@app.before_first_request
def init_data():
    print("calling init function")
    #TODO : change to flask variable
    # global UPDATE_ENGINE
    # global KEYWORD_EXTRACTOR

    request_json = populate_1500_questions(dir_ = "./accuracy_tests/intermediate_results/vsn_data_formatted")
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

    # iterate over questions in question list
    # format if necessary
    question_list = add_formatting(question_list)
    
    # TODO : check question list format
    keyword_dir = request_json['keyword_directory']
    app.config['KEYWORD_EXTRACTOR'].config = keyword_dir
    app.config['KEYWORD_EXTRACTOR'].dict = app.config['KEYWORD_EXTRACTOR'].parse_config(keyword_dir)

    data_hash_string = project_id + version_id
    data_hash_id = hashlib.sha512(data_hash_string.encode())\
                        .hexdigest()
    
    project_info = [data_hash_id, project_id, version_id, \
        version_number, previous_versions]
    
    UPDATE_ENGINE.add_questions(question_list, project_info)

@app.route('/')
def hello_world():
    return 'Hello, World! The service is up for serving qna to the bot :-('
        

if __name__ == '__main__':
    SEARCH_ENGINE = SolrSearchEngine(
        rerank_endpoint=RE_RANK_ENDPOINT+"/api/v1/reranking",
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
        debug=True,
        use_markdown=True
    )
    
    extractor_json_path = \
        "./accuracy_tests/unique_keywords.json"
    f = open(extractor_json_path,)
    jsonObj = json.load(f)
    KEYWORD_EXTRACTOR = KeywordExtract(jsonObj)
    
    ID_KEYWORD_DICT = defaultdict(dict)
    ID_QUERY_DICT = defaultdict(str)

    qa_config_path = "./accuracy_tests/question_asker_config.json"
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

    app.run(host='0.0.0.0', port = 5009)