import string
import random
import csv
import sys
import numpy
import pickle
import wget
import zipfile
from collections import defaultdict

### Util ###

def get_char_type(char):
    if char in string.ascii_letters:
        return 0
    elif char in string.digits:
        return 1
    else:
        return 2

def get_token_name(token):
    return str(get_char_type(token[0])) + str(len(token))

def write_csv(filename, values):
    with open(filename, 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(values)

def get_prob_distrib(freq_dict):
    total = float(sum(freq_dict.values()))
    token, calib_prob, total_prob = "", defaultdict(float), 0
    for token, freq in freq_dict.iteritems():
        calib_prob[token] = freq/total
        total_prob += calib_prob[token]
    calib_prob[token] = calib_prob[token] + 1 - total_prob
    return calib_prob

### PCFG Parse ###

def parse_string_cfg(s):
    token, state, grammar = " ", 0, []
    transition = [
        #Letter, Digit, Puncutation
        [1, 2, 3], # Out
        [4, 2, 3], # First Letter
        [1, 5, 3], # First Digit
        [1, 2, 6], # First Punctuation
        [4, 2, 3], # In Letter
        [1, 5, 3], # In Digit
        [1, 2, 6]  # In Puncuation
    ]
    for char in s:
        char_type = get_char_type(char)
        state = transition[state][char_type]
        if state in [1, 2, 3]:
            grammar.append((get_token_name(token), token))
            token = char
        else:
            token += char
    grammar.append((get_token_name(token), token))
    return grammar[1:]

def read_rockyou_file():
    with open("rockyou-withcount.txt") as f:
        return [i.split() for i in f.readlines() if len(i.split()) == 2]

def read_input_file(filename):
    with open(filename) as f:
        return [i.strip() for i in f.readlines() if len(i.strip()) > 0]

def parse_data_to_pcfg(data):
    grammar, term = defaultdict(int), defaultdict(lambda : defaultdict(int))
    for freq, password in data:
        raw_grammar = parse_string_cfg(password)
        grammar[tuple([i[0] for i in raw_grammar])] += int(freq)
        for token_name, token in raw_grammar:
            term[token_name][token] += int(freq)
    return grammar, term

def get_start_pcfg(grammar):
    return get_prob_distrib(grammar)

def get_term_pcfg(terminals):
    term_pcfg = {}
    for name, freqs in terminals.iteritems():
        term_pcfg[name] = get_prob_distrib(freqs)
    return term_pcfg

### Password Generation ###

def tough_nut():
    chars = string.ascii_letters + string.digits + string.punctuation
    return "".join([chars[random.randrange(len(chars))] for i in range(40)])

def gen_pickles():
    train_data = read_rockyou_file()
    grammar, terminal = parse_data_to_pcfg(train_data)
    start, term = get_start_pcfg(grammar), get_term_pcfg(terminal)
    with open("grammar.pickle", "wb") as grammar_file:
        pickle.dump(start, grammar_file)
    with open("terminal.pickle", "wb") as terminal_file:
        pickle.dump(term, terminal_file)

def download_pickles_zip():
    print "Downloading Pickle!"
    download_success = False
    file_url = "https://s3.amazonaws.com/afkfurion/pickles.zip"
    while not download_success:
        try:
            file_name = wget.download(file_url)
            download_success = True
            print
        except Exception, e:
            print e
            print "Download Failed. Please check your network connection."

def unzip_pickles():
    print "Unzipping PCFG Pickles!"
    with zipfile.ZipFile("pickles.zip", 'r') as f:
        f.extractall()

def load_pickles():
    print "Loading Pickles!"
    with open("grammar.pickle", "r") as grammar_file:
        start = pickle.load(grammar_file)
    with open("terminal.pickle", "r") as terminal_file:
        term = pickle.load(terminal_file)
    return start, term

def make_password(start_pcfg, term_pcfg, origin_password, number=10):
    tough_nut_prob = 0.1
    passwords = [tough_nut() for i in range(int(number*tough_nut_prob))]
    passwords.append(origin_password)
    while len(passwords) < number:
        grammar = numpy.random.choice(start_pcfg.keys(), p=start_pcfg.values())
        tokens = [numpy.random.choice(
            term_pcfg[i].keys(), p=term_pcfg[i].values()) for i in grammar]
        password = "".join(tokens)
        if password != origin_password and not password in passwords:
            passwords.append(password)
    random.shuffle(passwords)
    return passwords

def generate_passwords(input_file, number=10):
    input_data = read_input_file(input_file)
    download_pickles_zip()
    unzip_pickles()
    start, term = load_pickles()
    print "Generating Sweetwords!"
    sweetwords = [make_password(start, term, i, number) for i in input_data]
    return sweetwords

if len(sys.argv) != 4:
    print "Generate the honeywords."
    print ""
    print "python solution3.py n inputfile outputfile"
    print ""
    print "     n               the number of passwords"
    print "     inputfile       the filename of inputfile"
    print "     outputfile      the filename of outputfile"
    sys.exit(1)

#python solution3.py 5 rockyou-withcount.txt honeywords.txt

sweetwords = generate_passwords(sys.argv[2], int(sys.argv[1]))
write_csv(sys.argv[3], sweetwords)