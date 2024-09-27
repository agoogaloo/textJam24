variables = ["w","x","y","z"]
varValues = [0,0,0,0]
values = ["0","1","3","5","7","10"]
functions = ["assign(var,value)","increment(var,value)","decrement(var,value)", "for(repeats,function)", "doBoth(func,func)"]

#stores types required by functions to execute line can have func, val
typeStack = ["func"]



def play(players, lines):
    program = " "
    currPlayer = 0
    while lines>0:
        inputLine = input()
        executeLine(inputLine, "func")
        program +=inputLine+"\n"
        lines-=1
        currPlayer+=1
        currPlayer = currPlayer%players
        print("current program:\n"+program)
        print("player ",currPlayer," turn")
        print(lines,"lines left to write")

def executeLine(line, type):
    print("executing line '",line,"' as ",type)
    match type:
        case "func":
            paramStart = line.index("(")
            bracketStack=1
            paramEnd = paramStart+1
            while bracketStack>0:
                if line[paramEnd] =="(":
                    bracketStack+=1
                elif line[paramEnd] ==")":
                    bracketStack-=1
                paramEnd+=1

            symbol = line[0:paramStart]
            params = line[paramStart+1:paramEnd-1].split(",")
            paramTypes = getArgs(symbol)
            # print("line:"+line)
            # print("symbol: '"+symbol+"'")
            # print("params:",params," types:",paramTypes)
                
            for i in range(len(params)):
                if paramTypes[i]!= "func":
                    params[i]=executeLine(params[i],paramTypes[i])
            executeSymbol(symbol, params)

        case "val":
            if line in variables:
                val = varValues[variables.index(line)]
                # print("returning",line,"=",val)
                return val
            # print("(default) returning",int(line))
            return int(line)
        case "var":
            return line
        case _:
            print(line," with type ",type," not found")

def getArgs(symbol):
    match symbol:
        case "assign":
            return["var", "val"]
        case "for":
            return["val","func"]
        case "print":
            return["val"]
        case "doBoth":
            return ["func","func"]
        case "increment":
            return["var","val"]
        case "decrement":
            return["var","val"]
        case _:
            print("cant get args for symbol "+symbol)
            return[]

def executeSymbol(name, args):
    match name:
        case "assign":
            assign(args[0], args[1])
        case "for":
            for i in range(args[0]):
                executeLine(args[1],"func")
        case "print":
            print(" ->",args[0])
        case "doBoth":
            executeLine(args[0],"func")
            executeLine(args[1],"func")

def add(x,y):
    if(not x in variables):
        return "x:",x," is not a settable variable"
    varValues[variables.index(x)] += y
    
def sub(x,y):
    if(not x in variables):
        return "x:",x," is not a settable variable"
    varValues[variables.index(x)] -= y
def assign(x,y):
    if(not x in variables):
        return "x:",x," is not a settable variable"
    varValues[variables.index(x)] = y



def onInput(input):
    print("intput:",input)
