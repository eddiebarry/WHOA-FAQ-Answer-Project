import sys
import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# defines what kind of query we are serving
    # qna / location finding / connecting to human
@app.route('/api/v2/qna', methods=['GET'])
def answer_question():
    # Save a reference to the original standard output
    original_stdout = sys.stdout 
    with open('log.txt', 'a') as f:
        sys.stdout = f # Change the standard output to the file we created.
        print(request.args)
        sys.stdout = original_stdout

    resp_json = {
        "ask_more_question": True,
        "what_to_say": "what disease are you talking about ?",
        "user_id": "100200"
    }

    return jsonify(resp_json)

    # request will have user query and sentinel value

    # process the query and send the closest question

@app.route('/')
def hello_world():
    return 'Hello, World! Bye world'
        

    


app.run(host='0.0.0.0', port = 5001)