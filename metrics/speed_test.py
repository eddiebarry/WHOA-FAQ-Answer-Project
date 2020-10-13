import pickle
import os
import timeit
import requests
import numpy as np
import json

# torch.backends.cudnn.benchmark = True
# torch.backends.cudnn.enabled = True
# torch.backends.cudnn.fastest = False

# torch.set_num_threads(1)

base_url="http://18.203.115.216:5007/api/v1/reranking"

gpu_times_dict = {}
for x in sorted(os.listdir("./Search_data/")):
    title = "./Search_data/"+x
    if title.endswith("checkpoints"):
        continue

    batch_size = int(x.split("_")[2])
    
    if batch_size != 50:
        continue

    print("batch size : ", batch_size)


    gpu_times = []

    with open(title,'rb') as f:
        rerank_test = pickle.load(f)

    idx = 0
    accuracy = 0
    total = 0
    for x in rerank_test:
        idx += 1
        query_string = x[0]
        master_question = x[1]
        hits = x[2]
        

        texts = [[0,x[1]] for x in hits]


        start = timeit.default_timer()
        params = {
            "query": query_string,
            "texts": texts,
        }
        r = requests.get(base_url, json=json.dumps(params))
        response  = r.json()
        scoreDocs = response['scoreDocs']

        stop = timeit.default_timer()
        gpu_times.append(stop-start)
	
	#Top 5
        selected = scoreDocs[:5]
        for y in selected:
            if master_question == y[1]:
                accuracy +=1
                break
        total += 1


        if idx%10==0:
            print("mean time : ", np.mean(gpu_times))

        if idx%30== 0:
            print("mean time : ", np.mean(gpu_times[-30:]))
        
        if idx%100==0:
            break
    print(accuracy, total, accuracy/total)


print('$'*80)
print("reranking service done")


base_url="http://0.0.0.0:5006/api/v2/qna"

data_ = [
    {
        "query":"My child was vaccinated recently with MMR for school", 
        "user_id":"-1"
    }
    ,
    {
        "query":"what restrictions are there for immuno compromised people visiting ?",
        "user_id":"2d07dcffc217bf2864ba64fc8b60fdaa41d0b08f74fb522582f1031e77cb2a4fc3b5b0b98392efc0dce2b96f9be453c07373bfecea25964379c422e4f9e89877"
    }
]

times = []
for x in range(30):
    for idx,x in enumerate(data_):
        if idx==1:
            start = timeit.default_timer()
        r = requests.get(base_url, data=json.dumps(x))
        if idx==1:
            stop = timeit.default_timer()
            times.append(stop-start)
print(np.mean(times))