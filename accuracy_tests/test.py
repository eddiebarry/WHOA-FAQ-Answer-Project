import pickle

if __name__ == '__main__':
    rerank = [
        './intermediate_results/pure_search_5_0.757.p',
        "./intermediate_results/reranked_search_10_0.816.p",
        "./intermediate_results/reranked_search_50_0.905.p",
        "./intermediate_results/reranked_search_100_0.944.p",
    ]
    for path in rerank:
        with open(path,'rb') as f:
            rerank_test = pickle.load(f)
        
        accuracy = 0
        total = 0
        for x in rerank_test:
            query_string = x[0]
            master_question = x[1]
            hits = x[2]

            selected = hits[:5]
            for y in selected:
                if master_question == y[1]:
                    accuracy +=1
                    break
            
            # print(query_string)
            # # print(master_question)
            # print('$'*20)
            total += 1

        print(path)
        print(accuracy, total, accuracy/total)
                