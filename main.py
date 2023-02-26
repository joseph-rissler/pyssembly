import argparse
from functions import fdict

parser = argparse.ArgumentParser()
parser.add_argument("inputFile", help="File to interpret")
command_line = parser.parse_args()

class ExecutionHalt(Exception): pass

class Program:
    @classmethod
    def fromLines(cls, lines):
        new = cls()
        for line in lines:
            line = line.strip()
            command, arg = line.split(maxsplit=1)
            new.instructions.append(lambda: fdict[command](new, arg))
        return new

    @classmethod
    def fromFile(cls, filename):
        with open(filename) as file: 
            return cls.fromLines(file.readlines())
    
    def __init__(self):
        self.var = dict()
        self.pointer = 0
        self.instructions = list()

    def step(self):
        self.instructions[self.pointer]()
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
    prog = Program.fromFile(command_line.inputFile)
    prog.run()
