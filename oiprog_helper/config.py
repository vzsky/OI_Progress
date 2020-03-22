from pick import pick
from tinydb import TinyDB, Query, where

TOI_TOKEN = token = "ypRMh70pJkGNfWyAgTEWKk4iNgw9J63UlDv1i44WRPPUqtXKhFWgce51zDkddPIpkPA7LizyxKeVUHyZ1JrVuw%3D%3D"

def gather_toi () :
    token = TOI_TOKEN
    user = input("What is your username? ")
    pwd = input("What is your password? (We don't hash) ")
    toi = {'user' : user, 'pwd' : pwd, 'display' : True,
        'authen_token' : token,
        'url' : 'https://evaluator.thailandoi.org/login/login?utf8=%E2%9C%93&authenticity_token='+token+'&login='+user+'&password='+pwd+'&commit=Login'
    }
    return toi

def thailandoi (db) :
    token = TOI_TOKEN

    title = "Do you want to enable evaluator thailandoi? (can change)"
    options = ['Yes', 'No']
    option, index = pick(options, title,  indicator='>')
    toi = {}
    if (index == 0) :
        toi = gather_toi()
    if (index == 1) :
        toi = {'user' : None, 'pwd' : None, 'display' : False,
            'authen_token' : token,
            'url' : None
        }
    db.insert({'thailandoi' : toi})
    return

def gather_oic () :
    url = input("What is your url of the oichecklist? ")
    oic = { 'url' : url, 'display' : True }
    return oic

def oichecklist (db) :
    title = "Do you want to enable oichecklist? (can change)"
    options = ['Yes', 'No']
    option, index = pick(options, title,  indicator='>')
    oic = {}
    if index == 0 : 
        oic = gather_oic()
    if index == 1 :
        oic = { 'url' : None, 'display' : False }
    db.insert({'oichecklist' : oic})
    return

def gather_cf () :
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

def codeforces (db) :
    title = "Do you want to enable codeforces? (can change)"
    options = ['Yes', 'No']
    option, index = pick(options, title,  indicator='>')
    cf = {}

    if index == 0 : 
        cf = gather_cf()
    if index == 1 :
        cf = { 'handle' : None, 'display' : False, 'displaychart' : None, 'urlstatus' : None, 'urlrating' : None}
    db.insert({'codeforces' : cf})
    return 

def init () :
    db = TinyDB('./db.json')
    Config = Query()
    if len(db.search(where('valid') == 1)) == 1 :
        return
    
    print("What can I call you?")
    name = input()
    db.insert({'name' : name})

    thailandoi(db)
    oichecklist(db)
    codeforces(db)

    db.insert({'valid' : 1})

def set_config () :

    db = TinyDB('./db.json')
    Config = Query()
    
    title = "what's up! what do you want?"
    options = ['toggle display', 'config sites', 'change name', 'view config', 'cancel']
    option, index = pick(options, title,  indicator='>')
    if index == 0 :
        while True :
            title1 = "Which one ?"
            options1 = ['thailandoi', 'oichecklist', 'codeforces', 'done']
            option1, index1 = pick(options1, title1,  indicator='>')
            if (index1 == 3) :
                break
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
        options1 = ['thailandoi', 'oichecklist', 'codeforces', 'done']
        option1, index1 = pick(options1, title1,  indicator='>')
        now = {}
        if (option1 == 'thailandoi') :
            now = gather_toi()
        if (option1 == 'oichecklist') :
            now = gather_oic()
        if (option1 == 'codeforces') :
            now = gather_cf()
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
            toi = db.search(Config.thailandoi.exists())[0]['thailandoi']
            oic = db.search(Config.oichecklist.exists())[0]['oichecklist']
            cf = db.search(Config.codeforces.exists())[0]['codeforces']
            strmap = {'True' : 'enabled', 'False' : 'disabled'}
            print("Your name is " + name)
            print()
            print("Evaluator Thailandoi : " + strmap[str(toi['display'])])
            print("user : " + str(toi['user']))
            print("pwd : " + str(toi['pwd']))
            print()
            print("Oichecklist : " + strmap[str(oic['display'])])
            print("url : " + str(oic['url']))
            print()
            print("Codeforces : " + strmap[str(cf['display'])])
            print("handle : " + str(cf['handle']))
            if cf['displaychart'] :
                print("You wanted to see rating distribution of solved tasks")
            return
        except :
            print("failed : please do `oiprog init` first.")
    if index == 4 :
        return
    
