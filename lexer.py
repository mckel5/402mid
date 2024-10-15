import re

token_specs = [
    ("PRINT", r"print"),
    ("PUSH", r"push"),
    ("POP", r"pop"),
    ("STORE", r"store"),
    ("ASK", r"ask"),
    ("DUP", r"dup"),
    ("JUMPT", r"jumpt"),
    ("JUMPF", r"jumpf"),
    ("JUMP", r"jump"),
    ("STOP", r"stop"),
    ("NOOP", r"noop"),
    ("ADD", r"add"),
    ("SUB", r"sub"),
    ("MUL", r"mul"),
    ("DIV", r"div"),
    ("EQU", r"equ"),
    ("LEQ", r"leq"),
    ("NUMBER", r"-?[0-9]+"),
    ("NAME", r"[a-zA-Z_\$][a-zA-Z0-9_\$]*"),
    ("SEMI", r";"),
    ("COLON", r":"),
    ("COMMENT", r"//.*"),
    ("WHITESPACE", r"[ \t\n]+"),
    ("UNKNOWN", r"."),
]

token_types = set(type_ for (type_, _) in token_specs)


class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __str__(self):
        return "Token({},{})".format(self.type, self.value)


def tokenize(code):
    tokens = []
    re_list = ["(?P<{}>{})".format(type_, re) for (type_, re) in token_specs]
    combined_re = "|".join(re_list)
    match_object_list = list(re.finditer(combined_re, code))
    for mo in match_object_list:
        type_ = mo.lastgroup
        value = mo.group()
        if type_ in ["WHITESPACE", "COMMENT"]:
            continue
        elif type_ == "UNKNOWN":
            raise ValueError("unexpected character '{}'".format(value))
        else:
            tokens.append(Token(type_, value))
    tokens.append(Token("EOF", "eof"))
    return tokens


class Lexer:
    def __init__(self, input_string):
        self.tokens = tokenize(input_string)
        self.curr_token_ix = 0

    def pointer(self):
        return self.tokens[self.curr_token_ix]

    def next(self):
        if not self.end_of_file():
            self.curr_token_ix += 1
        return self.pointer()

    def match(self, token_type):
        if token_type == self.pointer().type:
            tk = self.pointer()
            self.next()
            return tk
        elif token_type not in token_types:
            raise ValueError("unknown token type '{}'".format(token_type))
        else:
            raise SyntaxError(
                "unexpected token {} while parsing, expected {}".format(
                    self.pointer().type, token_type
                )
            )

    def end_of_file(self):
        return self.pointer().type == "EOF"
