#!/usr/bin/env python3

from bs4 import BeautifulSoup
import decorating as dc
from decorating.color import colorize
from oiprog_helper import thailandoi, oichecklist, codeforces
from oiprog_helper.config import set_config, init, sites
from oiprog_helper.style import txt, number, error, help, msg
import sys
from tinydb import TinyDB, Query, where

@dc.writing(delay=0.005)
def printer(res) :
    if res == None :
        return
    # try :
    for site in sites :
        if site['name'] in res :
            site['lib'].display(res[site['name']])
    # except :
    #     print("\nCancelled")

def Crawl () :
    try :
        res = {}

        db = TinyDB('/usr/local/bin/oiprog.json')
        Config = Query()
        
        for site in sites : 
            data = db.search(Config[site['name']].exists())[0][site['name']]
            if (data['display']) :
                with dc.animated(msg[site['name']]) :
                    res[site['name']] = site['lib'].get()

        return res
    except Exception as e :
        # print(e)
        error()
        return 

if len(sys.argv) > 1 :
    if len(sys.argv) == 2 and sys.argv[1] == 'config' :
        set_config()
    elif len(sys.argv) == 2 and sys.argv[1] == 'init' :
        init()
    elif len(sys.argv) == 2 and sys.argv[1] == 'help' :
        help()
    else :
        print("Command not found : `oiprog help` to learn more")
else :

    printer(Crawl())
