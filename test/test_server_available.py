import os
import requests
from dotenv import load_dotenv
load_dotenv()

# Need to test solr server is up
# Need to tets application server is up
# Need to test rerank server is up
urls = [
    os.getenv("RE_RANK_ENDPOINT"),
    os.getenv("BOTPRESS_ENDPOINT"),
    os.getenv("LOCAL_URL"),
    os.getenv("REMOTE_URL"),
]   
def test_server_available():
    