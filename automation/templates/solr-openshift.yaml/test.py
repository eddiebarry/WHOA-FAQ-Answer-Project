import pysolr
import os, json, pdb, requests


# # zookeeper = pysolr.ZooKeeper("zkhost1:2181,zkhost2:2181,zkhost3:2181")
# solr = pysolr.Solr("http://solr-test-zookeeper-cluster.apps.who.lxp.academy.who.int/solr/newCollection1", always_commit=True)

# solr.ping()

# all_data = []
# for x in sorted(os.listdir('./data')):
#     if x.endswith('.json'):
#         jsonpath="./data/"+x
#         f = open(jsonpath,)
#         data = json.load(f)
#         # data = json.loads('./data/'+x)
#         data['id']=x.replace('.json','')
#         all_data.append(data)

# solr.add(all_data)

# solr.add([
#     {
#         "id": "doc_1",
#         "title": "A test document",
#     },
#     {
#         "id": "doc_2",
#         "title": "The Banana: Tasty or Dangerous?",
#         "_doc": [
#             { "id": "child_doc_1", "title": "peel" },
#             { "id": "child_doc_2", "title": "seed" },
#         ]
#     },
# ], commit=True)

# # You can index a parent/child document relationship by
# # associating a list of child documents with the special key '_doc'. This
# # is helpful for queries that join together conditions on children and parent
# # documents.

# # Later, searching is easy. In the simple case, just a plain Lucene-style
# # query is fine.
# results = solr.search('question:"I" question:"got" question:"the" question:"varicella" question:"booster" question:"2" question:"months" question:"ago" question:"and" question:"when" question:"I" question:"recently" question:"got" question:"my" question:"blood" question:"titers" question:"drawn" question:"it"  OR subject_1_immunization:"Generic"^1.05 OR subject_2_vaccination_general:"Booster"^1.05 OR subject_person:"Unknown"^1.05')

# # The ``Results`` object stores total results found, by default the top
# # ten most relevant results and any additional data like
# # facets/highlighting/spelling/etc.
# print("Saw {0} result(s).".format(len(results)))

# # Just loop over it to access the results.
# for result in results:
#     print(result)



# # For a more advanced query, say involving highlighting, you can pass
# # additional options to Solr.
# results = solr.search('title:banana', **{
#     'hl': 'true',
#     'hl.fragsize': 10,
# })

# for result in results:
#     print("The title is '{0}'.".format(result['title']))

# import requests

# link = "http://solr-test-zookeeper-cluster.apps.who.lxp.academy.who.int/solr/admin/collections?action=LIST&wt=json"

# # x = requests.get(link)


# # link = "http://solr-test-zookeeper-cluster.apps.who.lxp.academy.who.int/solr/admin/collections"
# # x = requests.get(link,{"action":"LIST","wt":"json"})


# # solr = pysolr.Solr("http://solr-test-zookeeper-cluster.apps.who.lxp.academy.who.int/solr/qa_999_1", always_commit=True)
# # results = solr.search('*:*')
# # len_ = 0
# # for result in results:
# #     # print(result)
# #     len_ += 1

# # def new_func(project_id, version_id, prev_versions):
# #     solr_server_link = "http://solr-test-zookeeper-cluster.apps.who.lxp.academy.who.int"
# #     link = "http://solr-test-zookeeper-cluster.apps.who.lxp.academy.who.int/solr/admin/collections"
# #     x = requests.get(link,{"action":"LIST","wt":"json"})
# #     prev_versions = [str(x) for x in prev_versions]
    
# #     docs_to_add = []
# #     for collection in x.json()['collections']:
# #         if 'qa' in collection:
# #             project_id_new, version_id_new = collection.split('_')[1:]

# #             if str(project_id_new) == str(project_id) and str(version_id_new) in prev_versions:
# #                 # copy all documents
# #                 index_url = solr_server_link + "/solr/" + collection
# #                 solr = pysolr.Solr(index_url)

# #                 results = solr.search("*:*")
# #                 docs = [x for x in results]
                
# #                 docs_to_add.extend(docs)

# #     for x in docs_to_add:
# #         x.pop('_version_')
    
    

            

# # new_func(1,1, prev_versions=[1,2])
# # # link = "http://solr-test-zookeeper-cluster.apps.who.lxp.academy.who.int/solr/admin/collections"
# # # x = requests.get(link,{"action":"CREATE","name":"testCollection1","numShards":"2"})


# link = "http://solr-test-zookeeper-cluster.apps.who.lxp.academy.who.int/solr/qa_999_1/schema/dynamicfields?wt=json"

# x = requests.get(link)

# pdb.set_trace()


# Create a collection with 1 replica



# change number of replicas to 2 - 3 - 4 -> 10

# Do locust load test