import sys
import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True



# defines what kind of query we are serving
    # qna / location finding / connecting to human
@app.route('/api/v2/qna', methods=['GET'])
def answer_question():
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

@app.route('/')
def hello_world():
    return 'Hello, World! Bye world'
        

    

if __name__ == '__main__':
    num_encountered = 0
    app.run(host='0.0.0.0', port = 5001)