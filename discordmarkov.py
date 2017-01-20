import markov

txt_order = 6
msg_order = 2

class DiscordMarkov:
  def __init__(self, skype_markov, person_defs):
    self.names = dict()  # key: discord ID; values: (char as id, worddict)
    self.chrnames = dict() # points to the same values as names but with chr id as key
    self.msgdict = dict()
    self.curr_id = ''
        
    chrdict = dict()
    
    for k, v in person_defs.items():
      nchr = chr(len(self.names))
      ndict = skype_markov.names[v][1]
      
      self.names[k] = (nchr, ndict)
      self.chrnames[nchr] = (k, ndict)
      chrdict[skype_markov.names[v][0]] = nchr
    
    self.msgdict = markov.replace_letter(skype_markov.msgdict, chrdict)
  
  def update(self, disc_id, disc_msg):
    if disc_id not in self.names:
      nchr = chr(len(self.names))
      ndict = dict()
      self.names[disc_id] = (nchr, ndict)
      self.chrnames[nchr] = (disc_id, ndict)
    markov.update_dictionary(self.names[disc_id][1], txt_order, disc_msg)
  
  def generate(self, discord_id=None, num_msg=1):
    for n in range(num_msg):
      if discord_id is not None:
        msg_id = self.names[discord_id][0]
      else:
        msg_id = markov.next_char(self.msgdict, self.curr_id)
        if msg_id is None:
          self.curr_id = ''
          msg_id = markov.next_char(self.msgdict, self.curr_id)
      self.curr_id = (self.curr_id + msg_id)[-msg_order:]
      nmsg = next(markov.generate(self.chrnames[msg_id][1], txt_order, 10000))
      nname = self.chrnames[msg_id][0]
      yield nname, nmsg