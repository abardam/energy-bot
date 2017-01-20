import re

skype_pattern = '''\[[0-9]+\/[0-9]+\/[0-9]+ [0-9]+\:[0-9]+\:[0-9]+ [AP]M(?:.+M)?\] ([^:]*): (.*)'''
compiled_skype_pattern = re.compile(skype_pattern)

# parse skype logs

def parse_skype_log(filename):
    with open(filename, 'r', encoding='utf-8') as fin:
        for line in fin:
            m = compiled_skype_pattern.match(line)
            if m is not None:
                name = m.group(1)
                msg = m.group(2)

                # if name not in nmdict:
                #     nmdict[name] = []
                # nmdict[name].append(msg)
                yield (name, msg)
