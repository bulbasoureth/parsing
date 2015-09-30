#!/usr/bin/env python3
import re
#1a
def number(tokens):
    if re.match(r"^([0-9][0-9]*)$", tokens[0]):
        return (int(tokens[0]), tokens[1:])

def variable(tokens):
    if re.match(r"^([a-zA-Z][a-zA-Z0-9]*)$", tokens[0]):
        return (tokens[0], tokens[1:])

#1b
def left(tokens, top = True):
     seqs = [\
       ('True', 'true'),\
       ('False', 'false'),\
       ]
     for (key, value) in seqs:
        if tokens[0] == value:
            tokens = tokens[1:]
            if not top or len(tokens) == 0:
                return (key,tokens)


     if tokens[0] == 'not' and tokens[1] == '(':
            tokens = tokens[2:]
            r = left(tokens, False)
            if not r is None:
                    (e1, tokens) = r
                    if tokens[0] == ')':
                            tokens = tokens[1:]
                            if not top or len(tokens) == 0:
                                    return ({'Not':[e1]}, tokens)

     if tokens[0] == 'nonzero' and tokens[1] == '(':
            tokens = tokens[2:]
            r = term(tokens, False)
            if not r is None:
                    (e1, tokens) = r
                    if tokens[0] == ')':
                            tokens = tokens[1:]
                            if not top or len(tokens) == 0:
                                    return ({'Nonzero':[e1]}, tokens)

     if re.match(r"^([a-zA-Z][a-zA-Z0-9]*)$", tokens[0]):
            if not top or len(tokens) == 0:
                    (e1, tokens) = variable(tokens)
                    return ({'Variable': [e1]}, tokens)
    #  if re.match(r"^([0-9][0-9]*)$", tokens[0]):
    #        if not top or len(tokens) == 0:
    #                (e1, tokens) = number(tokens)
    #                return ({'Number': [e1]}, tokens)

def formula(tmp, top = True):
    tokens = tmp[0:]
    r1 = left(tokens, False)
    if not r1 is None:
        (e1, tokens) = r1
        if len(tokens) != 0 and tokens[0] == 'and':
                tokens = tokens[1:]
                r2 = formula(tokens, False)
                if not r2 is None:
                    (e2, tokens) = r2
                    if not top or len(tokens) == 0:
                            return ({'And':[e1,e2]}, tokens)
        else:
            if not top or len(tokens) == 0:
                return (e1, tokens)

def term(tmp, top = True):
    tokens = tmp[0:]
    r1 = factor(tokens, False)
    if not r1 is None:
        (e1, tokens) = r1
        if len(tokens) != 0 and not r1 is None:
            if tokens[0] == '+':
                    tokens = tokens[1:]
                    r1 = term(tokens, False)
                    if not r1 is None:
                            (e2, tokens) = r1
                            if not top or len(tokens) == 0:
                                    return ({'Plus':[e1,e2]}, tokens)
    tokens = tmp[0:]
    r1 = factor(tokens, False)
    if not r1 is None:
        (e1, tokens) = r1
        if not top or len(tokens) == 0:
            return (e1, tokens)

def factorleft(tokens, top = True):

    if tokens[0] == '(':
            tokens = tokens[1:]
            r1 = term(tokens, False)
            if not r1 is None:
                    (e1, tokens) = r1
                    if tokens[0] == ')':
                            tokens = tokens[1:]
                            if not top or len(tokens) == 0:
                                return ({'Parens':[e1]}, tokens)

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


    if re.match(r"^([a-zA-Z][a-zA-Z0-9]*)$", tokens[0]):
            if not top or len(tokens) == 0:
                    (e1, tokens) = variable(tokens)
                    return ({'Variable': [e1]}, tokens)
    if re.match(r"^([0-9][0-9]*)$", tokens[0]):
            if not top or len(tokens) == 0:
                   (e1, tokens) = number(tokens)
                   return ({'Number': [e1]}, tokens)

def factor(tmp, top = True):
    tokens = tmp[0:]
    r1 = factorleft(tokens, False)
    if not r1 is None:
        (e1, tokens) = r1
        if len(tokens) != 0:
            if tokens[0] == '*':
                tokens = tokens[1:]
                r1 = factor(tokens, False)
                if not r1 is None:
                        (e2, tokens) = r1
                        if not top or len(tokens) == 0:
                                return ({'Mult':[e1,e2]}, tokens)
            else:
                if not top or len(tokens) ==0:
                    return(e1,tokens)
        else:
            if not top or len(tokens) == 0:
                return (e1, tokens)


#1d
def program(tmp, top = True):
    tokens = tmp[0:]
    if len(tokens) != 0:
        if tokens[0] == 'print':
                tokens = tokens[1:]
                r1 = expression(tokens, False)
                if not r1 is None:
                    (e1, tokens) = r1
                    if len(tokens) >1 and tokens[0] == ';' and tokens[1] == '}':
                        tokens = tokens[1:]
                        return({'Print': [e1, 'End']}, tokens)
                    elif tokens[0] == ';':
                        tokens = tokens[1:]
                        r1 = program(tokens, False)
                        if len(tokens) == 0 and not r1 is None:

                            if r1 == 'End' and not r1 is None:
                                if not top or len(tokens) == 0:
                                        return ({'Print':[e1,r1]}, tokens)
                            else:
                                if not r1 is None:
                                    (e2, tokens) = r1
                                    if not top or len(tokens) == 0:
                                        return ({'Print':[e1,e2]}, tokens)
                        else:
                            if not r1 is None:
                                (e2, tokens) = r1
                                return({'Print':[e1, e2]}, tokens)


    tokens = tmp[0:]
    if len(tokens) != 0:
        if tokens[0] == 'assign':
                tokens = tokens[1:]
                r1 = factor(tokens, False)
                if not r1 is None:
                    (e1, tokens) = r1
                    if tokens[0] == ':=':
                         tokens = tokens[1:]
                         r1 = expression(tokens, False)
                         if not r1 is None:
                                 (e2, tokens) = r1
                                 if tokens[0] == ';' and tokens[1] == '}':
                                      tokens = tokens[1:]
                                      return({'Assign': [e1,e2, 'End']}, tokens)
                                 elif tokens[0] == ';':
                                      tokens = tokens[1:]
                                      r1 = program(tokens, False)
                                      if len(tokens) == 0 and not r1 is None:
                                          if r1 == 'End' and not r1 is None:
                                               if not top or len(tokens) == 0:
                                                      return ({'Assign':[e1,e2, r1]}, tokens)
                                          else:
                                              if not r1 is None:
                                                  (e3, tokens) = r1
                                                  if not top or len(tokens) == 0:
                                                      return ({'Assign':[e1,e2, e3]}, tokens)
                                      else:
                                              (e3, tokens) = r1
                                              return({'Assign':[e1,e2,e3]}, tokens)
    tokens = tmp[0:]
    if len(tokens) != 0:
        if tokens[0] == 'if':
                tokens = tokens[1:]
                r1 = expression(tokens, False)
                if not r1 is None:
                    (e1, tokens) = r1
                    if tokens[0] == '{':
                         tokens = tokens[1:]
                         r1 = program(tokens, False)
                         if not r1 is None:
                                 (e2, tokens) = r1
                                 if tokens[0] == '}':
                                      tokens = tokens[1:]
                                      r1 = program(tokens, False)
                                      if not r1 is None:
                                              (e3, tokens) = r1
                                              if not top or len(tokens) == 0:
                                                    return ({'If':[e1,e2,e3]}, tokens)
    tokens = tmp[0:]
    if len(tokens) != 0:
        if tokens[0] == 'do' and tokens[1] == '{':
                tokens = tokens[2:]
                r1 = program(tokens, False)
                if not r1 is None:
                    (e1, tokens) = r1
                    if tokens[0] == '}' and tokens[1] == 'until':
                         tokens = tokens[2:]
                         r1 = expression(tokens, False)
                         if not r1 is None:
                                 (e2, tokens) = r1
                                 if tokens[0] == ';':
                                      tokens = tokens[1:]
                                      r1 = program(tokens, False)
                                      if not r1 is None:
                                              (e3, tokens) = r1
                                              if not top or len(tokens) == 0:
                                                    return ({'DoUntil':[e1,e2,e3]}, tokens)
    token = tmp[0:]
    if len(tokens) == 0:
            if not top or len(tokens) == 0:
                return ('End', tokens)

def expression(tmp, top = True):

            tokens = tmp[0:]
            if tokens[1] == 'and' or tokens[0] == 'nonzero' or tokens[0] == 'not' or tokens[0] == 'true' or tokens[0] == 'false':
                r1 = formula(tokens, False)
                if not r1 is None:
                    (e1, tokens) = r1
                    if not top or len(tokens) == 0:
                            return (e1, tokens)

            else:
                r1 = term(tokens, False)
                if not r1 is None:
                    (e1, tokens) = r1
                    if not top or len(tokens) == 0:
                            return (e1, tokens)


#2a
