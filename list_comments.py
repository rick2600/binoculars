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
                content += ("  0x%x  " %(int(address))).center(80, '=') + "\n"
                content += comment + "\n\n"

        show_plain_text_report("Binoculars List Comments", content)


    def run(self):
        self.multi_line()
