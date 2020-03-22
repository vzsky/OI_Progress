import requests
from bs4 import BeautifulSoup
from .config import config
from .style import txt, number
import decorating as dc

def get () :
    try :
        crawl  = requests.get(config['thailandoi']['url']).content
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
    if (config['thailandoi']['display']) :
        print(txt("From evaluator.thailandoi.org of " + config['name']))
        print(txt("Did solve problems worth ") +number(res[0])+ txt(" points"))
        print(txt("From overall of ") +number(res[1])+ txt(" points"))
        progress = res[0]*100/res[1]
        print(txt("Solved ") + number("%.2f %%" % progress) + txt(" of all tasks"))
        print()