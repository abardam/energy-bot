import markov
import parse

txt_order = 6
msg_order = 2

class SkypeMarkov:
    def __init__(self):
        self.names = dict()  # key: skype ID; values: (char as id, worddict)
        self.chrnames = dict() # points to the same values as names but with chr id as key
        self.msgdict = dict()
        self.curr_id = ''

    def load_skype(self, filename):
        chrid = ''
        for name, msg in parse.parse_skype_log(filename):
            if name not in self.names:
                nchr = chr(len(self.names))
                ndict = dict()
                self.names[name] = (nchr, ndict)
                self.chrnames[nchr] = (name, ndict)
            chrid += self.names[name][0]
            markov.update_dictionary(self.names[name][1], txt_order, msg)
        markov.update_dictionary(self.msgdict, msg_order, chrid)

    def generate(self):
        msg_id = markov.next_char(self.msgdict, self.curr_id)
        self.curr_id = (self.curr_id + msg_id)[-msg_order:]
        nmsg = markov.generate(self.chrnames[msg_id][1], txt_order, 10000).next()
        nname = self.chrnames[msg_id][0]
        return nname, nmsg




