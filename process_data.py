import json
import nltk

# QUERY is an int, indicating the number of top words to be found
def find_top_words (file_name, QUERY):
    with open(file_name) as json_file:  
        data = json.load(json_file)

        """
        for p in data['professor']:
            print("name is " + p['name'])
            print("school is " + p['school'])
            print("department is " + p['department'])
            print("scores are " + str(p['overall']))
            print("comments are " + str(p['comments']))
        """
        subject = {} # Key is subject, value is a list of [adj, freq]
        temp = {}    # Key is subject, value is a list of adj
        adj = {}     # Key is adj, value is frequency
        for p in data['professor']:
            if not p['department'] in subject:
                subject[p['department']] = []
                temp[p['department']] = []

            for comment in p['comments']:
                tokens = nltk.word_tokenize(comment)
                tagged = nltk.pos_tag(tokens)
                for each in tagged:
                    if each[1] == 'JJ' or each[1] == "JJR" or each[1] == "JJS":
                        curr = each[0].lower()
                        if not curr in temp[p['department']]:
                            temp[p['department']].append(curr)
                            subject[p['department']].append([curr, 1])
                        else:
                            index = temp[p['department']].index(curr)
                            subject[p['department']][index][1] += 1

                        if not curr in adj:
                            adj[curr] = 1
                        else:
                            adj[curr] += 1

        for key,val in subject.items():
            val.sort(key=lambda x: x[1], reverse=True)
            print("\nSubject: " + key)
            print("Top QUERY words for this subject: ")
            for i in range(min(len(val), QUERY)):
                print(val[i])

        i = 1
        print("\nTOP QUERY WORDS FOR ALL")
        for key, value in sorted(adj.items(), key=lambda x: (-x[1], x[0])):
            print((key, value))
            if i == QUERY:
                break
            i += 1

# QUERY is a list of words to be investigated
def find_query_words (file_name, QUERY):
    with open(file_name) as json_file:  
        data = json.load(json_file)

        """
        for p in data['professor']:
            print("name is " + p['name'])
            print("school is " + p['school'])
            print("department is " + p['department'])
            print("scores are " + str(p['overall']))
            print("comments are " + str(p['comments']))
        """
        subject = {} # Key is subject, value is a list of [adj, freq]
        temp = {}    # Key is subject, value is a list of adj
        count = {}
        adj = {}     # Key is adj, value is frequency
        for p in data['professor']:
            if not p['department'] in subject:
                subject[p['department']] = []
                count[p['department']] = 1
                temp[p['department']] = []
            else:
                count[p['department']] += 1

            for comment in p['comments']:
                tokens = nltk.word_tokenize(comment)
                tagged = nltk.pos_tag(tokens)
                for each in tagged:
                    curr = each[0].lower()
                    if curr in QUERY:
                        if not curr in temp[p['department']]:
                            temp[p['department']].append(curr)
                            subject[p['department']].append([curr, 1])
                        else:
                            index = temp[p['department']].index(curr)
                            subject[p['department']][index][1] += 1

                        if not curr in adj:
                            adj[curr] = 1
                        else:
                            adj[curr] += 1

        for key,val in subject.items():
            res = []
            val.sort(key=lambda x: x[1], reverse=True)
            res.append(key)
            res.append(str(count[key]))
            res.append(0)
            res.append(0)
            for i in range(len(val)):
                if val[i][0] == "funny":
                    res[2] += val[i][1]
                else:
                    res[3] += val[i][1]

            print(res[0] +"\t" +  res[1] + "\t" + str(res[2]) + "\t" + str(res[3]))

        
        print("\n\n----------")
        for key, value in sorted(adj.items(), key=lambda x: (-x[1], x[0])):
            print((key, value))

        print("There are " + str(len(subject)) + " subjects.")
        print("There are " + str(len(data['professor'])) + " professors.")

#find_top_words("data.json", 35)
find_query_words("data_0704_3pm.json", ["funny", "hilarious"])
