class State:
    def __init__(self):
        self.program = []
        self.stack = []
        self.symbol_table = {}
        self.label_table = {}
        self.instruction_index = 0

# Initialize state on import
# This allows a common state to be shared between modules
state = State()
