from pynput import keyboard
import pynput


variables = ["i","x","y","z"]
values = ["0","1","2","4","8"]
functions = ["print(value)","assign(var,value)","increment(var,value)","decrement(var,value)", 
             "for(repeats,function)", "doBoth(func,func)", "if(var, func)", "jump(value)"]
funcSubs = ["print","assign","incr","decr","for","both", "if","jump"]



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
            symbolList= (values+variables)
    if(idx>=len(symbolList)):
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


def printOptions():
    if(len(typeStack)==0):
        print("typestack is empty??")
        return
    options = []
    print("  --==  AVAILABLE SYMBOLS  ==--")
    match typeStack[-1]:
        case "func":
            options = functions
        case "var":
            options = variables
        case "val":
            options = values+variables

    for i in range(len(options)):
        if i%3==2:
            print("["+str(i)+"]:",options[i],"   ")
        else:
            print("["+str(i)+"]:",options[i],"   ",end="")
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

