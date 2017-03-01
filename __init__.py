from binaryninja import *
from flowgraph import *
from list_comments import *
from textify_function import *



def __flowgraph(bv, function):
    flowgraph = BinocularsFlowgraph(bv, None)
    flowgraph.start()

def __flowgraph_to_function(bv, function):
    flowgraph = BinocularsFlowgraph(bv, function)
    flowgraph.start()

def __list_comments(bv):
    list_comments = BinocularsListComments(bv)
    list_comments.start()

def __textify_function(bv, function):
    textify_function = BinocularsTextifyFunction(bv, function)
    textify_function.start()

PluginCommand.register("[BINoculars] List Comments", "", __list_comments)
PluginCommand.register_for_function("[BINoculars] Textify Function", "", __textify_function)
PluginCommand.register_for_function("[BINoculars] Flowgraph (all)", "", __flowgraph)
PluginCommand.register_for_function("[BINoculars] Flowgraph (this function)", "", __flowgraph_to_function)








