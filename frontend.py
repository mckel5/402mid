from state import state

# lookahead sets for parser
instr_lookahead = [
    "PRINT",
    "PUSH",
    "POP",
    "STORE",
    "ASK",
    "DUP",
    "ADD",
    "SUB",
    "MUL",
    "DIV",
    "EQU",
    "LEQ",
    "JUMPT",
    "JUMPF",
    "JUMP",
    "STOP",
    "NOOP",
]
labeled_instr_lookahead = instr_lookahead + ["NAME"]


# instr_list : ({NAME, PRINT, PUSH, POP, STORE, ASK, DUP, ADD, SUB, MUL, DIV,
#                EQU, LEQ, JUMPT, JUMPF, JUMP, STOP, NOOP} labeled_instr)*
def instr_list(stream):
    while stream.pointer().type in labeled_instr_lookahead:
        labeled_instr(stream)
    return None


# labeled_instr : {NAME} label_def instr
#               | {PRINT, PUSH, POP, STORE, ASK, DUP, ADD, SUB, MUL, DIV, EQU,
#                  LEQ, JUMPT, JUMPF, JUMP, STOP, NOOP} instr
def labeled_instr(stream):
    token = stream.pointer()
    if token.type in ["NAME"]:
        l = label_def(stream)
        i = instr(stream)
        state.label_table[l] = state.instruction_index
        state.program.append(i)
        state.instruction_index += 1
        return None
    elif token.type in instr_lookahead:
        i = instr(stream)
        state.program.append(i)
        state.instruction_index += 1
        return None
    else:
        raise SyntaxError("labeled_instr: syntax error at {}".format(token.value))


# label_def : {NAME} label COLON
def label_def(stream):
    token = stream.pointer()
    if token.type in ["NAME"]:
        l = label(stream)
        stream.match("COLON")
        return l
    else:
        raise SyntaxError("label_def: syntax error at {}".format(token.value))


# instr : {PRINT} PRINT SEMI
#       | {PUSH} PUSH arg SEMI
#       | {POP} POP SEMI
#       | {STORE} STORE var SEMI
#       | {ASK} ASK SEMI
#       | {DUP} DUP SEMI
#       | {ADD} ADD SEMI
#       | {SUB} SUB SEMI
#       | {MUL} MUL SEMI
#       | {DIV} DIV SEMI
#       | {EQU} EQU SEMI
#       | {LEQ} LEQ SEMI
#       | {JUMPT} JUMPT label SEMI
#       | {JUMPF} JUMPF label SEMI
#       | {JUMP} JUMP label SEMI
#       | {STOP} STOP SEMI
#       | {NOOP} NOOP SEMI
def instr(stream):
    no_args = [
        "PRINT",
        "POP",
        "ASK",
        "DUP",
        "ADD",
        "SUB",
        "MUL",
        "DIV",
        "EQU",
        "LEQ",
        "STOP",
        "NOOP",
    ]

    jumps = ["JUMPT", "JUMPF", "JUMP"]

    token = stream.pointer()

    if token.type in no_args:
        stream.match(token.type)
        stream.match("SEMI")
        return (token.type,)
    elif token.type in ["PUSH"]:
        stream.match("PUSH")
        a = arg(stream)
        stream.match("SEMI")
        return ("PUSH", a)
    elif token.type in ["STORE"]:
        stream.match("STORE")
        v = var(stream)
        stream.match("SEMI")
        return ("STORE", v)
    elif token.type in jumps:
        stream.match(token.type)
        l = label(stream)
        stream.match("SEMI")
        return (token.type, l)
    else:
        raise SyntaxError("instr: syntax error at {}".format(token.value))


# arg : {NUMBER} num
#     | {NAME} var
def arg(stream):
    token = stream.pointer()
    if token.type in ["NAME"]:
        v = var(stream)
        return ("NAME", v)
    elif token.type in ["NUMBER"]:
        n = num(stream)
        return ("NUMBER", n)
    else:
        raise SyntaxError("arg: syntax error at {}".format(token.value))


# label : {NAME} NAME
def label(stream):
    token = stream.pointer()
    if token.type in ["NAME"]:
        stream.match("NAME")
        return token.value
    else:
        raise SyntaxError("label: syntax error at {}".format(token.value))


# var : {NAME} NAME
def var(stream):
    token = stream.pointer()
    if token.type in ["NAME"]:
        stream.match("NAME")
        return token.value
    else:
        raise SyntaxError("var: syntax error at {}".format(token.value))


# num : {NUMBER} NUMBER
def num(stream):
    token = stream.pointer()
    if token.type in ["NUMBER"]:
        stream.match("NUMBER")
        return token.value
    else:
        raise SyntaxError("num: syntax error at {}".format(token.value))


# parser top-level driver
def parse(stream):
    from lexer import Lexer

    token_stream = Lexer(stream)
    instr_list(token_stream)  # call the parser function for start symbol
    if not token_stream.end_of_file():
        raise SyntaxError(
            "parse: syntax error at {}".format(token_stream.pointer().value)
        )


if __name__ == "__main__":
    import sys
    import os

    if len(sys.argv) == 1:  # no args - read stdin
        char_stream = sys.stdin.read()
    else:  # last arg is filename to open and read
        input_file = sys.argv[-1]
        if not os.path.isfile(input_file):
            print("unknown file {}".format(input_file))
            sys.exit(0)
        else:
            f = open(input_file, "r")
            char_stream = f.read()
            f.close()

    parse(char_stream)
    print("Parse successful!")
