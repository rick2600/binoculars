from binaryninja import *


class BinocularsTextifyFunction(BackgroundTaskThread):

    def __init__(self, bv, function, *args, **kwargs):
        BackgroundTaskThread.__init__(self, '', True)
        self.progress = "Binoculars Textifying Function"
        self.bv = bv
        self.function = function


    def textify_function_plain(self):
        output = ''    
        basic_blocks = sorted(self.function.basic_blocks, key=lambda bb: bb.start)
        
        for basic_block in basic_blocks:
            for inst in basic_block.get_disassembly_text():
                if str(inst.tokens[0]) == self.function.name: continue
                
                addr = hex(inst.address).replace("L", "")
                offset = inst.address - self.function.start
                output += "%s <%s+%d>:    %s\n" %\
                (addr, self.function.name, offset, str(inst))

        print output                
        show_plain_text_report("Binoculars Text Disasm", output)


    # TODO: syntax highlight
    def textify_function_html(self):
        output = ''    
        basic_blocks = sorted(self.function.basic_blocks, key=lambda bb: bb.start)
        
        for basic_block in basic_blocks:
            for inst in basic_block.get_disassembly_text():
                if str(inst.tokens[0]) == self.function.name: continue
                
                addr = hex(inst.address).replace("L", "")
                offset = inst.address - self.function.start
                output += "%s <%s+%d>:    %s\n" %\
                (addr, self.function.name, offset, str(inst))

        html = """
        <html>
        <head></head>
        <body>
        %s
        </body>
        </html>
        """ %(output)
        print html                
        show_html_report("Binoculars Text Disasm", output)        


    def run(self):
        #self.textify_function_html()
        self.textify_function_plain()



