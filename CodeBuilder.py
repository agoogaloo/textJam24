from pynput import keyboard
import pynput


variables = ["i","x","y","z"]
values = ["0","1","2","4","8","rand"]
functions = ["print(value)","assign(var,value)","increment(var,value)","decrement(var,value)", 
             "for(repeats,function)", "doBoth(func,func)", "jump(value)","getSymbols(value)"]
funcSubs = ["print","assign","incr","decr","for","both", "jump","symbol"]
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

def addSymbol(idx):
    from Game import getArgs, playLine, printGame
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
    if(len(typeStack)==0):
        playLine(line)


    printGame()
    print(line)


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
        print("typestack is empty??")
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

    print("[0]: (inf) ",options[0],"   ", end="")
    optNum = 1
    for i in range(len(options)):
        if counts[i]==0:
            continue
        optNum+=1
        if optNum%3==2:
            print("["+str(i)+"]: (x"+str(counts[i])+") ",options[i],"   ")
        else:
            print("["+str(i)+"]: (x"+str(counts[i])+") ",options[i],"   ", end="")
    print("")

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

