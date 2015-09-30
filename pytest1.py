#!/usr/bin/env python
import re

############################################################
# Load the file. Change the path if necessary.
exec(open('hw1.py').read())

def check(name, function, inputs_result_pairs):
    def str_(s):
        return '"'+str(s)+'"' if type(s) == str else str(s)
    if type(name) == tuple:
        prefix = name[0]
        suffix = name[1]
    if type(name) == str:
        prefix = name + '('
        suffix = ')'

    passed = 0
    for (inputs, result) in inputs_result_pairs:
        try:
            output = function(inputs[0], inputs[1]) if len(inputs) == 2  else function(inputs[0])
        except Exception as e:
            output = '<Error>'

        if output != '<Error>' and output == result:
            passed = passed + 1
        else:
            print("\n  Failed on:\n    "+prefix+', '.join([str_(i) for i in inputs])+suffix+"\n\n"+"  Should be:\n    "+str(result)+"\n\n"+"  Returned:\n    "+str(output)+"\n")
    print("Passed " + str(passed) + " of " + str(len(inputs_result_pairs)) + " tests.")
    print("")

############################################################
# The tests.

def testProblemOnePartA(ts, s):
    return re.match(regexp(ts), s).group(0)

print("Problem #1, part (a)...")
try: regexp
except: print("The regexp() function is not defined.")
else:
    check('testProblemOnePartA', testProblemOnePartA, [\
        ((['xyz'], "xyz"), 'xyz'),\
        ((['e','f'], "efghi"), 'e'),\
        ((['abc','def'], "abc def"), 'abc'),\
        ])

print("\n\nProblem #1, part (b)...")
try: tokenize
except: print("The tokenize() function is not defined.")
else:
    check('tokenize', tokenize, [\
        ((['token'], "token token   token token   "), ['token', 'token', 'token', 'token']),\
        ((['example','test'], "example test example example"), ['example', 'test', 'example', 'example']),\
        ((['a','b','c','d','e',','], "a,b,c,d,e,d,c,b,a"), ['a', ',', 'b', ',', 'c', ',', 'd', ',', 'e', ',', 'd', ',', 'c', ',', 'b', ',', 'a']),\
        ((['up','down','left','right','finish',';'], "left; right; finish;"), ['left', ';', 'right', ';', 'finish', ';']),\
        ((['+','*','(',')','f','x','y','z'], "f(x+y)*z"), ['f','(','x','+','y',')','*','z']),\
        ])

print("\n\nProblem #1, part (c)...")
try: (tokenize, tree)
except: print("The tokenize() and/or tree() functions are not defined.")
else:
    check(('''tree(tokenize(["children","child","two","one","zero","start","end",";"], ''', '''))'''), (lambda s: tree(tokenize(["children","child","two","one","zero","start","end",";"], s))), [\
        (("zero children",), ('Zero',[])),\
        (("one child start zero children end",), ({'One': ['Zero']},[])),\
        (["one child start one child start zero children end end"], ({'One': [{'One': ['Zero']}]},[])),\
        (["one child start two children start zero children; zero children end end"], ({'One': [{'Two': ['Zero', 'Zero']}]},[])),\
        (["two children start two children start zero children; zero children end; zero children end"], ({'Two': [{'Two': ['Zero', 'Zero']}, 'Zero']},[])),\
        ])

print("\n\nProblem #2, part (c)...")
try: formula
except: print("The formula() function is not defined.")
else: check('formula', formula, [\
    (("false".split(' '),), ('False',[])),\
    (("not ( true )".split(' '),), ({'Not': ['True']},[])),\
    (('xor ( true , false )'.split(' '),), ({'Xor': ['True', 'False']},[])),\
    (('xor ( xor ( true , false ) , xor ( true , false ) )'.split(' '),), ({'Xor': [{'Xor': ['True', 'False']}, {'Xor': ['True', 'False']}]},[])),\
    (('not ( xor ( xor ( true , not ( false ) ) , xor ( true , false ) ) )'.split(' '),), ({'Not': [{'Xor': [{'Xor': ['True', {'Not': ['False']}]}, {'Xor': ['True', 'False']}]}]},[])),\
    (('greater ( # 12 , # 34 )'.split(' '),), ({'Greater': [{'Number': [12]}, {'Number': [34]}]},[])),\
    (('xor ( xor ( equal ( # 12 , # 34 ) , false ) , xor ( less ( $ foo , $ bar ) , false ) )'.split(' '),), ({'Xor': [{'Xor': [{'Equal': [{'Number': [12]}, {'Number': [34]}]}, 'False']}, {'Xor': [{'Less': [{'Variable': ['foo']}, {'Variable': ['bar']}]}, 'False']}]},[])),\
    ])


print("\n\nProblem #2, part (e)...")
try: parse
except: print("The parse() function is not defined.")
else: check('parse', parse, [\
    (("end ;",), 'End'),\
    (("print # 123 ; end ;",), {'Print': [{'Number':[123]}, 'End']}),\
    (("print # 123 ; print # 456 ; end ;",), {'Print': [{'Number':[123]}, {'Print': [{'Number': [456]}, 'End']}]}),\
    (("assign $ x := # 1 ; end ;",), {'Assign': [{'Variable': ['x']}, {'Number': [1]}, 'End']}),\
    (("end;",), 'End'),\
    (("print if (true, #1, #0); end;",), {'Print': [{'If':['True',{'Number': [1]},{'Number': [0]}]}, 'End']}),\
    (("assign $x:=#1;end;",), {'Assign': [{'Variable': ['x']}, {'Number': [1]}, 'End']}),\
    (("input $giraffe;end;",), {'Input': [{'Variable': ['giraffe']}, 'End']}),\
    (("input $true; print #123; end;",), {'Input': [{'Variable':['true']}, {'Print': [{'Number': [123]}, 'End']}]}),\
    (("input $x; print #123; assign $x := #123; end;",), {'Input': [{'Variable':['x']}, {'Print': [{'Number': [123]}, {'Assign': [{'Variable': ['x']}, {'Number': [123]}, 'End']}]}]}),\
    (["print plus(if(true,#5,#4),#99); assign $x := #123; end;"], {'Print': [{'Plus': [{'If': ['True', {'Number': [5]}, {'Number': [4]}]}, {'Number': [99]}]}, {'Assign': [{'Variable': ['x']}, {'Number': [123]}, 'End']}]}),\
    (["assign $y := #10; print plus(max($abc,#4),$y); assign $x := #123; end;"], {'Assign': [{'Variable': ['y']}, {'Number': [10]}, {'Print': [{'Plus': [{'Max': [{'Variable':['abc']},{'Number': [4]}]}, {'Variable': ['y']}]}, {'Assign': [{'Variable': ['x']}, {'Number': [123]}, 'End']}]}]}),\
    (("print equal($x,$y); end;",), None),\
    (("print #1; print plus(true,false); end;",), None),\
    (["assign $x := plus(max($y,#20),#30); print if(xor(less($x, $y), xor(equal($y, #200), false)),#0,#0); end;"], {'Assign': [{'Variable': ['x']}, {'Plus': [{'Max': [{'Variable': ['y']}, {'Number': [20]}]}, {'Number': [30]}]}, {'Print': [{'If': [{'Xor': [{'Less': [{'Variable': ['x']}, {'Variable': ['y']}]}, {'Xor': [{'Equal': [{'Variable': ['y']}, {'Number': [200]}]}, 'False']}]}, {'Number': [0]}, {'Number': [0]}]}, 'End']}]}),\
    (["assign $b := if(not(false),if(greater(plus(max($a,#2),#3),#2),#1,#0),#0); end;"], {'Assign': [{'Variable': ['b']}, {'If': [{'Not': ['False']}, {'If': [{'Greater': [{'Plus': [{'Max': [{'Variable': ['a']}, {'Number': [2]}]}, {'Number': [3]}]}, {'Number': [2]}]}, {'Number': [1]}, {'Number': [0]}]}, {'Number': [0]}]}, 'End']}),\
    ])


print("\n\nProblem #3...")
try: parse
except: print("The parse() function is not defined.")
else: check('parse', parse, [\
    (["print ( # 2 + $ x ) ; end ;"], {'Print': [{'Plus': [{'Number': [2]}, {'Variable': ['x']}]}, 'End']}),\
    (["print (#2 max $x) ; end ;"], {'Print': [{'Max': [{'Number': [2]}, {'Variable': ['x']}]}, 'End']}),\
    (["print if((#2 == $x),#1,#0) ; end ;"], {'Print': [{'If':[{'Equal': [{'Number': [2]}, {'Variable': ['x']}]}, {'Number':[1]}, {'Number':[0]}]}, 'End']}),\
    (["print if(((#2 < $x) xor (#2 > $x)),#1,#0) ; end ;"], {'Print': [{'If': [{'Xor': [{'Less': [{'Number': [2]}, {'Variable': ['x']}]}, {'Greater': [{'Number': [2]}, {'Variable': ['x']}]}]}, {'Number': [1]}, {'Number': [0]}]}, 'End']}),\
    (["print (true ? #1 : #2) ; end ;"], {'Print': [{'If': ['True', {'Number': [1]}, {'Number': [2]}]}, 'End']}),\
    (["assign $y := #10; print (if(false,#0,#1) + $y); assign $x := #123; end;"], {'Assign': [{'Variable': ['y']}, {'Number': [10]}, {'Print': [{'Plus': [{'If': ['False', {'Number': [0]}, {'Number': [1]}]}, {'Variable': ['y']}]}, {'Assign': [{'Variable': ['x']}, {'Number': [123]}, 'End']}]}]}),\
    (["assign $y := #100; assign $x := plus(max($y,#20),#30); print if(xor(($y == #200), false),#4,(#5+#6)); end;"], {'Assign': [{'Variable': ['y']}, {'Number': [100]}, {'Assign': [{'Variable': ['x']}, {'Plus': [{'Max': [{'Variable': ['y']}, {'Number': [20]}]}, {'Number': [30]}]}, {'Print': [{'If': [{'Xor': [{'Equal': [{'Variable': ['y']}, {'Number': [200]}]}, 'False']}, {'Number': [4]}, {'Plus': [{'Number': [5]}, {'Number': [6]}]}]}, 'End']}]}]}),\
    (["assign $a := #1; assign $b := (($a max #2) + #3); print if(((($a max #2) + #3)>plus(max($a,#2),#3)),#1,#2); end;"], {'Assign': [{'Variable': ['a']}, {'Number': [1]}, {'Assign': [{'Variable': ['b']}, {'Plus': [{'Max': [{'Variable': ['a']}, {'Number': [2]}]}, {'Number': [3]}]}, {'Print': [{'If': [{'Greater': [{'Plus': [{'Max': [{'Variable': ['a']}, {'Number': [2]}]}, {'Number': [3]}]}, {'Plus': [{'Max': [{'Variable': ['a']}, {'Number': [2]}]}, {'Number': [3]}]}]}, {'Number': [1]}, {'Number': [2]}]}, 'End']}]}]}),\
    ])


#eof
