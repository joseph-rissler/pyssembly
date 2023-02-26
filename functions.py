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
def add(program, args):
    dest, value = args.split()
    program.var[dest] += int(value)

@function(name="print") #Avoid conflict with builtin function
def print_(program, args):
    print(args)
