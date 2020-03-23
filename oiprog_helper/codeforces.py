import requests
from bs4 import BeautifulSoup
from tinydb import TinyDB, Query, where
from .style import txt, number, chart
import decorating as dc
import json
from collections import Counter, OrderedDict
from pick import pick

def get () :
    try :
        db = TinyDB('/usr/local/bin/oiprog.json')
        Config = Query()
        cf = db.search(Config.codeforces.exists())[0]['codeforces']

        crawl  = requests.get(cf['urlstatus']).content
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

        crawl  = requests.get(cf['urlrating']).content
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
        
    db = TinyDB('/usr/local/bin/oiprog.json')
    Config = Query()
    cf = db.search(Config.codeforces.exists())[0]['codeforces']
    name = db.search(Config.name.exists())[0]['name']

    if cf['display'] :
        print(txt("From codeforces of " + name))
        print(txt("have solved ")+ number(res[0])+ txt(" problems in total"))

        if cf['displaychart'] :
            print(txt("this is solved problems rating distr."))
            solved_ratings = Counter(res[1])
            tochart = [ (s, solved_ratings[s]) for s in solved_ratings if s != None] 
            chart(sorted(tochart))

        print(txt("Rating of this codeforces id is now ") + number(res[2]))
        print()

def gather_user () :
    handle = input("What's your codeforces handle? ")
    title = "Do you want to enable codeforces rating distribution of solved tasks? (can change)"
    options = ['Yes', 'No']
    option, index2 = pick(options, title,  indicator='>')
    dis = None
    if (index2 == 0) :
        dis = True
    else :
        dis = False
    cf = { 'handle' : handle, 'display' : True, 'displaychart' : dis, 
        'urlstatus' : 'https://codeforces.com/api/user.status?handle='+handle,
        'urlrating' : 'https://codeforces.com/api/user.rating?handle='+handle
    }
    return cf

def init (db) :
    title = "Do you want to enable codeforces? (can change)"
    options = ['Yes', 'No']
    option, index = pick(options, title,  indicator='>')
    cf = {}

    if index == 0 : 
        cf = gather_user()
    if index == 1 :
        cf = { 'handle' : None, 'display' : False, 'displaychart' : None, 'urlstatus' : None, 'urlrating' : None}
    db.insert({'codeforces' : cf})
    return 

def showconfig (db) :
    cf = db.search(Query().codeforces.exists())[0]['codeforces']
    strmap = {'True' : 'enabled', 'False' : 'disabled'}
    print("Codeforces : " + strmap[str(cf['display'])])
    print("handle : " + str(cf['handle']))
    if cf['displaychart'] :
        print("You wanted to see rating distribution of solved tasks")