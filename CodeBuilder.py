from pynput import keyboard
from Game import getArgs

variables = ["w","x","y","z"]
values = ["0","1","3","5","7","10"]
functions = ["assign(var,value)","increment(var,value)","decrement(var,value)", 
             "for(repeats,function)", "doBoth(func,func)", "if(var, func)", "goto(value"]
funcSubs = ["print","assign","incr","decr","for","both", "if","goto"]

typeStack = ["func"]
paramStack = [1]
line = ""

print(typeStack)
def addSymbol(idx):
    if len(typeStack)==0:
        return
    global line
    symbol =""
    match typeStack[-1]:
        case "func":
            symbol=funcSubs[idx]
            
        case"var":
            symbol=variables[idx]
        case "val":
            symbol= (values+variables)[idx]


    
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

    print(typeStack)
    print(paramStack,len(paramStack))
    print(line)



def on_press(key):
    try:
        if key.char.isdigit():
            addSymbol(int(key.char))
    except AttributeError:
        pass

listener = keyboard.Listener(on_press=on_press)
listener.start()

