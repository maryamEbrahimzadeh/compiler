#compiler developed by maryam  ebrahimzadeh
#maryam.ebrahimzadeh1997@yahoo.com
# 22 june 2017
import re
import  stackClass

#variables
register_file = []
register_file = range(64)
register_file[0] = 0
for x in range(1 ,63):
    register_file[x]=''

wp = 0
assembly = []
code = []
numbers = []
def findSetReg (name):
    i = find_Ereg()
    if i==-1 :
        raise Exception("registerfile is full")
        return False
    else :
        set_Reg(i,name)
        return  True

def find_reg(name):
    for x in range(1,len(register_file)):
        if register_file[x]== name :
            return x
    return -1

def assmbel_if_variable_declarations01(variable,number):
    for i in range(0,len(variable)):
        reg = find_reg(variable[i])
        assembly.append("mil " + "R" + str(reg) + " "+ number)
        assembly.append("mih " + "R" + str(reg) + " " + number)


def if_variable_declarations(line):
    #int a,b = 5 + 3;
    words = re.findall(r'[^,;\s]+', line)
    i=1
    variable=[]
    while words[i] != '=':
        variable.append(words[i])
        findSetReg(words[i])
        i=i+1
    i = i+1
    if i==len(words)-1:
        assmbel_if_variable_declarations01(variable,words[i])
    else:
        phrase = words[i:]
        r =postfix_if_variable_declarations(phrase,i)
        for i in range(0, len(variable)):
            reg = find_reg(variable[i])
            assembly.append("str R62 " + " R" + r)
            assembly.append("lda "+ "R" + str(reg)+" R62")




def set_Reg(addr,name):
    register_file[addr] = name

def find_Ereg():
    for x in range(0,63):
        if register_file[x]=='' :
            return x
    return -1

def postfix_if_variable_declarations(phrase,i):
    phrase = infixtopostfix(phrase)
    return evaluate_postfix(phrase)


def infixtopostfix(tokenlst):
    s=stackClass.StackClass([])
    outlst=[]
    prec={}
    prec['/']=3
    prec['*']=3
    prec['+']=2
    prec['-']=2
    prec['(']=1
    oplst=['/','*','+','-']

    for token in tokenlst:
        if  token in '0123456789':
            outlst.append(token)

        elif token == '(':
            s.push(token)

        elif token == ')':
            topToken=s.pop()
            while topToken != '(':
                outlst.append(topToken)
                topToken=s.pop()
        else:
            while (not s.isEmpty()) and (prec[s.peek()] >= prec[token]):
                outlst.append(s.pop())

            s.push(token)

    while not s.isEmpty():
        opToken=s.pop()
        outlst.append(opToken)

    return outlst
    #return " ".join(outlst)

def evaluate_postfix(text):
    r = []
    print  text
    assembly.append("ccf")
    dr = None
    for symbol in text :
        dr = None
        if str(symbol).isdigit()  :
            #find a reg for it
            findSetReg(symbol)
            r.append(str(find_reg(symbol)))
            assembly.append("cwp")
            assembly.append("awp "+str(find_reg(symbol)))
            assembly.append("mil R" + str(find_reg(symbol))+" " + symbol)
            assembly.append("mih R" + str(find_reg(symbol))+" "+ symbol)
        elif  len(r)>0 :
            dr = r[len(r)-1]
            r.pop(len(r)-1)
            sr = r[len(r)-1]
            r.pop(len(r) - 1)
            calculate0("R"+dr,"R"+sr,str(symbol))
            r.append(dr)
        else:
             raise Exception("r is empty")
    return dr
def calculate0(r1,r2,op):
    #r1 <= r1+r2
    # r62 = 0
    # r63 = 1
    assembly.append("cwp")
    assembly.append("awp 60")
    assembly.append("mil R2 0" )
    assembly.append("mih R2 0" )
    assembly.append("mil R3 1")
    assembly.append("mih R3 1")
    assembly.append("str R2 "+ r1)
    assembly.append("str R3 "+ r2)
    assembly.append("lda R0 r62")
    assembly.append("lda R1 r63")
    #now i have mu number in r60 and r61
    if(op=="+"):
        assembly.append("ADD R0 R1")
    elif op=="-":
        assembly.append("SUB R0 R1")
    elif op=="*":
        assembly.append("mul R0 R1")
    elif op=="/":
        assembly.append("DIV R0 R1");
    assembly.append("str R2 R0" )# (r62) <= r60
    assembly.append("lda "+r1+" R2")

def calculate_assignments1(text):
    #a += b
    words = text.split();
    if words[1] == "+=":
        calculate0(find_reg(words[0]),find_reg(words[2]),"+")
    elif words[1] == "-=":
        calculate0(find_reg(words[0]),find_reg(words[2]),"-")
    elif words[1] == "/=":
        calculate0(find_reg(words[0]),find_reg(words[2]),"/")
    elif words[1] == "*=":
        calculate0(find_reg(words[0]),find_reg(words[2]),"*")
    elif words[1]=="=":
        if len(words)==3:
            assembly.append("cwp")
            assembly.append("awp 60")
            assembly.append("mil R2 0")
            assembly.append("mih R2 0")
            assembly.append("str R2 " +find_reg(words[2]) )
            assembly.append("lda R" + find_reg(words[0]) +"R62")
        else:
            dr = evaluate_postfix(words[3:])
            if words[1] =="+" :
                calculate0(find_reg(words[0]), dr, "+")
            elif words[1] =="-":
                calculate0(find_reg(words[0]), dr, "-")
            elif words[1] =="/":
                calculate0(find_reg(words[0]), dr, "/")
            elif words[1] =="*":
                calculate0(find_reg(words[0]), dr, "*")


if_variable_declarations("a += 8 ;")
print(register_file)
for s in assembly:
    print  s