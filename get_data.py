import requests
from bs4 import BeautifulSoup
import time
import json

data = {}
data['professor'] = []

orig = 'http://www.ratemyprofessors.com/ShowRatings.jsp?tid='

for i in range(50, 9999):
    try:
        url = orig + str(i) 
        body = requests.get(url).text
        soup = BeautifulSoup(body, 'lxml')

        if str(soup.title).find("School Reviews") != -1:
            continue

        # This gives the professor's name and their university
        name = str(soup.title).split(">")[1].split("at")[0]

        # This gives department, university and location
        info = str(soup.find_all(attrs={"class" : "result-title"}))
        dept = info.split("Professor in the")[1].split("department")[0].strip()


        # This gives university and location
        info = str(soup.find_all(attrs={"class" : "schoolname"}))
        info = info.split(">")
        school = info[2].split("<")[0]
        location = info[3].lstrip(", ").split("</")[0]


        overall = []
        difficulty = []
        # This gives the overall score and level of difficulty 
        for item in soup.find_all(attrs={"class" : "descriptor-container"}):
            curr = str(item)
            score = curr.split("span")[1].split("\">")[1].split("</")[0]
            if len(overall) > len(difficulty):
                difficulty.append(score)
            else:
                overall.append(score)

        comments = []
        # This gives the students' comments
        raw_comment = soup.find_all(attrs={"class" : "commentsParagraph"})
        for each in raw_comment:
            curr = str(each)
            curr = curr.replace("<p class=\"commentsParagraph\">", "")
            curr = curr.lstrip()
            curr = curr.rstrip("</p>")
            curr = curr.rstrip()
            comments.append(curr)

        data['professor'].append({
            'url' : url,
            'name': name,
            'school' : school,
            'department' : dept,
            'location' : location,
            'overall' : overall,
            'difficulty' : difficulty,
            'comments' : comments,
            })
        
        print("success in retriving " + str(i))
        time.sleep(1)
    except:
        continue

with open('data_0704_3pm.json', 'w') as outfile:  
    json.dump(data, outfile)
