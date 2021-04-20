import requests, pdb

solr_server_link = "http://solr-test-zookeeper-cluster"+\
    ".apps.who.lxp.academy.who.int"

collection_url = solr_server_link + "/solr/admin/collections"

for x in range(0,10,2):
    new_name = str(x+2)+"_replicas"
    x = requests.get(collection_url,\
                {"action":"CREATE","name":new_name,"numShards":"1","replicationFactor":x+2})

    print(new_name,"created")
    print(x.json())