#!/usr/bin/env python

from frontend import parse
from state import state

#####################################################################################
def interpret_program():
    state.instruction_index = 0

    # interpret until end of program or STOP code reached
    while True:
        if state.instruction_index == len(state.program):
            break  # no more instructions
        else:
            instruction = state.program[state.instruction_index]  # fetch instruction

        # instruction format: (type, [arg])
        instruction_type = instruction[0]

        # interpret instruction
        if instruction_type == "PRINT":
            # PRINT
            val = state.stack.pop()
            print(val)
            state.instruction_index += 1

        elif instruction_type == "PUSH":
            # PUSH arg
            val = eval_arg(instruction[1])
            state.stack.append(val)
            state.instruction_index += 1

        elif instruction_type == "POP":
            # POP
            state.stack.pop()
            state.instruction_index += 1

        elif instruction_type == "STORE":
            # STORE var
            var_name = instruction[1]
            val = state.stack.pop()
            state.symbol_table[var_name] = val
            state.instruction_index += 1

        elif instruction_type == "ASK":
            # ASK
            val = input("Enter an integer value: ")
            state.stack.append(int(val))
            state.instruction_index += 1

        elif instruction_type == "DUP":
            # DUP
            state.stack.append(state.stack[-1])
            state.instruction_index += 1

        elif instruction_type == "ADD":
            # ADD
            v1 = state.stack.pop()
            v2 = state.stack.pop()
            state.stack.append(v2 + v1)
            state.instruction_index += 1

        elif instruction_type == "SUB":
            # SUB
            v1 = state.stack.pop()
            v2 = state.stack.pop()
            state.stack.append(v2 - v1)
            state.instruction_index += 1

        elif instruction_type == "MUL":
            # MUL
            v1 = state.stack.pop()
            v2 = state.stack.pop()
            state.stack.append(v2 * v1)
            state.instruction_index += 1

        elif instruction_type == "DIV":
            # DIV
            v1 = state.stack.pop()
            v2 = state.stack.pop()
            state.stack.append(v2 // v1)
            state.instruction_index += 1

        elif instruction_type == "EQU":
            # EQU
            v1 = state.stack.pop()
            v2 = state.stack.pop()
            state.stack.append(1 if v2 == v1 else 0)
            state.instruction_index += 1

        elif instruction_type == "LEQ":
            # LEQ
            v1 = state.stack.pop()
            v2 = state.stack.pop()
            state.stack.append(1 if v2 <= v1 else 0)
            state.instruction_index += 1

        elif instruction_type == "JUMPT":
            # JUMPT label
            val = state.stack.pop()
            if val:
                state.instruction_index = state.label_table[instruction[1]]
            else:
                state.instruction_index += 1

        elif instruction_type == "JUMPF":
            # JUMPF label
            val = state.stack.pop()
            if not val:
                state.instruction_index = state.label_table[instruction[1]]
            else:
                state.instruction_index += 1

        elif instruction_type == "JUMP":
            # JUMP label
            state.instruction_index = state.label_table[instruction[1]]

        elif instruction_type == "STOP":
            # STOP
            break

        elif instruction_type == "NOOP":
            # NOOP
            state.instruction_index += 1

        else:
            raise ValueError("Unexpected instruction: {}".format(instruction_type))


#####################################################################################
def eval_arg(node):
    "evaluate arg to an integer value"

    # nodes are tuples (type, arg)
    node_type = node[0]

    if node_type == "NAME":
        # NAME var
        return state.symbol_table.get(node[1], 0)

    elif node_type == "NUMBER":
        # NUMBER num
        return int(node[1])

    else:
        raise ValueError("Unexpected node type: {}".format(node_type))


#####################################################################################
def interpret(input_stream):
    "Driver for the interpreter"

    try:
        parse(input_stream)  # build the IR
        interpret_program()  # interpret the IR
    except Exception as e:
        print("error: " + str(e))


#####################################################################################
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

    interpret(char_stream)
