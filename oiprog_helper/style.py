import decorating as dc
from decorating.color import colorize
from ascii_graph import Pyasciigraph
from ascii_graph.colors import *
from ascii_graph.colordata import vcolor, hcolor

msg = {
    'thailandoi' : "Crawling back to you~",
    "oichecklist" : "We bout to go up, baby up we go~",
    "codeforces" : "let it be~"
}

theme = 'my99n'

themes = {
    'codeforces' : {
        'text' : ('gray', 'bold'),
        'number' : ('yellow', 'underline'),
        'error' : ('red', 'bold'),
        'symbol' : ':',
        'chart' : [Yel, Blu, Red]
    }, 
    'my99n' : {
        'text' : ('gray', 'bold'),
        'number' : ('pink', 'underline'),
        'error' : ('red', 'bold'),
        'symbol' : '|',
        'chart' : [ICya, IGre, IYel, IRed, IBlu, IPur]
    },
    'autoratch' : {
        'text' : ('gray', 'bold'),
        'number' : ('cyan', 'underline'),
        'error' : ('red', 'bold'),
        'symbol' : ':',
        'chart' : [Gre, Whi, Cya, Whi]
    }
}

def txt(str) :
    return colorize(str, themes[theme]['text'][0], themes[theme]['text'][1])

def number (str) :
    return colorize(str, themes[theme]['number'][0], themes[theme]['number'][1])

@dc.writing(delay=0.02)
def error () :
    print(colorize("There's an error in the process, please config and try again", themes[theme]['error'][0], themes[theme]['error'][1]))

def chart (tochart) :
    chart = Pyasciigraph(graphsymbol=themes[theme]['symbol'])
    data = vcolor(tochart, themes[theme]['chart'])
    for line in chart.graph(label=None, data=data):
        print(line)

def help () :
    print("This is OIPROG")
    print("A cli application to keep oi status in track")
    print("If you are new, please do " + colorize("oiprog init", 'red'))
    print("If you want to go to settings, please do " + colorize("oiprog config", 'red'))
    print("If you have already set the configurations, please do " + colorize("oiprog", 'red'))
    print("If there're any problems, please contact us at " + colorize('github.com/vzsky/OI_Progress', 'yellow'))