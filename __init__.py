from binaryninja import *
from flowgraph import *

def __flowgraph(bv, function):
    flowgraph = BinocularsFlowgraph(bv, None)
    flowgraph.start()

def __flowgraph_to_function(bv, function):
    flowgraph = BinocularsFlowgraph(bv, function)
    flowgraph.start()


PluginCommand.register_for_function("[BINoculars] Flowgraph (all)", "", __flowgraph)
PluginCommand.register_for_function("[BINoculars] Flowgraph (this function)", "", __flowgraph_to_function)




