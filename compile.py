#!/usr/bin/env python3
######################################################################
#
# CAS CS 320, Fall 2015
# Assignment 3 (skeleton code)
# compile.py
#
import re
exec(open('parse.py').read())
exec(open('machine.py').read())


Node = dict
Leaf = str

import random

def freshStr():
	return str(random.randint(0,100000))

def compileTerm(env,t,heap):
    if type(t) == Node:
        for label in t:
            children = t[label]
            if label == 'Number':
                n = children[0]
                heap = heap+1
                inst = 'set ' + str(heap) + ' ' + str(n)
                return ([inst], heap, heap)

            elif label == 'Variable':
                n = children[0]
                if n in env:
                        return ([], env[n], heap)
                else:
                    exit()
            elif label == 'Plus':
                f1 = children[0]
                f2 = children[1]
                (insts1, addr1, heap2) = compileTerm(env, f1, heap)
                (insts2, addr2, heap3) = compileTerm(env, f2, heap2)
                heap4 = heap3 + 1
                instsPlus = \
                    copy (str(heap2), 1) +\
                    copy (str(heap3),2)+\
                    ["add"] + \
                    copy(0,heap4) \

                return (insts1 + insts2 + instsPlus, heap4, heap4)

def compileFormula(env,f,heap):
    if type(f) == Leaf:
        if f == 'True':
            heap = heap + 1
            inst = 'set ' + str(heap) + ' 1'
            return ([inst], heap, heap)
        if f == 'False':
            heap = heap + 1
            inst = 'set ' + str(heap) + ' 0'
            return ([inst], heap, heap)

    elif type(f) == Node:
        for label in f:
            children = f[label]
            if label == 'Number':
                n = children[0]
                heap = heap + 1
                inst = 'set ' + str(heap) + ' ' + str(n)
                return ([inst], heap, heap)

            elif label == 'Variable':
                n = children[0]
                if n in env:
                        return ([], env[n], heap)
                else:
                    exit()

            elif label == 'Not':
                f = children[0]
                (insts1, addr, heap) = compileFormula(env, f, heap)
                fresh = freshStr();
                instsNot = \
                   ["branch setZero "   + fresh+  str(heap),\
                    "set " + str(heap) + " 1",\
                    "branch finish "  + fresh,\
                    "label setZero "  + fresh,\
                    "set " + str(heap) + " 0",\
                    "label finish "  + fresh\
                   ]
                return(insts1 + instsNot, heap, heap)

            elif label == 'And':
                f1 = children[0]
                f2 = children[1]
                (insts1, addr1, heap2) = compileFormula(env, f1, heap)
                (insts2, addr2, heap3) = compileFormula(env, f2, heap2)
                heap4 = heap3 + 1
                fresh = freshStr()
                instsAnd = [\
					"label begin "] +\
					copy(addr1, 1) +\
					["set 2 0",\
					"add",\
					"branch addTwo 0",\
					"goto finish ",\
					"label addTwo "] +\
					copy(addr2, 1) +\
					["set 2 0",\
					"add",\
					"branch setOne 0",\
					"goto finish ",\
					"label setOne ",\
					"set 0 1",\
					"label finish "] +\
					copy(0, heap4)

                return (insts1 + insts2 + instsAnd, heap4, heap4)

            elif label == 'And-Short':
                (insts1, addr1, heap) = compileFormula(env, children[0], heap)
                heap=heap+1
                fresh = freshStr();
                insts2 = [
                    "label f1" + fresh +\
                    copy(addr1, 1) +\
                    "set 2 0",\
		            "add",\
		            "branch result" + fresh + " 0",\
		            "goto finish" + fresh,\
                    "label result" + fresh,\
		            "set 0 1",\
		            "label finish" + fresh +\
		            copy(0, heap)]
                return (insts1 + insts2, heap, heap)

            elif label == 'Equal':
                f1 = children[0]
                f2 = children[1]
                (insts1, addr1, heap2) = compileTerm(env, f1, heap)
                (insts2, addr2, heap3) = compileTerm(env, f2, heap2)
                heap4 = heap3 + 1
                fresh = freshStr();
                instsEqual = \
                    copy (str(heap2), 8) +\
                    copy (str(heap3),9)+[\
                    "copy 9 0" ,\
                    "set 3 0" ,\
                    "set 4 " + str(heap4) ,\
                    "copy" +\
                    copy(0,heap3s)
                   ]

                return (insts1 + insts2 + instsEqual, heap3, heap3)

            elif label == 'Xor':
                f1 = children[0]
                f2 = children[1]
                (insts1, addr, heap) = compileFormula(env, f1, heap)
                (insts2, addr1, heap) = compileFormula(env, f2, heap)
                heap1 = heap + 1
                fresh = freshStr();
                instsXor = \
                   copy (str(addr), 1) +\
                   copy (str(addr1),2) + [\
                    "add",\
                    "branch setOne "   + fresh+ " 0",\
                    "goto finish "  + fresh,\
                    "label setOne "  + fresh,\
                    "set 0 0",\
                    "label finish "  + fresh] + \
                    copy (0, str(heap1))

                return(insts1 + insts2 + instsXor, heap1, heap1)

def compileExpression(env, x, heap):
    return compileTerm(env, x, heap) or compileFormula(env, x, heap)

def compileProgram(env, s, heap):
    if s == 'End':
        instsEnd = []
        return (env, instsEnd, heap)
    elif type(s) == Node:
        for label in s:
            if label == 'Print':
                children = s[label]
                f1 = children[0]
                f2 = children[1]
                (insts1, addr, heap) = compileExpression(env, f1, heap)
                instsPrint=copy(heap,5)
                (env1, insts2, heap2) = compileProgram(env, f2, heap)
                return (env1, insts1 + instsPrint + insts2, heap2)

            elif label == 'Assign':
                children = s[label]
                x = children[0]['Variable'][0]
                f2 = children[1]
                f3 = children[2]
                (insts1, addr, heap) = compileExpression(env, f2, heap)
                if x in env:
                        instsAssign = copy(heap, env[x])
                else:
                        env[x] = addr
                        instsAssign = []
                (env1, insts2, heap3) = compileProgram(env, f3, heap)
                return (env1, insts1 + instsAssign + insts2, heap3)



            elif label == 'If':
                [cond, body, rest] = s[label]
                (insts1, addr1, heap1) = compileExpression(env, cond, heap)
                (env1, insts2, heap2) = compileProgram(env,body,heap1)
                fresh = freshStr();
                instsIf = [
                          'branch ifBody '+ str(addr1),\
                          'goto skip ',\
                          'label ifBody '] +\
                          insts2 + [\
                          'label skip '\
                          ]
                (env2, insts3, heap3) = compileProgram(env1,rest,heap2)
                return(env2, insts1 + instsIf + insts3, heap3)

            elif label == 'Until':
                fresh = freshStr();
                [cond, body, rest] = s[label]
                instsUntil = ['label startUntil ' + fresh]
                (insts1, addr1, heap1) = compileExpression(env, cond, heap)
                instsUntil.append(insts1)
                instsUntil.append('branch untilEnd '  + fresh+ addr1)
                (env1, insts2, heap2) = compileProgram(env,b,heap1)
                instsUntil.append(insts2)
                instsUntil.append('goto Until ' + fresh)
                instsUntil.append('label untilEnd ' + fresh)
                (env2, insts3, heap3) = compileProgram(env1,r,heap2)
                instsUntil.append(insts3)
                return(env2, instsUntil, heap3)

            elif label == 'Procedure':
                children = s[label]
                f1 = children[0]['Variable'][0]
                f2 = children[1]
                f3 = children[2]
                (env2, insts2, heap2) = compileProgram(env, f2, heap)
                instsProc = procedure(f1, insts2)
                (env3, insts3, heap3) = compileProgram(env2, f3, heap2)
                return (env3, instsProc + insts3, heap3)

            elif label == 'Call':
                children = s[label]
                f1 = children[0]['Variable'][0]
                f2 = children[1]
                instsCall = call(f1)
                (env1, insts1, heap1) = compileProgram(env, f2, heap)
                return (env1, instsCall + insts1, heap1)


# Implement a function compile(s) that takes a single string s that
# is a concrete syntax representation of a program in the source programming
# language and returns its compiled form: a sequence of instructions
# in the target machine language.
def compile(s):
    a = tokenizeAndParse(s)
    setup = [\
            "set 7 -1"\
            ]
    (env, insts, heap) = compileProgram({}, a, 8)
    return (setup + insts)
# print(simulate(compile("x := 1; y := 2; z := 3; print x + y + z;")))
#eof
