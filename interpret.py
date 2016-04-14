#!/usr/bin/env python3
exec(open('parse.py').read())

def printnum(p):
    return {'Number': [p]}
def vand(v1, v2):
    if v1 == 'True'  and v2 == 'True':  return 'True'
    if v1 == 'True'  and v2 == 'False': return 'False'
    if v1 == 'False' and v2 == 'True':  return 'False'
    if v1 == 'False' and v2 == 'False': return 'False'

def vxor(v1, v2):
    if v1 == 'True'  and v2 == 'True':  return 'False'
    if v1 == 'True'  and v2 == 'False': return 'True'
    if v1 == 'False' and v2 == 'True':  return 'True'
    if v1 == 'False' and v2 == 'False': return 'False'

def vnot(v):
    if v == 'True' :return 'False'
    if v == 'False' :return 'True'

def vkwal(v1,v2):
    v1 = v2
    return v1

Node = dict
Leaf = str

def evalTerm(env, a):
    if type(a) == Node:
        for label in a:
            children = a[label]
            if label == 'Number':
                n = children[0]
                if n in env:
                    return env[n]
                else:
                    return {'Number':[n]}

            elif label == 'Variable':
                x = children[0]
                if x in env:
                    return env[x]
                else:
                    return {'Variable':[x]}

            elif label == 'Plus':
                t1 = children[0]
                v1 = evalTerm(env,t1)
                t2 = children[1]
                v2 = evalTerm(env,t2)
                v1 = v1['Number'][0]
                v2 = v2['Number'][0]
                return {'Number':[v1+v2]}
def evalFormula(env, f):
    if type(f) == Node:
        for label in f:
            children = f[label]
            if label == 'Number':
                n = children[0]
                if n in env:
                    return env[n]
                else:
                    return {'Number':[n]}

            if label == 'Variable':
                x = children[0]
                if x in env:
                    return env[x]
                else:
                    return {'Variable':[x]}

            elif label == 'Not':
                f = children[0]
                v = evalFormula(env,f)
                return vnot(v)


            elif label == 'And':
                f1 = children[0]
                v1 = evalFormula(env,f1)
                f2 = children[1]
                v2 = evalFormula(env,f2)
                return vand(v1,v2)

            elif label == 'Xor':
                f1 = children[0]
                v1 = evalFormula(env, f1)
                f2 = children[1]
                v2 = evalFormula(env, f2)
                return vxor(v1,v2)
            elif label == 'Equal':
                f1 = children[0]
                v1 = evalTerm(env, f1)
                f2 = children[1]
                v2 = evalTerm(env, f2)
                return vkwal(v1,v2)

    elif type(f) == Leaf:
        if f == 'True':
            return 'True'
        if f == 'False':
            return 'False'
        if f == 'End':
            return (env,[])

def evalExpression(env, e): # Useful helper function.
    if type(e) == Node:
        for label in e:
            if label == 'Not' or label == 'Equal' or label == 'And' or label == 'Xor':
                v = evalFormula(env,e)
                return v
            else:
                v = evalTerm(env,e)
                return v
    else:
        v = evalFormula(env,e)
        return v


def execProgram(env,s):
    if s == 'End':
        return (env,[])
    elif type(s) == Node:
        for label in s:
            if label == 'Print':
                children = s[label]
                e = children[0]
                p = children[1]
                v = evalExpression(env, e)
                (env, o) = execProgram(env, p)
                return (env, [v] + o)

            if label == 'Assign':
                children = s[label]
                x = children[0]['Variable'][0]
                e = children[1]
                p = children[2]
                v = evalExpression(env, e)
                env[x] = v
                (env, o) = execProgram(env, p)
                return (env, o)

            if label == 'If':
                [cond, body, rest] = s[label]
                env1 = env
                v = evalExpression(env1, cond)
                if v == 'False':
                    (env2, o1) = execProgram(env1, rest)
                    return (env2, o1)
                if v == 'True':
                    (env2, o1) = execProgram(env1, body)
                    (env3, o2) = execProgram(env2, rest)
                    return (env3, o1 + o2)

            if label == 'Until':
                [cond, body, rest] = s[label]
                env1 = env
                (env2, o1) = execProgram(env1, body)
                e = evalExpression(env2, cond)
                if e == 'False':
                    (env3, o2) = execProgram(env2, {'Until':[body, cond, rest]})
                    return (env3, o1 + o2)
                if e == 'True':
                    (env3, o2) = execProgram(env2, rest)
                    return (env3, o2)

            if label == 'Procedure':
                children = s[label]
                x = children[0]['Variable'][0]
                p1 = children[1]
                p2 = children[2]
                env1 = env
                env1[x] = p1
                (env2, o) = execProgram(env1, p2)
                return (env2, o)

            if label == 'Call':
                children = s[label]
                x = children[0]['Variable'][0]
                p2 = children[1]
                env1 = env
                if x in env1:
                    (env2, o1) = execProgram(env1, env1[x])
                    (env3, o2) = execProgram(env2, p2)
                    return (env3, o1 + o2)


def interpret(s):
    (env, o) = execProgram({}, tokenizeAndParse(s))
    return o

#eof
