from binaryninja import *
import graphviz
import tempfile
import os

# reference: http://matthiaseisen.com/articles/graphviz/

class BinocularsFlowgraph(BackgroundTaskThread):

    def __init__(self, bv, function, *args, **kwargs):
        BackgroundTaskThread.__init__(self, '', True)
        self.progress = "Binoculars Flowgraph Running..."
        self.bv = bv
        self.function = function

    def get_styles(self, label):
        styles = {
            'graph': {
                'label': label,
                'fontsize': '16',
                'fontcolor': 'white',
                #'bgcolor': '#333333',
                'bgcolor': '#101010',                
                #'rankdir': 'LR',
            },
            'nodes': {
                'fontname': 'Helvetica',
                'shape': 'box',
                'fontcolor': 'white',
                'color': 'white',
                'style': 'filled',
                'fillcolor': '#006699',
            },
            'edges': {
                #'style': 'dashed',
                'color': 'white',
                'arrowhead': 'open',
                'fontname': 'Courier',
                'fontsize': '12',
                'fontcolor': 'white',
            }
        }
        return styles

    def apply_styles(self, graph, styles):
        graph.graph_attr.update(('graph' in styles and styles['graph']) or {})
        graph.node_attr.update(('nodes' in styles and styles['nodes']) or {})
        graph.edge_attr.update(('edges' in styles and styles['edges']) or {})
        return graph        

    def view_flowgraph_to_bin(self):        
        g = graphviz.Digraph(format='png')
        flowgraph = self.build_flowgraph_to_bin()
        for node in flowgraph.keys():
            g.node(node)
            dst = node
            for src in flowgraph[dst]: 
                g.edge(src, dst)

        styles = self.get_styles('flowgraph')
        g = self.apply_styles(g, styles)
        g.view()

    def view_flowgraph_to_function(self):        
        g = graphviz.Digraph(format='png')
        filename = "%s-%s" % (os.path.basename(self.bv.file.filename), self.function.symbol.name)
        fullpath = os.path.join(tempfile.gettempdir(), filename)
        
        flowgraph = {}
        self.build_flowgraph_to_function_recursive(self.function, flowgraph)
        for node in flowgraph.keys():
            g.node(node)
            dst = node
            for src in flowgraph[node].keys():
                for xref_addr in flowgraph[node][src]:
                    g.edge(src, dst, label=hex(xref_addr).replace("L", ""))
        styles = self.get_styles("flowgraph '%s'" % filename)
        g = self.apply_styles(g, styles)
        filename = "%s.png" % self.function.symbol.name

        filename = "%s-%s" % (os.path.basename(self.bv.file.filename), self.function.symbol.name)
        fullpath = os.path.join(tempfile.gettempdir(), filename)
        g.render(fullpath)

        output = """
        <html>
        <title></title>
        <body>
        <div align='center'>
            <img src='%s.png'/>
        </div>
        <body>
        </html>
        """ % (fullpath)
        show_html_report("Binoculars Flowgraph (this function)", output)
        #print flowgraph

    def build_flowgraph_to_bin(self):
        flowgraph = {}
        for function in self.bv.functions:
            flowgraph[function.symbol.name] = []
            for xref in self.bv.get_code_refs(function.symbol.address):
                if xref.function.symbol.name not in flowgraph[function.symbol.name]:
                    flowgraph[function.symbol.name].append(xref.function.symbol.name)
        return flowgraph


    def build_flowgraph_to_function_recursive(self, function, flowgraph):
        if function.symbol.name not in flowgraph.keys():
            flowgraph[function.symbol.name] = {}

        for xref in self.bv.get_code_refs(function.symbol.address):
            if xref.function.symbol.name not in flowgraph[function.symbol.name].keys():
                flowgraph[function.symbol.name][xref.function.symbol.name] = []
            if xref.address not in flowgraph[function.symbol.name][xref.function.symbol.name]:
                flowgraph[function.symbol.name][xref.function.symbol.name].append(xref.address)
            self.build_flowgraph_to_function_recursive(xref.function, flowgraph)

    def run(self):
        if self.function == None:
            self.view_flowgraph_to_bin()
        else:
            self.view_flowgraph_to_function()
