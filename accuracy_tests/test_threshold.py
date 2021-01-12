import pickle, pdb
import matplotlib.pyplot as plt

if __name__ == '__main__':
    rerank = [
        './intermediate_results/pure_search_5_0.757.p',
        # "./intermediate_results/reranked_search_10_0.816.p",
        # "./intermediate_results/reranked_search_50_0.905.p",
        # "./intermediate_results/reranked_search_100_0.944.p",
    ]
    for path in rerank:
        with open(path,'rb') as f:
            rerank_test = pickle.load(f)
        
        accuracy = 0
        total = 0

        acc_scores = []
        in_acc_scores = []
        for x in rerank_test:
            query_string = x[0]
            master_question = x[1]
            hits = x[2]

            acc = False
            selected = hits[:5]
            for y in selected:
                if master_question == y[1]:
                    acc_scores.append(y[0])
                    accuracy +=1
                    acc = True
                    break
            
            if not acc:
                # pdb.set_trace()
                try:
                    in_acc_scores.append(selected[0][0])
                except:
                    y = "yellow"
                    # pdb.set_trace()
            # print(query_string)
            # # print(master_question)
            # print('$'*20)
            # pdb.set_trace()
            total += 1

        print(path)
        print(accuracy, total, accuracy/total)
    
    acc_scores = [x for x in acc_scores if x < 30]
    in_acc_scores = [x for x in in_acc_scores if x < 30]

    fig, ax = plt.subplots()
    ax.hist(acc_scores , 50, None, ec='red', fc='none', lw=1.5, histtype='step', label='n-gram')
    ax.hist(in_acc_scores , 50, None, ec='green', fc='none', lw=1.5, histtype='step', label='ensemble')
    ax.legend(loc='upper left')
    plt.savefig("./scores.png")

    # pdb.set_trace()
                