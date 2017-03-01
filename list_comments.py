from binaryninja import *


class BinocularsListComments(BackgroundTaskThread):

    def __init__(self, bv, *args, **kwargs):
        BackgroundTaskThread.__init__(self, '', True)
        self.progress = "Binoculars Collecting User Comments..."
        self.bv = bv

    def do_formatting(self, comment):
        return comment.replace("\n", "\\n")

    def multi_line(self):
        content = ""
        for function in self.bv.functions:
            for address, comment in function.comments.iteritems():
                content += "Address: 0x%x\n" %(int(address))
                content += comment 
                content += "\n"
                content += "=" * 80
                content += "\n\n"

        show_plain_text_report("Binoculars List Comments", content)


    def run(self):
        self.multi_line()
