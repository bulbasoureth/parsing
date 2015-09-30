# parsing
parsing in linux
program ::= print term ; program
        | input $ variable ; program
        | assign $ variable := term ; program
        | end ;

formula ::= true | false | not ( formula ) | xor ( formula , formula )
        | equal ( term , term ) | less ( term , term ) | greater ( term , term )
        | ( formula xor formula )
        | ( term == term ) | ( term < term ) | ( term > term )
term ::= # number | $ variable | plus ( term , term ) | max ( term , term ) | if ( formula , term , term )
      | ( term + term ) | ( term max term )
      | ( formula ? term : term )

variable ::= non-empty character strings containing only alphabetical characters (lowercase or uppercase)
number ::= positive integers or negative integers preceded by −
