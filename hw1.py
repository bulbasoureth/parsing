#!/usr/bin/env python3
import re
import json
#1a
def regexp(s):
	return "|".join(s)


#1b
def tokenize(s, string):
    #tokens = [t for t in re.split('|\s+|\+|\*|\(|\)'+regexp(s), string)]
    tokens = [t for t in re.split(r"(\s+|\+|\*|\(|\)|[a-z]+|[0-9]+)", string)]
    return [t for t in tokens if not t.isspace() and not t == ""]


#1c
def tree(tmp, top = True):
    tokens = tmp[0:]
    if tokens[0] == 'two' and tokens[1] == 'children' and tokens[2] == 'start':
        tokens = tokens[3:]
        r = tree(tokens, False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == ';':
                tokens = tokens[1:]
                r = tree(tokens, False)
                if not r is None:
                    (e2, tokens) = r
                    if tokens[0] == 'end':
                        tokens = tokens[1:]
                if not top or len(tokens) == 0:
                    return ({'Two':[e1,e2]}, tokens)

    tokens = tmp[0:]
    if tokens[0] == 'one' and tokens[1] == 'child' and tokens[2] == 'start':
        tokens = tokens[3:]
        r = tree(tokens, False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == 'end':
                tokens = tokens[1:]
                if not top or len(tokens) == 0:
                    return ({'One':[e1]}, tokens)

    tokens = tmp[0:]
    if tokens[0] == 'zero' and tokens[1] == 'children':
        tokens = tokens[2:]
        if not top or len(tokens) == 0:
            return ('Zero', tokens)
#2a
def number(tokens):
    if re.match(r"^([0-9][0-9]*)$", tokens[0]):
        return ({"Number": [int(tokens[0])]}, tokens[1:])

def variable(tokens):
    if re.match(r"^([a-z]*)$", tokens[0]):
        return ({"Variable": [tokens[0]]}, tokens[1:])

#2b
def term(tmp, top = True):
    seqs = [\
        (number,'#'),\
        (variable, '$'),\
        ]
    for (key, value) in seqs:
        tokens = tmp[0:]
        if tokens[0] == value:
            tokens = tokens[1:]
            if not top or len(tokens) == 0:
                return key(tokens)

    tokens = tmp[0:]
    if tokens[0] == 'plus' and tokens[1] == '(':
            tokens = tokens[2:]
            r1 = term(tokens, False)
            if not r1 is None:
                (e1, tokens) = r1
                if tokens[0] == ',':
                     tokens = tokens[1:]
                     r1 = term(tokens, False)
                     if not r1 is None:
                             (e2, tokens) = r1
                             if tokens[0] == ')':
                                 tokens = tokens[1:]
                                 if not top or len(tokens) == 0:
                                                return ({'Plus':[e1,e2]}, tokens)

    tokens = tmp[0:]
    if tokens[0] == 'max' and tokens[1] == '(':
            tokens = tokens[2:]
            r1 = term(tokens, False)
            if not r1 is None:
                    (e1, tokens) = r1
                    if tokens[0] == ',':
                            tokens = tokens[1:]
                            r1 = term(tokens, False)
                            if not r1 is None:
                                    (e2, tokens) = r1
                                    if tokens[0] == ')':
                                            tokens = tokens[1:]
                                            if not top or len(tokens) == 0:
                                                return ({'Max':[e1,e2]}, tokens)
    tokens = tmp[0:]
    if tokens[0] == 'if' and tokens[1] == '(':
                  tokens = tokens[2:]
                  r1 = formula(tokens, False)
                  if not r1 is None:
                     (e1, tokens) = r1
                     if tokens[0] == ',':
                            tokens = tokens[1:]
                            r1 = term(tokens, False)
                     if not r1 is None:
                             (e2, tokens) = r1
                             if tokens[0] == ',':
                                    tokens = tokens[1:]
                                    r1 = term(tokens, False)
                             if not r1 is None:
                                     (e3, tokens) = r1
                                     if tokens[0] == ')':
                                         tokens = tokens[1:]
                                         if not top or len(tokens) == 0:
                                                return ({'If':[e1,e2,e3]}, tokens)


    tokens = tmp[0:]
    if tokens[0] == '(':
            tokens = tokens[1:]
            r1 = term(tokens, False)
            if not r1 is None:
                (e1, tokens) = r1
                if tokens[0] == '+':
                     tokens = tokens[1:]
                     r1 = term(tokens, False)
                     if not r1 is None:
                             (e2, tokens) = r1
                             if tokens[0] == ')':
                                 tokens = tokens[1:]
                                 if not top or len(tokens) == 0:
                                                return ({'Plus':[e1,e2]}, tokens)
    tokens = tmp[0:]
    if tokens[0] == '(':
            tokens = tokens[1:]
            r1 = term(tokens, False)
            if not r1 is None:
                (e1, tokens) = r1
                if tokens[0] == 'max':
                     tokens = tokens[1:]
                     r1 = term(tokens, False)
                     if not r1 is None:
                             (e2, tokens) = r1
                             if tokens[0] == ')':
                                 tokens = tokens[1:]
                                 if not top or len(tokens) == 0:
                                                return ({'Max':[e1,e2]}, tokens)
    tokens = tmp[0:]
    if tokens[0] == '(':
                  tokens = tokens[1:]
                  r1 = formula(tokens, False)
                  if not r1 is None:
                     (e1, tokens) = r1
                     if tokens[0] == '?':
                            tokens = tokens[1:]
                            r1 = term(tokens, False)
                     if not r1 is None:
                             (e2, tokens) = r1
                             if tokens[0] == ':':
                                    tokens = tokens[1:]
                                    r1 = term(tokens, False)
                             if not r1 is None:
                                     (e3, tokens) = r1
                                     if tokens[0] == ')':
                                         tokens = tokens[1:]
                                         if not top or len(tokens) == 0:
                                                return ({'If':[e1,e2,e3]}, tokens)


def formula(tmp, top = True):
     seqs = [\
       ('True', 'true'),\
       ('False', 'false'),\
       ]
     for (key, value) in seqs:
        tokens = tmp[0:]
        if tokens[0] == value:
            tokens = tokens[1:]
            if not top or len(tokens) == 0:
                return (key,tokens)
     tokens = tmp[0:]
     if tokens[0] == 'not' and tokens[1] == '(':
            tokens = tokens[2:]
            r = formula(tokens, False)
            if not r is None:
                    (e1, tokens) = r
                    if tokens[0] == ')':
                            tokens = tokens[1:]
                            if not top or len(tokens) == 0:
                                    return ({'Not':[e1]}, tokens)
     tokens = tmp[0:]
     if tokens[0] == 'xor' and tokens[1] == '(':
            tokens = tokens[2:]
            r = formula(tokens, False)
            if not r is None:
                    (e1, tokens) = r
                    if tokens[0] == ',':
                            tokens = tokens[1:]
                            r = formula(tokens, False)
                            if not r is None:
                                    (e2, tokens) = r
                                    if tokens[0] == ')':
                                        tokens = tokens[1:]
                                        if not top or len(tokens) == 0:
                                                return ({'Xor':[e1,e2]}, tokens)
     tokens = tmp[0:]
     if tokens[0] == 'equal' and tokens[1] == '(':
            tokens = tokens[2:]
            r = term(tokens, False)
            if not r is None:
                    (e1, tokens) = r
                    if tokens[0] == ',':
                            tokens = tokens[1:]
                            r = term(tokens, False)
                            if not r is None:
                                    (e2, tokens) = r
                                    if tokens[0] == ')':
                                        tokens = tokens[1:]
                                        if not top or len(tokens) == 0:
                                                return ({'Equal':[e1,e2]}, tokens)
     tokens = tmp[0:]
     if tokens[0] == 'less' and tokens[1] == '(':
            tokens = tokens[2:]
            r = term(tokens, False)
            if not r is None:
                    (e1, tokens) = r
                    if tokens[0] == ',':
                            tokens = tokens[1:]
                            r = term(tokens, False)
                            if not r is None:
                                    (e2, tokens) = r
                                    if tokens[0] == ')':
                                        tokens = tokens[1:]
                                        if not top or len(tokens) == 0:
                                                return ({'Less':[e1,e2]}, tokens)
     tokens = tmp[0:]
     if tokens[0] == 'greater' and tokens[1] == '(':
            tokens = tokens[2:]
            r = term(tokens, False)
            if not r is None:
                    (e1, tokens) = r
                    if tokens[0] == ',':
                            tokens = tokens[1:]
                            r = term(tokens, False)
                            if not r is None:
                                    (e2, tokens) = r
                                    if tokens[0] == ')':
                                        tokens = tokens[1:]
                                        if not top or len(tokens) == 0:
                                                return ({'Greater':[e1,e2]}, tokens)

     tokens = tmp[0:]
     if tokens[0] == '(':
            tokens = tokens[1:]
            r1 = formula(tokens, False)
            if not r1 is None:
                (e1, tokens) = r1
                if tokens[0] == 'xor':
                     tokens = tokens[1:]
                     r1 = formula(tokens, False)
                     if not r1 is None:
                             (e2, tokens) = r1
                             if tokens[0] == ')':
                                 tokens = tokens[1:]
                                 if not top or len(tokens) == 0:
                                                return ({'Xor':[e1,e2]}, tokens)
     tokens = tmp[0:]
     if tokens[0] == '(':
            tokens = tokens[1:]
            r1 = term(tokens, False)
            if not r1 is None:
                (e1, tokens) = r1
                if tokens[0] == '==':
                     tokens = tokens[1:]
                     r1 = term(tokens, False)
                     if not r1 is None:
                             (e2, tokens) = r1
                             if tokens[0] == ')':
                                 tokens = tokens[1:]
                                 if not top or len(tokens) == 0:
                                                return ({'Equal':[e1,e2]}, tokens)
     tokens = tmp[0:]
     if tokens[0] == '(':
            tokens = tokens[1:]
            r1 = term(tokens, False)
            if not r1 is None:
                (e1, tokens) = r1
                if tokens[0] == '<':
                     tokens = tokens[1:]
                     r1 = term(tokens, False)
                     if not r1 is None:
                             (e2, tokens) = r1
                             if tokens[0] == ')':
                                 tokens = tokens[1:]
                                 if not top or len(tokens) == 0:
                                                return ({'Less':[e1,e2]}, tokens)
     tokens = tmp[0:]
     if tokens[0] == '(':
            tokens = tokens[1:]
            r1 = term(tokens, False)
            if not r1 is None:
                (e1, tokens) = r1
                if tokens[0] == '>':
                     tokens = tokens[1:]
                     r1 = term(tokens, False)
                     if not r1 is None:
                             (e2, tokens) = r1
                             if tokens[0] == ')':
                                 tokens = tokens[1:]
                                 if not top or len(tokens) == 0:
                                                return ({'Greater':[e1,e2]}, tokens)
def program(tmp, top = True):
    tokens = tmp[0:]
    if tokens[0] == 'print':
            tokens = tokens[1:]
            r1 = term(tokens, False)
            if not r1 is None:
                (d1, tokens) = r1
                if tokens[0] == ';':
                     tokens = tokens[1:]
                     r1 = program(tokens, False)
                     if not r1 is None:
                         d2 = r1
                         return ({'Print':[d1,d2]})

    tokens = tmp[0:]
    if tokens[0] == 'input' and tokens[1] == '$':
            tokens = tokens[2:]
            r1 = variable(tokens)
            if not r1 is None:
                    (d1, tokens) = r1
                    if tokens[0] == ';':
                            tokens = tokens[1:]
                            r1 = program(tokens, False)
                            if not r1 is None:
                                d2 = r1
                                return ({'Input':[d1,d2]})
    tokens = tmp[0:]
    if tokens[0] == 'assign' and tokens[1] == '$':
            tokens = tokens[2:]
            r1 = variable(tokens)
            if not r1 is None:
                    (d1, tokens) = r1
                    if tokens[0] == ':=':
                            tokens = tokens[1:]
                            r1  = term(tokens, False)
                            if not r1  is None:
                                    (d2, tokens) = r1
                                    if tokens[0] == ';':
                                        tokens = tokens[1:]
                                        r1 = program(tokens, False)
                                        if not r1 is None:
                                            e3 = r1
                                            return ({'Assign':[d1,d2,e3]})


    tokens = tmp[0:]
    if tokens[0] == 'end' and tokens[1] == ';':
            tokens = tokens[2:]
            if not top or len(tokens) == 0:
                return ('End')
# Implement a function parse() that takes a single string as an argument.
# If the input string conforms to the grammar of the programming language,
# the function should return a parse tree corresponding to that input string.

def parse(s):
    tokens = [t for t in re.split(r"(\s+|\+|\*|\(|\)|\,|\#|[a-z]+|[0-9]+)", s)]
    p = ([t for t in tokens if not t.isspace() and not t == ""])
    return program(p)


print(variable(['test']))
