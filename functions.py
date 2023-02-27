fdict = dict()
def function(f=None, name=None):
    if name is None: name = f.__name__
    def inner(func):
        fdict[name] = func
        return func
    if f is None:
        return inner
    else:
        return inner(f)

@function
def int_add(program, dest, value):
    program.var[dest] += int(value)

@function(name="print") #Avoid conflict with builtin function
def print_(program, *args):
    print(*args)

@function
def print_var(program, var):
    print(program.var[var])

@function
def int_gt(program, var, comp, dest_label):
    if program.var[var] > int(comp):
        program.pointer = program.labels[dest_label] - 1

@function
def int_set(program, var, value):
    program.var[var] = int(value)

@function
def goto(program, dest_label):
         program.pointer = program.labels[dest_label] - 1
    
