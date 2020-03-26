from pick import pick
from tinydb import TinyDB, Query, where
import thailandoi, oichecklist, codeforces
import os, pathlib
__dir = pathlib.Path(__file__).parent.parent.absolute()

sites = [
    {       
        'name' : 'thailandoi',
        'lib' : thailandoi
    },
    {       
        'name' : 'oichecklist',
        'lib' : oichecklist
    },
    {       
        'name' : 'codeforces',
        'lib' : codeforces
    },
]

siteoption = [site['name'] for site in sites]
siteoption.append('done')

def init () :
    db = TinyDB(os.path.join(__dir,'oiprog.json'))
    Config = Query()
    if len(db.search(where('valid') == 1)) == 1 :
        return
    
    print("What can I call you?")
    name = input()
    db.insert({'name' : name})

    for site in sites :
        site['lib'].init(db)

    db.insert({'valid' : 1})

def set_config () :

    db = TinyDB(os.path.join(__dir,'oiprog.json'))
    Config = Query()
    
    title = "what's up! what do you want?"
    options = ['toggle display', 'config sites', 'change name', 'view config', 'cancel']
    option, index = pick(options, title,  indicator='>')
    try : 
        if index == 0 :
            title1 = "Which one ?"
            option1, index1 = pick(siteoption, title1,  indicator='>')

            if (option1 == 'done') :
                return

            title2 = "Do whats ?"
            options2 = ['enable', 'disable']
            option2, index2 = pick(options2, title2,  indicator='>')
            cond = { 0 : True, 1 : False }
            now = db.search(Config[option1].exists())[0][option1]
            now['display'] = cond[index2]
            db.upsert({option1 : now}, Config[option1].exists())
            return

        if index == 1 :
            title1 = "Which one ?"
            option1, index1 = pick(siteoption, title1,  indicator='>')

            if (option1 == 'done') :
                return

            now = sites[index1]['lib'].gather_user()
            db.upsert({option1 : now}, Config[option1].exists())
            print("We also enabled " + option1 + " for you!")
            return

        if index == 2 :
            print("what's your name?")
            newname = input()
            db.upsert({'name' : newname}, Config.name.exists())
            print("Alright, " + newname)
            return

        if index == 3 :
            try :
                name = db.search(Config.name.exists())[0]['name']
                
                print("Your name is " + name)
                print()

                for site in sites :
                    site['lib'].showconfig(db)
    
                return
            except :
                print("failed : please do `oiprog init` first.")

        if index == 4 :
            return
    except :
        print("Configuration is cancelled")