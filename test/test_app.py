import requests ,hashlib, json, os, pickle, timeit, pdb, sys
from statistics import mean 

import pytest

from dotenv import load_dotenv
load_dotenv()

urls = [
    os.getenv("LOCAL_URL"),
    os.getenv("REMOTE_URL"),
]

"""
Batch Keyword Extract Test
"""
def test_batch_keyword_extract():
    batch_keyword_input = {
        "question_answer_list": [
            {
                "question": "My child is sick where can he get measles vaccine ?",
                "answer": "Please go to khandala",
                "id": "1"
            },
            {
                "question": "My child is sick where can he get rubella vaccine ?",
                "answer": "Please go to khandala",
                "id": "2"
            },
            {
                "question": "My child is sick where can he get polio vaccine ?",
                "answer": "Please go to khandala",
                "id": "3"
            }
        ]
    }
    batch_keyword_response ={
    "questions_keywords_list": [
        {
            "id": "1",
            "keywords": {
                "disease_1": [
                    "measles"
                ],
                "disease_2": [
                    "measles"
                ],
                "other_conditions_or_symptoms_etc": [
                    "sick",
                    "child",
                    "baby"
                ],
                "subject_2_vaccination_general": [
                    "travel"
                ],
                "subject_person": [
                    "baby",
                    "child"
                ],
                "vaccine_1": [
                    "measles"
                ],
                "vaccine_2": [
                    "measles"
                ],
                "who_is_writing_this": [
                    "child"
                ]
            }
        },
        {
            "id": "2",
            "keywords": {
                "disease_1": [
                    "rubella"
                ],
                "disease_2": [
                    "rubella"
                ],
                "other_conditions_or_symptoms_etc": [
                    "sick",
                    "child",
                    "baby"
                ],
                "subject_2_vaccination_general": [
                    "travel"
                ],
                "subject_person": [
                    "baby",
                    "child"
                ],
                "vaccine_1": [
                    "rubella"
                ],
                "vaccine_2": [
                    "rubella"
                ],
                "who_is_writing_this": [
                    "child"
                ]
            }
        },
        {
            "id": "3",
            "keywords": {
                    "other_conditions_or_symptoms_etc": [
                        "sick",
                        "child",
                        "baby"
                    ],
                    "subject_2_vaccination_general": [
                        "travel"
                    ],
                    "subject_person": [
                        "baby",
                        "child"
                    ],
                    "vaccine_1": [
                        "polio"
                    ],
                    "vaccine_2": [
                        "polio"
                    ],
                    "who_is_writing_this": [
                        "child"
                    ]
                }
            }
        ]
    }

    for url in urls:
        base_url = url  + "/api/v2/batch_keyword_extract"
        r = requests.post(base_url,
            data=json.dumps(batch_keyword_input))
        data = r.json()
        assert data == batch_keyword_response, \
            "Keyword extract failed for " + url

"""
Batch QA index 
"""

def test_qa_indexing():
    qa_index_data = {
        "project_id": 999,
        "version_id": 3,
        "previous_versions": [
            1,
            2
        ],
        "question_list": [
            {
                "answer": "As per Canada's National Advisory Committee on Immunization (NACI), there are no data on the safety or effectiveness of the HPV9 vaccine in men 27 years of age and older and therefore, no evidence-based recommendations can be made for the use of the vaccine in this age group.\u00a0 However, the HPV9 vaccine may be given to men 27 years of age and older who are at ongoing risk of exposure to HPV. \u00a0\nMen who have sex with men are at increased risk of HPV-related diseases. For this reason, the HPV vaccine is recommended for men 27 years of age and older who have sex with men, although there are no data on the effectiveness of the HPV9 vaccine in this population.\nWe recommend that you discuss getting vaccinated further with your health care provider.\u00a0\nThe HPV9 vaccine is available for purchase at most pharmacies and travel clinics (the HPV9 vaccine is not provided for free to males in your age group).\nYou can learn more about the HPV9 vaccine on our HPV page.\n- Immunization Nurse",
                "question": "A recent study showed men with 5+ partners who perform unprotected oral sex have a higher risk of HPV-induced oral cancers. I am 38, male, sexually active, I never have used protection when giving oral sex. Can I get the HPV vaccine?",
                "question_variation_0": "when can a male be in sexual activity with oral sex and never have used protection when giving oral sex",
                "question_variation_1": "can i take hpv vaccine without protection",
                "question_variation_2": "what hpv vaccination for hpv",
                "id": "0",
                "keywords": [
                    {
                        "disease_1": [
                            "Human papillomavirus (HPV)"
                        ]
                    },
                    {
                        "disease_2": [
                            "Cancer"
                        ]
                    },
                    {
                        "subject_1_immunization": [
                            "Vaccination"
                        ]
                    },
                    {
                        "vaccine_1": [
                            "(HPV) Human papillomavirus "
                        ]
                    },
                    {
                        "who_is_writing_this": [
                            "Adult"
                        ]
                    }
                ]
            },
            {
                "answer": "The Tetanus and Diphtheria (Td) Vaccine is provided for free in BC.\u00a0 \nAdults who were immunized against tetanus and diphtheria when they were younger should get a booster dose of the Td vaccine every 10 years. \u00a0\nAdults can get the vaccine from public health units and most pharmacies. Some doctors' offices also provide vaccines. Services vary across BC.",
                "question": "Is Td booster covered by MSP or Pharmacare?\n",
                "question_variation_0": "does ms booster ms td booster covered by msp or Pharmacare",
                "question_variation_1": "is MSP coverage or MSP coverage coverage",
                "question_variation_2": "is td booster covered Ms td booster booster booster coverage",
                "id": "1",
                "keywords": [
                    {
                        "subject_2_vaccination_general": [
                            "Vaccine Cost"
                        ]
                    },
                    {
                        "vaccine_1": [
                            "(DTap) Diphtheria / Tetanus / Pertussis"
                        ]
                    },
                    {
                        "who_is_writing_this": [
                            "Unknown "
                        ]
                    }
                ]
            },
            {
                "answer": "In BC, the HPV vaccine is publicly funded (free) for some boys and young men depending on their age and other factors. Learn more\u00a0here.\u00a0Anyone who is not eligible for a free HPV vaccine can purchase and receive it at most pharmacies and travel clinics without a prescription. Services vary across BC.\nImmunization Nurse\n",
                "question": "Does my 13 year old son need a prescription to receive the HPV vaccine at my pharmacy? He did not receive the vaccine in grade 6.",
                "question_variation_0": "do 13 year old boys need a prescription for vaccine",
                "question_variation_1": "do i need a prescription for HPV vaccine",
                "question_variation_2": "do i need a prescription for my 13 year old son to receive hpv vaccine",
                "id": "2",
                "keywords": [
                    {
                        "disease_1": [
                            "Human papillomavirus (HPV)"
                        ]
                    },
                    {
                        "subject_1_immunization": [
                            "Immunization Required"
                        ]
                    },
                    {
                        "subject_2_vaccination_general": [
                            "Vaccination"
                        ]
                    },
                    {
                        "subject_person": [
                            "Child"
                        ]
                    },
                    {
                        "vaccine_1": [
                            "Human papillomavirus (HPV)"
                        ]
                    },
                    {
                        "who_is_writing_this": [
                            "Parent"
                        ]
                    }
                ]
            }
        ],
        "keyword_directory": [
            {
                "disease_1": [
                    "rubella",
                    "tuberculosis",
                    "tb",
                    "autism",
                    "mouth",
                    "hpv",
                    "meningitis",
                    "asthma",
                    "measles",
                    "pneumonia",
                    "hand and foot disease",
                    "shingles",
                    "genital herpes",
                    "rabies",
                    "influenza",
                    "mumps",
                    "pulmonaary fibrosis",
                    "common cold",
                    "allergy",
                    "poliomyelitis",
                    "dengue",
                    "pertussis",
                    "cancer",
                    "hepatitis a",
                    "hepatitis",
                    "overweight and obesity",
                    "varicella",
                    "herpes simplex virus",
                    "tick borne encephalitis",
                    "diphtheria",
                    "flu",
                    "bcg",
                    "tetanus",
                    "human papillomavirus",
                    "hepatitis b",
                    "malaria",
                    "chickenpox",
                    "pneumococcal",
                    "diabetes",
                    "meningococcal",
                    "mmr",
                    "sexually transmitted diseases",
                    "typhoid",
                    "rotavirus"
                ]
            },
            {
                "disease_2": [
                    "rubella",
                    "tuberculosis",
                    "tb",
                    "hpv",
                    "hepatitis a&b",
                    "meningitis",
                    "measles",
                    "pneumonia",
                    "shingles",
                    "rabies",
                    "influenza",
                    "dtap",
                    "mumps",
                    "toxoid",
                    "poliomyelitis",
                    "dengue",
                    "pertussis",
                    "cancer",
                    "hepatitis a",
                    "hepatitis",
                    "varicella",
                    "cholera",
                    "tick borne encephalitis",
                    "diphtheria",
                    "flu",
                    "tetanus",
                    "bcg",
                    "human papillomavirus",
                    "hepatitis b",
                    "chickenpox",
                    "pneumococcal",
                    "general vaccine safety information",
                    "meningococcal",
                    "mmr",
                    "typhoid",
                    "rotavirus"
                ]
            },
            {
                "other_conditions_or_symptoms_etc": [
                    "splenectomy",
                    "vegetarian",
                    "shingrix vaccine",
                    "booster",
                    "delayed reaction",
                    "breast milk",
                    "tuberculin skin test",
                    "swelling",
                    "itchy and pain",
                    "brother in law",
                    "high risk",
                    "emoninail topical fungus treatment",
                    "condyloma acuminatum.",
                    "surgery",
                    "results",
                    "wife",
                    "international",
                    "cervarix",
                    "clinic",
                    "twinrix vaccine",
                    "sexual health",
                    "heavy metals",
                    "lung condition",
                    "flu mist",
                    "immunocompromised",
                    "b12 shot",
                    "needle phobia",
                    "barriere",
                    "vaxigrip",
                    "tests",
                    "dates",
                    "reaction",
                    "dpt",
                    "fatty liver",
                    "kawasaki disease",
                    "outbreak",
                    "allergy shots",
                    "vasovagal",
                    "high dose",
                    "weighed and measured",
                    "high white blood count",
                    "phone number",
                    "allergic reaction",
                    "outreach",
                    "consent",
                    "mass under the skin",
                    "vaccine clinic",
                    "diabetic",
                    "brands",
                    "intercourse",
                    "vaccine prep",
                    "compromised immune system",
                    "partner",
                    "adjuvants",
                    "fever",
                    "suppressed immune system",
                    "coughing and nasally congested",
                    "uncontrollable infantile spasms",
                    "full paralysis",
                    "weigh baby",
                    "bexserro",
                    "pre pregnancy",
                    "pap test",
                    "pneumococcal conjuga",
                    "reason",
                    "cephalosporin",
                    "phn",
                    "vomitting",
                    "pimple",
                    "flu zone high dose",
                    "herpes testing",
                    "rsv",
                    "allergy. aefi",
                    "options",
                    "lactose intolerant",
                    "chemotherapy",
                    "quadracel",
                    "sexual orientation",
                    "indigenous status",
                    "form",
                    "vaccination procedure",
                    "gbs",
                    "needle phobic",
                    "near the injection site",
                    "heart attack",
                    "hemophiliac",
                    "bite",
                    "mandatory",
                    "weekends arm",
                    "prescription",
                    "men",
                    "aleve",
                    "hexavalent vaccine",
                    "4 in one",
                    "work",
                    "hantavirus",
                    "iud",
                    "havrix",
                    "respiritory infection",
                    "west syndrome",
                    "blood fractions",
                    "strep throat",
                    "celiac",
                    "private clinic",
                    "seizeure",
                    "arm hurts",
                    "syringe disposal",
                    "missing",
                    "amoxicillin antibiotics",
                    "vaccine hesitant",
                    "online",
                    "addison's disease",
                    "appointment",
                    "prservatives",
                    "preservative free",
                    "cousin",
                    "suscetability",
                    "soreness and weeping eyes",
                    "sick",
                    "cystic fibrosis lung disease",
                    "cow milk allergy",
                    "health passport",
                    "vegan",
                    "rash",
                    "twinrix",
                    "immune suppressed",
                    "presciption",
                    "draw blood",
                    "numbing cream",
                    "infanrix hexa",
                    "hives",
                    "fluzone",
                    "plantars warts",
                    "available",
                    "zostavax",
                    "bottle feeding",
                    "energix b",
                    "public awareness",
                    "systematic lupus",
                    "tb test",
                    "alcohol",
                    "tattoo",
                    "acne",
                    "diarrhea",
                    "emla",
                    "itpurpura",
                    "arbovirus",
                    "granchild",
                    "supply",
                    "nasal spray",
                    "hbig",
                    "clyndamyacine antiobiotic",
                    "vaccine brand",
                    "youth",
                    "permisssion",
                    "malarone",
                    "legionaries disease",
                    "asymptomatic carrier",
                    "exemption",
                    "bronchiectosis",
                    "red eyes",
                    "strains",
                    "achy",
                    "subject  adult",
                    "child",
                    "public transport",
                    "first aid",
                    "aluminum",
                    "approved",
                    "dukoral",
                    "doses",
                    "breast feeding",
                    "husband",
                    "gardasil",
                    "four vaccines",
                    "translation",
                    "meningococcal quadrivalent conjugate",
                    "unrelated",
                    "whooping cough",
                    "fluad",
                    "quadrivalent",
                    "bad reaction",
                    "symptoms",
                    "eggs",
                    "pregnant",
                    "baby",
                    "low white blood cell count",
                    "blood type",
                    "manufacture",
                    "fluezone",
                    "fertility",
                    "administer",
                    "cost",
                    "severe adverse reaction",
                    "kinder shot",
                    "availability",
                    "rashes on waist",
                    "post herpetic neuralgia",
                    "age",
                    "appt.",
                    "mercury",
                    "hep c",
                    "pneumo conjugate 13",
                    "shingrix",
                    "infanrix",
                    "injury",
                    "side effects",
                    "hard lump",
                    "fluviral",
                    "tasc shingles vaccine study",
                    "side effect",
                    "employees",
                    "redness",
                    "crohns",
                    "earlier",
                    "egg allergy",
                    "stelara",
                    "lyme disease",
                    "flu clinic",
                    "herpes",
                    "short supply",
                    "anaphylaxis",
                    "period",
                    "immunization package",
                    "globulin",
                    "bitten by a dog",
                    "opt out",
                    "brand",
                    "anxiety",
                    "training",
                    "titer",
                    "kidney transplant patient",
                    "email"
                ]
            },
            {
                "subject_1_immunization": [
                    "vaccination",
                    "immunization record",
                    "immunization",
                    "immunization general",
                    "immunity",
                    "immunization required",
                    "immunization schedule",
                    "generic",
                    "immunization safety"
                ]
            },
            {
                "subject_2_vaccination_general": [
                    "booster",
                    "appointment",
                    "vaccine ingredients",
                    "antibody",
                    "protection",
                    "vaccination",
                    "care",
                    "vaccine education",
                    "effectiveness",
                    "safety",
                    "immunity",
                    "pregnancy",
                    "health insurance",
                    "info",
                    "vaccine cost",
                    "prescription",
                    "vaccine safety",
                    "travel",
                    "generic",
                    "work",
                    "school"
                ]
            },
            {
                "subject_person": [
                    "general public",
                    "grandparent",
                    "baby",
                    "elderly",
                    "unknown",
                    "family",
                    "parent",
                    "infant",
                    "girl",
                    "grandchild",
                    "newborn",
                    "sibling",
                    "adolescent",
                    "child",
                    "adult"
                ]
            },
            {
                "vaccine_1": [
                    "rubella",
                    "hep b",
                    "tuberculosis",
                    "tb",
                    "hpv",
                    "hepatitis a&b",
                    "meningitis",
                    "measles",
                    "pneumonia",
                    "shingles",
                    "influenza",
                    "rabies",
                    "dtap",
                    "polio",
                    "mumps",
                    "hib",
                    "poliomyelitis",
                    "dengue",
                    "pertussis",
                    "hepatitis a",
                    "dtap ipv",
                    "ipv",
                    "hepatitis",
                    "varicella",
                    "tick borne encephalitis",
                    "diphtheria",
                    "tetanus",
                    "hepatitis b",
                    "flu",
                    "bcg",
                    "human papillomavirus",
                    "malaria",
                    "chickenpox",
                    "pneumococcal",
                    "general vaccine safety information",
                    "mmr",
                    "meningococcal",
                    "typhoid",
                    "rotavirus"
                ]
            },
            {
                "vaccine_2": [
                    "rubella",
                    "tuberculosis",
                    "tb",
                    "mmrv",
                    "hepatitis a&b",
                    "meningitis",
                    "measles",
                    "pneumonia",
                    "shingles",
                    "influenza",
                    "rabies",
                    "dtap",
                    "japanese encephalitis",
                    "polio",
                    "mumps",
                    "clinic",
                    "hib",
                    "poliomyelitis",
                    "pertussis",
                    "hepatitis a",
                    "ipv",
                    "varicella",
                    "cholera",
                    "high dose",
                    "diphtheria",
                    "haemophilus influenzae type b",
                    "hepatitis b",
                    "tetanus",
                    "bcg",
                    "flu",
                    "aefi",
                    "chickenpox",
                    "pneumococcal",
                    "general vaccine safety information",
                    "hepatitis e",
                    "mmr",
                    "meningococcal",
                    "wheezing",
                    "typhoid",
                    "rotavirus"
                ]
            },
            {
                "who_is_writing_this": [
                    "grandparent",
                    "adolescent",
                    "unknown",
                    "parent",
                    "sibling",
                    "mother",
                    "elderly",
                    "child",
                    "adult"
                ]
            }
        ]
    }

    response_data = {
        "estimated_time": 9,
        "project_id": "999",
        "status": "ok",
        "version_id": "3"
    }

    for url in urls:
        base_url = url  + "/api/v2/train_bot_json_array"
        r = requests.post(base_url,
            data=json.dumps(qa_index_data))
        data = r.json()
        assert data == response_data, \
            ("Test QA index failed for " + url)


"""
Bot host test
"""
def test_bot_host():
    test_bot_data = {
        "project_id":1,
        "version_id":1,
    }
    test_bot_response = {
        "host_id": 'https://new-botpress-botpress-openshift.apps.who.lxp.academy.who.int',
        "bot_id": 'bot_test'
    }
    for url in urls:
        base_url = url  + "/api/v2/get-bot-host"
        r = requests.get(base_url,
            data=json.dumps(test_bot_data))
        data = r.json()

        assert data == test_bot_response, \
            "test bot link failed for " + url