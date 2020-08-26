import flask
from flask import request, jsonify
from match import matcher

app = flask.Flask(__name__)
app.config["DEBUG"] = True

keywords = {"user1": [..., ... ]}

@app.route('/api/v2/qna', methods=['GET'])
def api_question():
    # Get Question
        # Check if id is present

    # Extract Keywords
        # merge with previous if value is not sentinel

    # Check if keywords are present, if yes answer

    # If not, Store keywords, return question id, return specific question



app.run(host='0.0.0.0')