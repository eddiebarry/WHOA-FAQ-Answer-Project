import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# defines what kind of query we are serving
    # qna / location finding / connecting to human
@app.route('/api/v2/qna', methods=['GET'])
def answer_question():
    pass
    # request will have user query and sentinel value

    # process the query and send the closest question

@app.route('/')
def hello_world():
    return 'Hello, World!'
        

    


app.run(host='0.0.0.0')