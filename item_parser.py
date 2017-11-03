# -*- coding: utf-8 -*-

from collections import defaultdict
import re
from expressions import *
from terms import *
from items import items, exp
import getopt
import sys

sentence = "Quiero 2 empanadás de pollo y una docena de carne, una piza de muza y 1 coca grande"

class Token:
    def __init__(self, string, start=0, end=None, term=None):
        self.string = string
        self.term = term
        self.start = start
        self.end = end or len(string)
        self.lemma = (term.lemma if term else None) or string
        assert self.end - self.start == len(string)
        
    def __repr__(self):
        return "{} ({})".format(self.string, self.term.name if self.term else 'None') 

class TokenSequence:
    def __init__(self, tokens):
        self.tokens = tokens
        self.indexes = defaultdict(list)
        for i, token in enumerate(tokens):
            if token.term and TermCategory.ITEM in token.term.categories : 
                self.indexes[token.term].append(i)
    
def parse_term(tokens, term):
    parsed_tokens = []    
    for token in tokens:
        if not token.term:
            string = token.string
            start = token.start
            end = token.end
            match = term.regex.search(string)
            while match:
                prefix = string[:match.start()].strip()
                if prefix:
                    parsed_tokens.append(Token(prefix, start=start, end=start + len(prefix)))
                parsed_tokens.append(Token(match.group(), term=term, start=start + match.start(), end=start + match.end()))
                string = string[match.end():].strip()
                start = end - len(string)
                match = term.regex.search(string)
            if string:
                parsed_tokens.append(Token(string, start=start, end=end))
        else:
            parsed_tokens.append(token)
    return parsed_tokens

class ItemMatch:
    def __init__(self, clear_match, items, start, end):
        self.clear_match = clear_match
        self.items = items
        self.start = start
        self.end = end
        self.count = None
        
    def __repr__(self):
        padding = ' ' * self.start
        rep = padding + '<' + ' ' * (self.end - self.start - 2) + '>\n'
        if self.count:
            rep += padding + "Count is " + str(self.count) + "\n"
        else:
            rep += padding + "Cannot determine count\n"
        if not self.items:
            return rep + padding + "Sorry, we don't have that\n"
        if self.clear_match:
            rep += padding + "Likely canidate(s):\n"
        else: 
            rep += padding + "Nothing matches, some suggestion(s):\n"
        rep += ''.join('{}{} (P={:.4f})\n'.format(padding, item.name, score) for item, score in self.items)
        return rep

def get_item(seq, potential_items, item_tokens):
    if not potential_items:
        return []
    scores = [item.evaluate(seq, item_tokens[0][0], item_tokens[-1][0] + 1) for item in potential_items]
    
    mx = max(scores)
    start = item_tokens[0][1].start
    end = item_tokens[-1][1].end
    if mx < exp**12:
        return ItemMatch(clear_match=False, items=zip(potential_items, scores), start=start, end=end)
    return ItemMatch(clear_match=True, items=[(item, score) for item, score in zip(potential_items, scores) if score >= mx - 0.001], start=start, end=end)

def parse(sent):
    spaces = re.compile(r'\s+')
    sent = sent.replace(',', ' , ').replace('.', ' . ').replace(' ( ', '(').replace(' ) ', ')')
    sent = re.sub(spaces, ' ', sent).strip().lower()
    sent = sent.replace('á','a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('ü', 'u')
    tokens = [Token(sent)]
    for term in all_terms:
        tokens = parse_term(tokens, term)
    tokens = [token for token in tokens if token.term]
    tokens.append(Token("", term=end))
    seq = TokenSequence(tokens)
    parsed_items = []
    item_tokens = []
    counts = []
    potential_items = items

    
    for i, token in enumerate(tokens):
        if TermCategory.NUMBER in token.term.categories:
            counts.append(token)
        if (set([TermCategory.NUMBER, TermCategory.END]) & token.term.categories) and item_tokens:
            parsed_items.append(get_item(seq, potential_items, item_tokens))
            potential_items = items
            item_tokens = []
        elif TermCategory.ITEM in token.term.categories: 
            filtered_items = [item for item in potential_items if item.match_exp(token.term)]
            if filtered_items:
                potential_items = filtered_items
                item_tokens.append((i, token))
            elif item_tokens:
                parsed_items.append(get_item(seq, potential_items, item_tokens))
                potential_items = [item for item in items if item.match_exp(token.term)]
                item_tokens = [(i, token)]

    if len(counts) == len(parsed_items):
        for count, match in zip(counts, parsed_items):
            match.count = count.lemma
    return sent, tokens, parsed_items

def pretty_parse(sent):
    sent, tokens, parsed_items = parse(sent)
    # print(tokens)
    ans = sent + "\n"
    for item in parsed_items:
        ans += "\n" + repr(item)
    return ans

def main():
    # parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.error:
        print("For help use --help")
        sys.exit(2)
    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            print("Armá tu pedido con lo que quieras de este menú")
            print("\n".join("{:>3} $ - {}".format(item.get_price(), item.name) for item in items))
            sys.exit(0)
    sentence = ' '.join(args)
    print(pretty_parse(sentence))

if __name__ == "__main__":
    main()