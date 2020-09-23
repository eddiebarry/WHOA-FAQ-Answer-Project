import pickle

if __name__ == '__main__':
    with open('./reranked_data.pkl','rb') as f:
        rerank_test = pickle.load(f)
    
    accuracy = 0
    total = 0
    for x in rerank_test:
        query_string = x[0]
        master_question = x[1]
        hits = x[2]

        selected = hits[:5]
        for x in selected:
            if master_question == x[1]:
                accuracy +=1
                break
        
        print(query_string)
        # print(master_question)
        print('$'*20)
        total += 1
    
    print(accuracy, total, accuracy/total)
                