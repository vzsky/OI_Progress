import decorating as dc
from decorating.color import colorize
from ascii_graph import Pyasciigraph
from ascii_graph.colors import *
from ascii_graph.colordata import vcolor, hcolor

def txt(str) :
    return colorize(str, 'gray', 'bold')

def number (str) :
    return colorize(str, 'yellow', 'underline')

@dc.writing(delay=0.02)
def error () :
    print(colorize("There's an error in the process, please config and try again", "red", "bold"))

def chart (tochart) :
    chart = Pyasciigraph(graphsymbol=':')
    pattern = [Yel, Blu, Red]
    data = vcolor(tochart, pattern)
    for line in chart.graph(label=None, data=data):
        print(line)