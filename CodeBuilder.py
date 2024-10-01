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
    print(typeStack)
    print(paramStack,len(paramStack))
    print(line)


def printOptions(_availableOptions):
    global availableOptions
    availableOptions =_availableOptions 

    print(availableOptions)
    if(len(typeStack)==0):
        print("typestack is empty??")
        return
    options = []
    subOpts= []
    print("  --==  AVAILABLE SYMBOLS  ==--")
    match typeStack[-1]:
        case "func":
            options = functions
            subOpts = funcSubs
        case "var":
            options = variables
            subOpts= variables
        case "val":
            options = variables+values
            subOpts= variables+values
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

listener = keyboard.Listener(on_press=on_press)
listener.start()

