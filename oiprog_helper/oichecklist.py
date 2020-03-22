import requests
from bs4 import BeautifulSoup
from .config import config
from .style import txt, number
import decorating as dc

def get () :
    try :
        crawl  = requests.get(config['oichecklist']['url']).content
        soup = BeautifulSoup(crawl, features="html.parser")
        soup.prettify()

        main = soup.find("div", {"class" : "container", "role" : "main"})
        solved = main.find("h3").contents[0].split(' ')[2]
        progressbar = soup.find("div", {"role" : "progressbar"})
        ratio = progressbar['aria-valuenow']

        return [solved, ratio]
    except Exception as e :
        raise e

def display (res) :
    if res == None :
        return
    if (config['oichecklist']['display']) :
        print(txt("From oichecklist of "+config['name']))
        print(txt("Did solve ") +number(res[0])+ txt(" OI problems"))
        print(txt("Solved ") +number(str(res[1])+" %")+ txt(" of all tasks"))
        print()