from pynput import keyboard
import pynput


variables = ["i","x","y","z"]
values = ["0","1","2","4","8","rand"]
functions = ["getSymbols(value)","removeSymbols(value)", "print(value)","increment(var,value)","divide(var,value)", 
            "multiply(var,value)", "for(var,func)", "doBoth(func,func)"]
funcSubs = ["addsbl","rmvsbl", "print","incr","div","mul","for","both" ]
availableOptions=["print","x","i","assign"]



typeStack = ["func"]
paramStack = [1]
line = ""

print(typeStack)
def startTurn():
    global typeStack
    global paramStack
    global line
    typeStack = ["func"]
    paramStack = [1]
    line = ""

def onEnter(input):
    from Game import playLine,printGame
    if len(typeStack)==0:
        playLine(line)
        printGame()
        
        return


    if input =="addsbl" or input == "getSymbols":
        print("addsbl(val)")
        print("takes a value and gives you that many new symbols for your next turn")
    elif input =="rmvsbl" or input == "removeSymbols":
        print("rmvsbl(val)")
        print("takes a value and removes that many symbols from your opponents")
        print("it removes <value> symbols total, not per player, and they get start the player next in the turn order")
    elif input =="print" :
        print("print(val)")
        print("takes a value (either a varaible or direct number value) and gives you that many points")
    elif input =="assign" :
        print("assign(var,val)")
        print("sets a variable to be the given value, or the value of another variable")
    elif input =="incr" or input=="increment" :
        print("incr(var,val)")
        print("increases the value of a variable by the given amount")
    elif input =="div" or input == "divide":
        print("decr(var,val)")
        print("integer divides the variable by an amount (rounds down to the nearest int)")
        print("dividing by 0 sets the variable to -1")
    elif input =="for":
        print("for(var,func)")
        print("executes func, and decrements var by 1 until var is less or equal to 0")
    elif input =="both" or input=="doBoth":
        print("both(func,func)")
        print("executes both functions passed to it ")
    elif input =="rand":
        print("a random value from [0-8] inclusive")
        
    else:
        print("use 0-9 to write your line of code.\nprint numbers to get points!\ntype a function name for a description")


def addSymbol(idx):
    from Game import getArgs, printGame,useSymbol
    if len(typeStack)==0:
        return
    global line
    symbolList = []
    match typeStack[-1]:
        case "func":
            symbolList=funcSubs
            
        case"var":
            symbolList=variables
        case "val":
            symbolList= (variables+values)
    if idx>=len(symbolList) or (availableOptions.count(symbolList[idx])==0 and idx!=0):
        return
    symbol = symbolList[idx]
    useSymbol(symbol)

    
    args = getArgs(symbol)

    line+=symbol
    if typeStack[-1] =="func":
        line+="("
        paramStack.append(len(args))
    while(paramStack[-1]==0):
        paramStack.pop(-1)
        line+=")"
    if len(typeStack)>1 and typeStack[-1]!="func":
        line+=","
    typeStack.pop(-1)
    paramStack[-1]-=1
    args.reverse()
    typeStack.extend(args)
    printGame()


def printSymbolList(optionList,varValues):
    funcCounts = [0]*len(funcSubs)
    varCounts =  [0]*len(variables)
    valueCounts = [0]*len(values)
    for opt in optionList:
        if opt in funcSubs:
            funcCounts[funcSubs.index(opt)]+=1
        if opt in values:
            valueCounts[values.index(opt)]+=1
        if opt in variables:
            varCounts[variables.index(opt)]+=1

    print("     --==  Inventory  ==--")
    print(" -Values:",end="")
    print(values[0]+"(xINF)  ",end="")
    for i in range(1,len(values)):
        if valueCounts[i]!=0:
            print(values[i]+"(x"+str(valueCounts[i])+")  ",end="")
    print("")

    print(" -Variables:",end="")
    print(variables[0]+"="+str(varValues[0])+" (xINF)  ",end="")
    for i in range(1,len(variables)):
        if varCounts[i]!=0:
            print(variables[i]+"="+str(varValues[i])+" (x"+str(varCounts[i])+")  ",end="")
    print("")

    print(" -Functions:",end="")
    print(funcSubs[0]+"(xINF)  ",end="")
    for i in range(1,len(funcSubs)):
        if funcCounts[i]!=0:
            print(funcSubs[i]+"(x"+str(funcCounts[i])+")  ",end="")
    print("")



def printOptions(_availableOptions,varValues):
    global availableOptions
    availableOptions =_availableOptions 
    if(len(typeStack)==0):
        print(" -- Enter To Execute Line --")
        print(" >",line)
        return
    options = []
    subOpts= []
    printSymbolList(availableOptions,varValues)
    print("     --==  AVAILABLE SYMBOLS  ==--")
    match typeStack[-1]:
        case "func":
            options = functions
            subOpts = funcSubs
        case "var":
            options = variables.copy()
            subOpts= variables
            for i in range(len(variables)):
                options[i]+= "="+str(varValues[i])
        case "val":
            options = variables.copy()+values
            subOpts= variables+values
            for i in range(len(variables)):
                options[i]+= "="+str(varValues[i])
    counts = [0]*len(options)
    for opt in availableOptions:
        if opt in subOpts:
            counts[subOpts.index(opt)]+=1

    print("(inf) [0]:",options[0],"   ", end="")
    optNum = 1
    for i in range(len(options)):
        if counts[i]==0:
            continue
        optNum+=1
        if optNum%3==2:
            print("(x"+str(counts[i])+") ["+str(i)+"]:",options[i],"   ")
        else:
            print("(x"+str(counts[i])+") ["+str(i)+"]:",options[i],"   ", end="")
    if optNum%3!=2:
        print("")
    print(" >",line)

def on_press(key):
    try:
        if key.char.isdigit():
            pass
            addSymbol(int(key.char))
        if key==pynput.keyboard.Key.enter:
            from Game import playLine
            playLine(line)
            
    except AttributeError:
        pass

def startBuilder():
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

