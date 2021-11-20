"""
******************************************************************************************

    LICENCE :

    IAs_Code
    Copyright (C) 2018  Sebastien SILVANO
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.

    If not, see <https://www.gnu.org/licenses/>.
"""
import sys
from tkinter import *
from time import sleep

def getKeyPressed(k):
    data.keyPressed = k.char
def getKeyReleased(k):
    data.keyReleased = k.char
def getPos(name):
    for a in range(len(data.var)):
        if data.var[a].split(':')[0] == name:
            return a
    print("Line {0} : NAME ERROR : The variable is undefined.".format(data.line))
    data.end = True
def getType(name):
    for v in data.var:
        if v.split(':')[0] == name:
            return v.split(':')[1]
def getValue(name):
    for v in data.var:
        if v.split(':')[0] == name:
            return v.split(':')[2]
def testType(typ,value):
    if typ == 'int':
        try:
            value = str(int(value))
        except:
            print("Line {0} : TYPE ERROR : The type must be integer.".format(data.line))
            data.end = True
            return False
    elif typ == 'float':
        try:
            value = str(float(value))
        except:
            print("Line {0} : TYPE ERROR : The type must be float.".format(data.line))
            data.end = True
            return False
    return True

def analysis(execution):
    for cmd in range(len(execution)):
        command = execution[cmd]
        if data.debug:
            a = input(command + '\n-->ife='+data.ife + '\n-->case='+data.case + '\n-->part='+str(data.p))
        if command.startswith('IFE'): #"IF Equals"
            try:
                arg1 = command.split(' ')[1] #var name
                arg2 = command.split(' ')[2] #var name
            except:
                print("Line {0} : ARGUMENT ERROR : Not enough arguments.".format(data.line))
                print(command)
                data.end = True
                break
            if getType(arg1) != getType(arg2):
                print("Line {0} : COMPARING ERROR : Can't compare different types.".format(data.line))
                print(command)
                data.end = True
                break
            if getValue(arg1) == getValue(arg2): #INCLUDING LIST COMPARATION !!!
                data.ife = 'true'
            else:
                data.ife = 'false'
            data.case = 'true'
        elif command.startswith('ENE'): #Equals / Not Equals (ife middle delimiter)
            data.case = 'false'
        elif command.startswith('EIE'): #End "If Equals"
            data.ife = 'off'
            data.case = 'off'
        elif data.case == data.ife:
            if command.startswith('DCL'): #DeCLare variable
                try:
                    arg1 = command.split(' ')[1] #var name
                    arg2 = command.split(' ')[2] #type
                except:
                    print("Line {0} : ARGUMENT ERROR : Not enough arguments.".format(data.line))
                    print(command)
                    data.end = True
                    break
                for v in data.var:
                    if v.split(':')[0] == arg1:
                        print("Line {0} : OVERDECLARING ERROR : Variable already declared.".format(data.line))
                        print(command)
                        data.end = True
                        break
                if not arg2 in 'int float string list':
                    print("Line {0} : TYPE ERROR : Undefined type in declaration.".format(data.line))
                    print(command)
                    data.end = True
                    break
                if arg2 == 'list':
                    temp = '{}'
                else:
                    temp = ''
                if not data.end:
                    data.var.append(arg1 + ':' + arg2 + ':' + temp)
            elif command.startswith('DEL'): #DELete variable
                try:
                    arg1 = command.split(' ')[1] #var name
                except:
                    print("Line {0} : ARGUMENT ERROR : Not enough arguments.".format(data.line))
                    print(command)
                    data.end = True
                    break
                temp = getPos(arg1)
                if data.end: #because of the getPos() errors
                    print(command)
                    break
                del data.var[temp]
            elif command.startswith('MDL'): #MoDify var from vaLue
                try:
                    arg1 = command.split(' ')[1] #var name
                    arg2 = command.split(' ')[2] #value
                except:
                    print("Line {0} : ARGUMENT ERROR : Not enough arguments.".format(data.line))
                    print(command)
                    data.end = True
                    break
                temp = getType(arg1)
                if testType(temp,arg2):
                    temp1 = getPos(arg1)
                    if data.end: #because of the getPos() errors
                        print(command)
                        break
                    data.var[temp1] = arg1 + ':' + temp + ':' + arg2
                if data.end: #because of the testType() errors
                    print(command)
                    break
            elif command.startswith('MDR'): #MoDify var from vaR
                try:
                    arg1 = command.split(' ')[1] #var name
                    arg2 = command.split(' ')[2] #var name
                except:
                    print("Line {0} : ARGUMENT ERROR : Not enough arguments.".format(data.line))
                    print(command)
                    data.end = True
                    break
                temp = getValue(arg2)
                temp1 = getType(arg1)
                if testType(temp1,temp):
                    temp2 = getPos(arg1)
                    if data.end: #because of the getPos() errors
                        print(command)
                        break
                    data.var[temp2] = arg1 + ':' + temp1 + ':' + temp
                if data.end: #because of the testType() errors
                    print(command)
                    break
            elif command.startswith('APL'): #APpend to list from vaLue
                try:
                    arg1 = command.split(' ')[1] #var name
                    arg2 = command.split(' ')[2] #value
                except:
                    print("Line {0} : ARGUMENT ERROR : Not enough arguments.".format(data.line))
                    print(command)
                    data.end = True
                    break
                temp = getValue(arg1)
                try:
                    if len(temp) == 2:
                        temp = temp[0:len(temp)-1] + arg2 + '}'
                    else:
                        temp = temp[0:len(temp)-1] + ',' + arg2 + '}'
                except:
                    print("Line {0} : TYPE ERROR : The type of the variable must be list.".format(data.line))
                    print(command)
                    data.end = True
                    break
                temp1 = getPos(arg1)
                if data.end: #because of the getPos() errors
                    print(command)
                    break
                data.var[temp1] = arg1 + ':list:' + temp
            elif command.startswith('APR'): #APpend to list from vaR
                try:
                    arg1 = command.split(' ')[1] #var name
                    arg2 = command.split(' ')[2] #var name
                except:
                    print("Line {0} : ARGUMENT ERROR : Not enough arguments.".format(data.line))
                    print(command)
                    data.end = True
                    break
                temp = getValue(arg1)
                try:
                    if len(temp) == 2:
                        temp = temp[0:len(temp)-1] + getValue(arg2) + '}'
                    else:
                        temp = temp[0:len(temp)-1] + ',' + getValue(arg2) + '}'
                except:
                    print("Line {0} : TYPE ERROR : The type of the variable must be list.".format(data.line))
                    print(command)
                    break
                temp2 = getPos(arg1)
                if data.end: #because of the getPos() errors
                    print(command)
                    break
                data.var[temp2] = arg1 + ':list:' + temp
            elif command.startswith('GLL'): #Get List element from vaLue
                try:
                    arg1 = command.split(' ')[1] #var name
                    arg2 = command.split(' ')[2] #value
                    arg3 = command.split(' ')[3] #var name
                except:
                    print("Line {0} : ARGUMENT ERROR : Not enough arguments.".format(data.line))
                    print(command)
                    data.end = True
                    break
                temp = getValue(arg1)
                if not temp.startswith('{'):
                    print("Line {0} : TYPE ERROR : The type of the variable must be list.".format(data.line))
                    print(command)
                    data.end = True
                    break
                temp = temp[1:len(temp)-1].split(',')
                try:
                    temp = temp[int(arg2)]
                except:
                    print("Line {0} : KEY ERROR : Not enough elements in the list.".format(data.line))
                    print(command)
                    data.end = True
                    break
                temp1 = getType(arg3)
                if temp1 == 'list':
                    print("Line {0} : TYPE ERROR : The type of receiving variable can't be list.".format(data.line))
                    print(command)
                    data.end = True
                    break
                temp2 = getPos(arg3)
                if data.end: #because of the getPos() errors
                    print(command)
                    break
                data.var[temp2] = arg3 + ':' + temp1 + ':' + temp
            elif command.startswith('GLR'): #Get List element from vaRiable
                try:
                    arg1 = command.split(' ')[1] #var name
                    arg2 = command.split(' ')[2] #var name
                    arg3 = command.split(' ')[3] #var name
                except:
                    print("Line {0} : ARGUMENT ERROR : Not enough arguments.".format(data.line))
                    print(command)
                    data.end = True
                    break
                temp = getValue(arg1)
                if not temp.startswith('{'):
                    print("Line {0} : TYPE ERROR : The type of the variable must be list.".format(data.line))
                    print(command)
                    data.end = True
                    break
                temp = temp[1:len(temp)-1].split(',')
                temp1 = getPos(arg2)
                if data.end:
                    print(command)
                    break
                temp1 = getValue(arg2)
                try:
                    temp = temp[int(temp1)]
                except:
                    print("Line {0} : KEY ERROR : The list don't have an element at this place.".format(data.line))
                    print(command)
                    data.end = True
                    break
                temp1 = getType(arg3)
                if temp1 == 'list':
                    print("Line {0} : TYPE ERROR : The type of receiving variable can't be list.".format(data.line))
                    print(command)
                    data.end = True
                    break
                temp2 = getPos(arg3)
                if data.end: #because of the getPos() errors
                    print(command)
                    break
                data.var[temp2] = arg3 + ':' + temp1 + ':' + temp
            elif command.startswith('SHW'): #SHOW the value of a var
                try:
                    arg1 = command.split(' ')[1] #var name
                except:
                    print("Line {0} : ARGUMENT ERROR : Not enough arguments.".format(data.line))
                    print(command)
                    data.end = True
                    break
                temp = getValue(arg1)
                print(temp)
            elif command.startswith('PRT'): #PRinT text
                try:
                    arg1 = command.split(' ')[1] #text
                except:
                    print("Line {0} : ARGUMENT ERROR : Not enough arguments.".format(data.line))
                    print(command)
                    data.end = True
                    break
                try:
                    print(command.split('"')[1])
                except:
                    print("Line {0} : ARGUMENT ERROR : Argument must be text.".format(data.line))
                    print(command)
                    break
            elif command.startswith('SLP'): #SLeeP
                try:
                    sleep(float(command.split(' ')[1])) #value
                except:
                    print("Line {0} : TYPE ERROR : The value must be float.".format(data.line))
                    print(command)
                    data.end = True
                    break
            elif command.startswith('RPT'): #RePeaT the actual loop
                try:
                    arg1 = command.split(' ')[1] #value
                except:
                    print("Line {0} : ARGUMENT ERROR : Not enough arguments.".format(data.line))
                    print(command)
                    data.end = True
                    break
                data.p -= 1
            elif command.startswith('DBG'): #DeBuG
                data.debug = not data.debug
            elif command.startswith('ADD'): #ADD a value to a var
                try:
                    arg1 = command.split(' ')[1] #var name
                    arg2 = command.split(' ')[2] #value
                except:
                    print("Line {0} : ARGUMENT ERROR : Not enough arguments.".format(data.line))
                    print(command)
                    data.end = True
                    break
                try:
                    temp = float(getValue(arg1))+float(arg2)
                    temp1 = getType(arg1)
                    if temp1 == 'int': #An int is just less than a float
                        temp = int(temp)
                    temp2 = getPos(arg1)
                    if data.end: #because of the getPos() errors
                        print(command)
                        break
                    data.var[temp2] = arg1 + ':' + temp1 + ':' + str(temp)
                except:
                    print("Line {0} : TYPE ERROR : All must be floats or integers.".format(data.line))
                    print(command)
                    data.end = True
                    break
            elif command.startswith('FTN'):
                try:
                    arg1 = command.split(' ')[1] #function name
                    arg2 = command.split(' ')[2] #var name
                except:
                    print("Line {0} : ARGUMENT ERROR : Not enough arguments.".format(data.line))
                    print(command)
                    data.end = True
                    break
                ft = ''
                for f in data.ftn:
                    if f[0].split(' ')[1] == arg1:
                        ft = f
                        break
                temp = getPos(arg2)
                if data.end: #because of the getPos() errors
                    print(command)
                    break
                data.var[temp] = data.var[temp].split(':')[0] + ':' + data.var[temp].split(':')[1] + ':' + str(analysis(ft))
            elif command.startswith('RET'):
                try:
                    arg1 = command.split(' ')[1] #var name
                except:
                    print("Line {0} : ARGUMENT ERROR : Not enough arguments.".format(data.line))
                    print(command)
                    data.end = True
                    break
                return arg1
            #==============================FILES=========================================
            elif command.startswith('FIR'): #FIle Read
                try:
                    arg1 = command.split(' ')[1] #file name
                    arg2 = command.split(' ')[2] #var name
                except:
                    print("Line {0} : ARGUMENT ERROR : Not enough arguments.".format(data.line))
                    print(command)
                    data.end = True
                    break
                try:
                    f = open(arg1,'r')
                    temp = getPos(arg2)
                    data.var[temp] = arg2 + ':' + getType(arg2) + ':' + f.read()
                    f.close()
                except:
                    f.close()
                    print("Line {0} : FILE ERROR : File not found.".format(data.line))
                    print(command)
                    data.end = True
                    break
            elif command.startswith('FIW'): #FIle Write
                try:
                    arg1 = command.split(' ')[1] #file name
                    arg2 = command.split(' ')[2] #var name
                except:
                    print("Line {0} : ARGUMENT ERROR : Not enough arguments.".format(data.line))
                    print(command)
                    data.end = True
                    break
                try:
                    f = open(arg1,'w')
                    f.write(getValue(arg2))
                    f.close()
                except:
                    f.close()
                    print("Line {0} : FILE ERROR : File not found.".format(data.line))
                    print(command)
                    data.end = True
                    break
            #=============================GRAPHICS=======================================
            elif command.startswith('SIZ'): #set graphics SIZe
                try:
                    arg1 = command.split(' ')[1] #value
                    arg2 = command.split(' ')[2] #value
                except:
                    print("Line {0} : ARGUMENT ERROR : Not enough arguments.".format(data.line))
                    print(command)
                    data.end = True
                    break
                try:
                    data.maxX = int(arg1)
                    data.maxY = int(arg2)
                except:
                    print("Line {0} : TYPE ERROR : The value of both must be integer.".format(data.line))
                    print(command)
                    data.end = True
                    break
            elif command.startswith('IGR'): #Init GRaphics
                data.win = Tk()
                data.canvas = Canvas(data.win,width=data.maxX,height=data.maxY,bg='white')
                data.canvas.pack()
                data.canvas.bind('<KeyPress>',getKeyPressed)
                data.canvas.bind('<KeyRelease>',getKeyReleased)
                data.canvas.focus_set()
            elif command.startswith('UGR'): #Update GRaphics
                data.keyPressed = ''
                data.keyReleased = ''
                data.canvas.update()
                data.canvas.delete(ALL)
            elif command.startswith('DGR'): #Destroy GRaphics
                data.canvas.destroy()
                data.win.destroy()
            elif command.startswith('GKP'): #Get Keypad Pressures
                try:
                    arg1 = command.split(' ')[1] #var name
                except:
                    print("Line {0} : ARGUMENT ERROR : Not enough arguments.".format(data.line))
                    print(command)
                    data.end = True
                    break
                temp = getPos(arg1)
                if data.end: #because of the getPos() errors
                    print(command)
                    break
                data.var[temp] = data.var[temp].split(':')[0] + ':' + data.var[temp].split(':')[1] + ':' + data.keyPressed
            elif command.startswith('GKR'): #Get Keypad Releases
                try:
                    arg1 = command.split(' ')[1] #var name
                except:
                    print("Line {0} : ARGUMENT ERROR : Not enough arguments.".format(data.line))
                    print(command)
                    data.end = True
                    break
                temp = getPos(arg1)
                if data.end: #because of the getPos() errors
                    print(command)
                    break
                data.var[temp] = data.var[temp].split(':')[0] + ':' + data.var[temp].split(':')[1] + ':' + data.keyReleased
            elif command.startswith('COL'): #set COLor
                try:
                    arg1 = command.split(' ')[1] #color
                    arg2 = command.split(' ')[2] #value
                except:
                    print("Line {0} : ARGUMENT ERROR : Not enough arguments.".format(data.line))
                    print(command)
                    data.end = True
                    break
                try:
                    temp = hex(int(arg2))[2:]
                    if len(temp) < 2:
                        temp = '0' + temp
                    if len(temp) > 2 or int(arg2) < 0:
                        print("Line {0} : ARGUMENT ERROR : Color must be set between 0 and 255.".format(data.line))
                        print(command)
                        data.end = True
                        break
                    if arg1 == 'red':
                        data.color = data.color[0] + temp + data.color[3:7]
                    elif arg1 == 'green':
                        data.color = data.color[:3] + temp + data.color[5:7]
                    elif arg1 == 'blue':
                        data.color = data.color[:5] + temp
                except:
                    print("Line {0} : TYPE ERROR : The value must be integer.".format(data.line))
                    print(command)
                    data.end = True
                    break
            elif command.startswith('RCT'): #create a ReCTangle
                try:
                    temp1 = getValue(command.split(' ')[1]) #var name
                    temp2 = getValue(command.split(' ')[2]) #var name
                    temp3 = getValue(command.split(' ')[3]) #var name
                    temp4 = getValue(command.split(' ')[4]) #var name
                except:
                    print("Line {0} : ARGUMENT ERROR : Not enough arguments.".format(data.line))
                    print(command)
                    data.end = True
                    break
                try:
                    temp1 = int(temp1)
                    temp2 = int(temp2)
                    temp3 = int(temp3)
                    temp4 = int(temp4)
                except:
                    print("Line {0} : TYPE ERROR : All values must be integers.".format(data.line))
                    print(command)
                    data.end = True
                    break
                data.canvas.create_rectangle(temp1,temp2,temp3,temp4,fill=data.color,outline=data.color)
            #===========================================================================
        if not data.lineStop:
            data.line += 1
'''
COMMANDS:

standard :

- LOP       : Create a new loop
- DCL a b   : Declare a variable a of type b (a=variable b=type)
- MDL a b   : Attribute b to the variable a (a=variable b=value)
- MDR a b   : Attribute the value of the variable b into the variable a (a,b=variable)
- DEL a     : Delete the variable a (a=variable)
- APL a b   : Append b to the list a (a=list b=allTypes)
- APR a b   : Append the value of b into the list a (a,b=variable)
- GLL a b c : Get the value of the element number b of the list a and attribute it in the variable c (a,c=variable b=value)
- GLR a b c : Get the value of the element number of the value of b of the list a and attribute it in the variable c (a,c=variable b=value)
- SHW a     : Show the value of the variable a (a=variable)
- SLP a     : Stop the execution for a seconds (a=float)
- RPT a b   : Repeat the actual loop a number of times (a=int)
- PRT a     : Print text in the console (a=text between double quotes)
- DBG       : Switch the debug on/off (shows the execution line by line)
- IFE a b   : Call a "If equals". if a == b, execute the next lines until ENE command. (a,b=variable)
- ENE       : Separate the "Equals" and the "Not Equals" sections
- EIE       : End a "If equals"
- ADD a b   : Add b to a (a,b=float,int)
- FTN a b   : Call the function a and return the result in the variable b (a=function b=variable)
- BFT a     : Declare a function a (a=function)
- RET a     : Set the return value of the current function at the value of the variable a (a=variable)
- EFT       : End a function

files:

- FIR a b : Save the data of the file a in the var b (a=fileName b=variable)
- FIW a b : Load the data of the var b into the file a (a=fileName b=variable)

graphics :

- IGR     : Initialize graphics
- UGR     : Update graphics
- DGR     : Delete graphics
- SIZ     : Set the size of the window (a,b=int)
- COL a b : Set drawing color (a=red,green,blue b=int)
- RCT a b c d : Draw a rectangle with 4 coordonates (a,b,c,d=int)
'''
class IA():
    def __init__(self):
        self.parts = []
        self.var = []
        self.ftn = []
        self.ife = 'off'
        self.case = 'off'
        self.maxX = 100
        self.maxY = 100
        self.color = '#000000'
        self.win = ''
        self.canvas = ''
        self.line = 1
        self.lineStop = False
        self.debug = False
        self.end = False
        self.p = 0
        self.keyPressed = ''
        self.keyReleased = ''
data = IA()

while True:
    script = open(input("Select a file to execute > "),'r')
    code = script.read().split('\n')
    script.close()
    '''
    Organisation of VAR: [name:type:value, name:type:value, name:type:value, ...]
    '''
    #--------------------Code Segmentation-------------------
    row = -1
    ftDetected = False
    for cmd in range(len(code)): #Separate the functions from the principal execution
        if code[cmd].startswith('BFT'):
            ftDetected = True
            data.ftn.append([])
            row += 1
        if code[cmd].startswith('EFT'):
            ftDetected = False
            data.ftn[row].append(code[cmd])
            code[cmd] = ''
        if ftDetected:
            data.ftn[row].append(code[cmd])
            code[cmd] = ''
    row = -1
    for cmd in code:
        if cmd.startswith('LOP'):
            new = True
        try:
            if new:
                new = False
                row += 1
                data.parts.append([''])
            else:
                data.parts[row].append(cmd)
        except:
            print("Line 1 : START ERROR : You don't have writen 'LOP' to begin.")
            sys.exit()
    '''
    print("Parts :")
    for a in data.parts:
        for b in a:
            print("        " + b)
        print("    _")
    print("Functions :")
    for a in data.ftn:
        for b in a:
            print("        " + b)
        print("    _")
    '''
    #------------------------------------------------------------
    del code
    while len(data.parts) > data.p and not data.end:
        analysis(data.parts[data.p])
        data.p += 1
    print("\nEnd of execution.\n")
    data.parts = [] #reset
    data.var = []
    data.ftn = []
    data.ife = 'off'
    data.case = 'off'
    data.maxX = 100
    data.maxY = 100
    data.color = '#000000'
    data.win = ''
    data.canvas = ''
    data.line = 1
    data.lineStop = False
    data.debug = False
    data.end = False
    data.p = 0
    data.keyPressed = ''
    data.keyReleased = ''
