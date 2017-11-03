# -*- coding: utf-8 -*-

import operator
import functools
import re
# import exrex

class TermCategory:
    END = "end"
    ITEM = "item" # terms that belong to and describe items you can buy in the shop
    NUMBER = "number"
    UNKNOWN = "unknown"

    
all_terms = []
class  Term: 
    def __init__(self, regex="", name=None, categories=(), wrap=True, lemma=None):
        self.name = name or regex or '?' # exrex.getone(regex) 
        self.regex = re.compile(r'\b' + regex + r'\b' if wrap else regex, re.UNICODE)
        self.categories = frozenset(categories)
        self.lemma = lemma
        global all_terms
        all_terms.append(self)
        
    def __hash__(self):
        return hash(self.name)
    
    def __repr__(self):
        return self.name
        
class Expression:
    def evaluate(self, seq, start, end):
        raise NotImplementedError()
    
    def terms(self):
        return frozenset()
    
    def __or__(self, exp):
        return OrExpression(self, exp)
    
    def __and__(self, exp):
        return AndExpression(self, exp)
    
    def __not__(self, exp):
        return NotExpression(self)
    
class TermExpression(Expression):
    def __init__(self, term, implicit=0.0, memory=(0.0, 0.0)):
        self._term = term
        self._implicit = implicit
        self._memory = memory
        
    def evaluate(self, seq, start, end):
        indexes = seq.indexes[self._term]
        if [i for i in indexes if start <= i and i < end]:
            return 1.0
        
        # if the term is mentioned right before the interval get the biggest memory score
        # and the smallest if it was mentioned first
        memory_indexes = [i for i in indexes if i < start]
        if memory_indexes and self._memory != (0.0, 0.0):
            ratio = max(memory_indexes) / (start - 1.0)
            return self._memory[0] * (1 - ratio) + self._memory[1] * ratio
        
        print(self._term.name, self._implicit)
        return self._implicit
    
    def terms(self):
        return frozenset([self._term])
        
x = TermExpression

class NotExpression(Expression):
    def __init__(self, exp):
        self._exp = exp
        
    def evaluate(self, seq, start, end):
        return 1.0 - self._exp.evaluate(seq, start, end)
    
class AndExpression(Expression):
    def __init__(self, *exps):
        self._exps = exps
        
    def evaluate(self, seq, start, end):
        return functools.reduce(operator.mul, [exp.evaluate(seq, start, end) for exp in self._exps], 1.0)
    
    def terms(self):
        return frozenset.union(*[exp.terms() for exp in self._exps])
    
and_ = AndExpression
    
class OrExpression(Expression):
    def __init__(self, *exps):
        self._exps = exps
        
    def evaluate(self, seq, start, end):
        return 1.0 - functools.reduce(operator.mul, [1.0 - exp.evaluate(seq, start, end) for exp in self._exps], 1.0)
        
    def terms(self):
        return frozenset.union(*[exp.terms() for exp in self._exps])
    
or_ = OrExpression

class Item:
    def __init__(self, name, exp, price, desc = "", tags=frozenset()):
        self.name = name
        self.price = price
        self.desc = desc
        self._exp = exp
        self._tags = tags | exp.terms()
        
    def match_exp(self, term):
        return bool(term in self._exp.terms())
    
    def match_tags(self, term):
        return bool(term in self._tags)
    
    def evaluate(self, seq, start, end):
        return self._exp.evaluate(seq, start, end)
    
    def get_price(self, n=1):
        if type(self.price) == int:
            return self.price * n
        else:
            return self.price(n)

    def __repr__(self):
        return self.name
    
it = Item