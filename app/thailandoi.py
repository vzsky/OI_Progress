import requests
from bs4 import BeautifulSoup
from tinydb import TinyDB, Query, where
from style import txt, number
import decorating as dc
from pick import pick
import os, pathlib
__dir = pathlib.Path(__file__).parent.parent.absolute()

def get () :
    try :
        db = TinyDB(os.path.join(__dir,'oiprog.json'))
        Config = Query()
        toi = db.search(Config.thailandoi.exists())[0]['thailandoi']

        crawl  = requests.get(toi['url']).content
        soup = BeautifulSoup(crawl, features="html.parser")
        soup.prettify()
        tasks = soup.find("div", {"class": "col-md-7"})
        tasks = tasks.find_all("tr")

        sumEva = 0
        overallEva = 0

        for task in tasks[1::] :
            task = task.find_all("td")
            score = task[3]
            if len(score.contents) == 1 :
                continue
            score = score.contents[6].split('\n')
            score = int(score[1])
            if score > 100 :
                score = 100
            sumEva += score

        overallEva = (len(tasks)-1)*100

        return [sumEva, overallEva]
    except Exception as e :
        raise e

def display (res) :
    if res == None :
        return

    db = TinyDB(os.path.join(__dir,'oiprog.json'))
    Config = Query()
    toi = db.search(Config.thailandoi.exists())[0]['thailandoi']
    name = db.search(Config.name.exists())[0]['name']

    if (toi['display']) :
        print(txt("From evaluator.thailandoi.org of " + name))
        print(txt("Did solve problems worth ") +number(res[0])+ txt(" points"))
        print(txt("From overall of ") +number(res[1])+ txt(" points"))
        progress = res[0]*100/res[1]
        print(txt("Solved ") + number("%.2f %%" % progress) + txt(" of all tasks"))
        print()

TOI_TOKEN = token = "ypRMh70pJkGNfWyAgTEWKk4iNgw9J63UlDv1i44WRPPUqtXKhFWgce51zDkddPIpkPA7LizyxKeVUHyZ1JrVuw%3D%3D"

def gather_user () :
    token = TOI_TOKEN
    user = input("What is your username? ")
    pwd = input("What is your password? (We don't hash) ")
    toi = {'user' : user, 'pwd' : pwd, 'display' : True,
        'authen_token' : token,
        'url' : 'https://evaluator.thailandoi.org/login/login?utf8=%E2%9C%93&authenticity_token='+token+'&login='+user+'&password='+pwd+'&commit=Login'
    }
    return toi

def init (db) :
    token = TOI_TOKEN

    title = "Do you want to enable evaluator thailandoi? (can change)"
    options = ['Yes', 'No']
    option, index = pick(options, title,  indicator='>')
    toi = {}
    if (index == 0) :
        toi = gather_user()
    if (index == 1) :
        toi = {'user' : None, 'pwd' : None, 'display' : False,
            'authen_token' : token,
            'url' : None
        }
    db.insert({'thailandoi' : toi})
    return

def showconfig (db) :
    toi = db.search(Query().thailandoi.exists())[0]['thailandoi']
    strmap = {'True' : 'enabled', 'False' : 'disabled'}
    print("Evaluator Thailandoi : " + strmap[str(toi['display'])])
    print("user : " + str(toi['user']))
    print("pwd : " + str(toi['pwd']))
    print()