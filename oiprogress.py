#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import json
import re
import decorating as dc
from decorating.color import colorize


config = {
    "name" : "my99n",
    "thailandoi" : {
        "display" : True,
        "user" : "user09",
        "pwd" : "amoyc",
        "authen_token" : "ypRMh70pJkGNfWyAgTEWKk4iNgw9J63UlDv1i44WRPPUqtXKhFWgce51zDkddPIpkPA7LizyxKeVUHyZ1JrVuw%3D%3D",
    },
    "oichecklist" : {
        "display" : True,
        "url" : "https://oichecklist.pythonanywhere.com/view/3c02e91ff695852116eb474380831f2f6735b3ae/"
    }
}

def txt(str) :
    return colorize(str, 'yellow', 'bold')

def number (str) :
    return colorize(str, 'red', 'underline')

@dc.writing(delay=0.02)
def error () :
    print(colorize("There's an error in the process, please config and try again", "red", "bold"))

@dc.writing(delay=0.02)
def printer(a) :
    if (config['thailandoi']['display']) :
        print(txt("From evaluator.thailandoi.org of " + config['name']))
        print(txt("Did solve problems worth ") +number(a['thailandoi'][0])+ txt(" points"))
        print(txt("From overall of ") +number(a['thailandoi'][1])+ txt(" points"))
        progress = a['thailandoi'][0]*100/a['thailandoi'][1]
        print(txt("Solved ") + number("%.2f %%" % progress) + txt(" of all tasks"))
        print()

    if (config['oichecklist']['display']) :
        print(txt("From oichecklist of "+config['name']))
        print(txt("Did solve ") +number(a['oichecklist'][0])+ txt(" OI problems"))
        print(txt("Solved ") +number(str(a['oichecklist'][1])+" %")+ txt(" of all tasks"))
        print()

def Crawl () :
    try :
        crawl  = requests.get(config['thailandoi']['url']).content
        soup = BeautifulSoup(crawl, features="html.parser")
        soup.prettify()

        res = {}

        if (config['thailandoi']['display']) :
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

            res['thailandoi'] = [sumEva, overallEva]

        if (config['oichecklist']['display']) :
            crawl  = requests.get(config['oichecklist']['url']).content
            soup = BeautifulSoup(crawl, features="html.parser")
            soup.prettify()

            main = soup.find("div", {"class" : "container", "role" : "main"})
            solved = main.find("h3").contents[0].split(' ')[2]
            progressbar = soup.find("div", {"role" : "progressbar"})
            ratio = progressbar['aria-valuenow']

            res['oichecklist'] = [solved, ratio]

        return res
    except :
        return -1

config['thailandoi']['url'] = 'https://evaluator.thailandoi.org/login/login?utf8=%E2%9C%93&authenticity_token='+config['thailandoi']['authen_token']+'&login='+config['thailandoi']['user']+'&password='+config['thailandoi']['pwd']+'&commit=Login'

with dc.animated("Crawling back to you~") :
    res = Crawl()
    
if res == -1 :
    error()
else :
    printer(res)