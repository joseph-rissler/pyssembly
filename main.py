import argparse
import re
from functions import fdict

class ExecutionHalt(Exception): pass
class ParsingError(Exception): pass

WHITESPACE = " \t\v\n\r\f"
QUOTES = "'\""
def tokenize(line):
    token_list = list()
    current_token = ""
    escape = False
    quote_match = None
    def finish_token():
        nonlocal current_token, token_list, escape, quote_match
        if current_token:
            token_list.append(current_token)
            current_token = ""
        escape = False
        quote_match = None
    for char in line:
        if escape:
            current_token += char
            escape = False
        elif char == "\\":
            escape = True
        elif quote_match:
            if char == quote_match:
                finish_token()
            else:
                current_token += char
        elif char in WHITESPACE:
            finish_token()
        elif char in QUOTES:
            if current_token:
                raise ParsingError("No whitespace before string")
            else:
                quote_match = char
        elif char == "#":
            finish_token()
            break
        else:
            current_token += char
    if quote_match:
        raise ParsingError("Unmatched quote")
    finish_token()
    return token_list
                    

re_label = re.compile(r':(?P<label>\w+):')

class Program:

    @classmethod
    def fromLines(cls, lines):
        new = cls()
        for line in lines:
            tokens = tokenize(line)
            if len(tokens) == 1 and re_label.fullmatch(tokens[0]):
                label = re_label.fullmatch(tokens[0]).group('label')
                assert label not in new.labels, "Duplicate Label"
                new.labels[label] = len(new.instructions)
            else:
                command = tokens[0]
                args = tokens [1:]
                new.instructions.append(
                    (fdict[command], *args)
                )
        return new

    @classmethod
    def fromFile(cls, filename):
        with open(filename) as file: 
            return cls.fromLines(file.readlines())
    
    def __init__(self):
        self.var = dict()
        self.labels = dict()
        self.pointer = 0
        self.instructions = list()

    def step(self):
        command, *args = self.instructions[self.pointer]
        command(self, *args)
        self.pointer += 1
        if self.pointer >= len(self.instructions):
            raise ExecutionHalt

    def run(self):
        try:
            while True:
                self.step()
        except ExecutionHalt:
            pass
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inputFile", help="File to interpret")
    command_line = parser.parse_args()
    inputFile = command_line.inputFile
    
    Program.fromFile(inputFile).run()
