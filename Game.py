import CodeBuilder
from random import randint

variables = ["i","x","y","z"]
varValues = [0,1,2,4]

#stores types required by functions to execute line can have func, val
typeStack = ["func"]


program = ""
players = 1
currPlayer = 0
lines = 5

availableSymbols = []
points = []

def play(_players, _lines):
    global players 
    global lines
    global builderOptions
    global availableSymbols
    global points
    players = _players
    for i in range(players):
        availableSymbols.append(["print","mul"])
        drawNewSymbols(i,4+i)
    points= [0]*players
    print("symbol list:",availableSymbols)
    lines = _lines
    
    CodeBuilder.startBuilder()
    printGame()
    while(lines>0):
        CodeBuilder.onEnter(input())

def printProgram():
    print("     --== PROGRAM ==--")
    lines = program.split("\n")
    for i in range(len(lines)-1):
        print(i+1,":",lines[i])
    print("---------------------------")
def printGame():
    print("\n\n\n\n\n\n")
    
    printProgram()

    print(" PLAYER "+str(currPlayer)+" TURN   ",end="")
    print(lines,"lines left ")
    print("     --==  SCORE  ==--")
    for i in range(players):
        print("Player"+str(i)+":",points[i],end="   ")
    print("")
    CodeBuilder.printOptions(availableSymbols[currPlayer],varValues)
    print("\n")

def drawNewSymbols(playnum = currPlayer, amount = 3):
    symbolList = CodeBuilder.funcSubs[1::]+CodeBuilder.funcSubs[1::]+CodeBuilder.variables[1::]+CodeBuilder.values[1::]+CodeBuilder.variables[1::]
    
    print("symbolList:")
    print(symbolList)
    print("player",playnum,"getting new symbols")
    for i in range(amount):
        randIdx = randint(0,len(symbolList)-1)
        availableSymbols[playnum].append(symbolList[randIdx])
    print(availableSymbols)

def useSymbol(name):
    if availableSymbols[currPlayer].count(name)==0:
        print(name,"not in",availableSymbols[currPlayer])
        return
    availableSymbols[currPlayer].remove(name)

def playLine( line):
    global program
    global players 
    global currPlayer
    global lines
    global builderOptions

    executeLine(line)
    program +=line+"\n"
    lines-=1
    currPlayer+=1
    currPlayer = currPlayer%players
    drawNewSymbols(currPlayer)
    CodeBuilder.startTurn()


def getParamLength(symbols):
    typeStack = ["func"]
    lastParam=0
    while(len(typeStack)>0):
        typeStack.pop(-1)
        exension =getArgs(symbols[lastParam])
        typeStack.extend( exension)
        # print(symbols[lastParam],"needs",exension,"current stack",typeStack)
        lastParam+=1
    return lastParam

def executeLine(line):
    line = line.replace("("," ")
    line = line.replace(")"," ")
    line = line.replace(","," ")
    while line.__contains__("  "):
        line = line.replace("  ", " ")
    line = line.strip()
    executeSymbols(line.split(" "), "func")
def executeSymbols(symbols, type ):
    
    print("executing symabols",symbols,"as type",type)
    match type:
        case "func":
            lastParam =  getParamLength(symbols)
            print("func",symbols[0],"using params",symbols[1:lastParam+1])
            executeSymbol(symbols[0], symbols[1:lastParam+1])

        case "val":
            if symbols=="rand":
                return randint(0,8)
            if symbols in variables:
                val = varValues[variables.index(symbols)]
                print("returning",symbols,"=",val)
                return val
            print("(default) returning",int(symbols))
            return int(symbols)
        case "var":
            return symbols 
        case _:
            print(symbols," with type ",type," not found")

def getArgs(symbol):
    match symbol:
        case "assign":
            return["var", "val"]
        case "for":
            return["var","func"]
        case "print":
            return["val"]
        case "both":
            return ["func","func"]
        case "incr":
            return["var","val"]
        case "div":
            return["var","val"]
        case "mul":
            return["var","val"]
        case "rmvsbl":
            return["val"]
        case "addsbl":
            return["val"]
        case _:
            # print("cant get args for symbol ",symbol)
            return[]

def executeSymbol(name, args):
    match name:
        case "assign":
            args[1] = executeSymbols(args[1], "val")
            assign(args[0], args[1])
        case "incr":
            args[1] = executeSymbols(args[1], "val")
            add(args[0], args[1])
        case "div":
            args[1] = executeSymbols(args[1], "val")
            div(args[0], args[1])
        case "mul":
            args[1] = executeSymbols(args[1], "val")
            mul(args[0], args[1])
        case "for":
            index = variables.index(args[0])
            while(varValues[index]>0):
                executeSymbols(args[1::],"func")
                varValues[index]-=1;
        case "print":
            args[0] = executeSymbols(args[0], "val")
            points[currPlayer]+=args[0]
            print(" ->",args[0])
        case "both":
            index = getParamLength(args)
            executeSymbols(args[0:index],"func")
            executeSymbols(args[index::],"func")
        case "rmvsbl":
            args[0] = executeSymbols(args[0], "val")
            removeSymbol(args[0])
            pass
        case "addsbl":
            args[0] = executeSymbols(args[0], "val")
            drawNewSymbols(amount=args[0])
            pass
        case _:
            print("cant execute symbol "+name)

def removeSymbol(times):
    
    victim = currPlayer
    # cycling through all the players
    for i in range(times):
        victim+=1
        if victim%players==currPlayer:
            victim+=1
        victim = victim%players
        # removing a random symbol
        options = len(availableSymbols[victim])
        if options==0:
            print("p",victim,"has no symbols to take")
            return
        index = randint(0,options-1)
        print("index",index)
        print("removing",availableSymbols[victim][index],"from p",victim)
        availableSymbols[victim].pop(index)



def add(x,y):

    if(not x in variables):
        print("x:",x," is not a settable variable")
        return
    print("inctementing",x,"by",y)
    varValues[variables.index(x)] += int(y)
    
def div(x,y):
    if(not x in variables):
        return "x:",x," is not a settable variable"
    if y==0:
        print("y=0, setting",x,"to -1")
        varValues[variables.index(x)]   =-1
        return

    varValues[variables.index(x)] = int(varValues[variables.index(x)] / int(y))
def mul(x,y):
    if(not x in variables):
        return "x:",x," is not a settable variable"

    varValues[variables.index(x)] = int(varValues[variables.index(x)] * int(y))
def assign(x,y):
    if(not x in variables):
        return "x:",x," is not a settable variable"
    varValues[variables.index(x)] = int(y)



def onInput(input):
    print("intput:",input)
