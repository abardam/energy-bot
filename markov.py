import numpy as np

txt = '''
Lorem Ipsum is simply dummy text of the printing and typesetting industry.
Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.
It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.
It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
'''

wordlen = 6
worddict = dict()


def update_dictionary(worddict, wordlen, txt):
    word = ''
    for c in txt.strip() + '\n':

        word = word[-(wordlen):]
        if word not in worddict:
            worddict[word] = dict()
        if c not in worddict[word]:
            worddict[word][c] = 1
        else:
            worddict[word][c] += 1

        word += c


def next_char(worddict, word):
    if word not in worddict:
        return None
    s = sum(worddict[word].values())
    r = np.random.randint(s)
    for k, v in worddict[word].items():
        if r < v:
            return k
        else:
            r -= v
    return worddict[word].keys()[0]


def generate(worddict, wordlen, txtlen):
    txt = ''
    word = ''
    while len(txt) < txtlen:
        word = word[-(wordlen):]
        c = next_char(worddict, word)
        if c is None:
            word = ''
            c = ''
        elif c == '\n':
            word = ''
            nword = yield txt
            if nword is not None:
                word = nword
            txt = ''
        else:
            word = (word + c)
            txt += c
    yield txt


def combine_worddict(dict1, dict2):
    assert type(dict1) is dict
    assert type(dict2) is dict
    rdict = dict()
    for key, value in dict1.items():
        if key in dict2:
            rdict[key] = combine_segdict(value, dict2[key])
        else:
            rdict[key] = value
    for key, value in dict2.items():
        if key not in dict1:
            rdict[key] = value
    return rdict


def combine_segdict(dict1, dict2):
    rdict = dict()
    for key, value in dict1.items():
        total = value
        if key in dict2:
            total += dict2[key]
        rdict[key] = total
    for key, value in dict2.items():
        if key not in dict1:
            rdict[key] = value
    return rdict


def replace_letter(dict0, kdict):
    rdict = dict()
    for key, value in dict0.items():
        nkey = ''.join(k if k not in kdict else kdict[k] for k in key)
        dict1 = dict()
        for key1, value1 in value.items():
            nkey1 = key1 if key1 not in kdict else kdict[key1]
            dict1[nkey1] = value1
        rdict[nkey] = dict1
    return rdict