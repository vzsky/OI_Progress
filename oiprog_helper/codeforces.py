import requests
from bs4 import BeautifulSoup
from .config import config
from .style import txt, number, chart
import decorating as dc
import json
from collections import Counter, OrderedDict

def get () :
    try :
        crawl  = requests.get(config['codeforces']['urlstatus']).content
        soup = BeautifulSoup(crawl, features='html.parser')
        soup.prettify()

        soup = json.loads(str(soup))

        tasks = [{
            'rating' : s['problem']['rating'],
            'id' : str(s['problem']['contestId'])+s['problem']['index'],
            'verdict' : s['verdict']
        } if 'rating' in s['problem'] 
        else {
            'rating' : None, 
            'id' : str(s['problem']['contestId'])+s['problem']['index'],
            'verdict' : s['verdict']
        }
        for s in soup['result'] ]

        solved = [ {'rating' : task['rating'], 'id' : task['id']} for task in tasks if task['verdict'] == 'OK']
        solved = [dict(s) for s in set(tuple(x.items()) for x in solved)]
        solved_rate = [task['rating'] for task in solved]

        crawl  = requests.get(config['codeforces']['urlrating']).content
        soup = BeautifulSoup(crawl, features='html.parser')
        soup.prettify()

        soup = json.loads(str(soup))['result']
        now_rating = soup[-1]['newRating']

        return [len(solved), solved_rate, now_rating]
        

    except Exception as e :
        raise e

def display (res) :
    if res == None :
        return
    if config['codeforces']['display'] :
        print(txt("From codeforces of " + config['name']))
        print(txt("have solved ")+ number(res[0])+ txt(" problems in total"))

        if config['codeforces']['displaychart'] :
            print(txt("this is solved problems rating distr."))
            solved_ratings = Counter(res[1])
            tochart = [ (s, solved_ratings[s]) for s in solved_ratings if s != None] 
            chart(sorted(tochart))

        print(txt("Rating of this codeforces id is now ") + number(res[2]))
        print()
