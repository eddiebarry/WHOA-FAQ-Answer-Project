import requests

base_url="http://18.220.219.51:5003/api/v2/keyword_extract"
params = {
    "question":"My child is sick where can he get measles vaccine ?",
    "answer":"Please go to khandala",
}

r = requests.get(base_url, params=params)
print(r.text)
"""
{
    "Disease 1": [
        "measles"
    ], 
    "Disease 2": [
        "measles"
    ], 
    "Keyword": [
        "child", 
        "measles"
    ], 
    "Other -condition, symptom etc": [
        "sick", 
        "child"
    ], 
    "Subject - Person": [
        "child"
    ], 
    "Vaccine 1": [
        "measles"
    ], 
    "Vaccine 2": [
        "measles"
    ], 
    "Who is writing this": [
        "child"
    ]
}
"""