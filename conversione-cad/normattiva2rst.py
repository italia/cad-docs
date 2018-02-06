import re
import sys

# === Helper functions

def removeDash(ln):
    if re.match(r'----', ln):
        return ""
    else:
        return ln


def subsAccent(l):
    '''
    Sostituisce apostrofo con l'accento in parole che finiscono per vocale. 
    Es: liberta' -> libertà
    Po', po', è vengono ripristinati nella versione corretta
    '''
    l = l.replace("a'", "à").replace("e'", "é").replace("i'", "ì")
    l = l.replace("o'", "ò").replace("u'", "ù").replace("E'", "È")
    l = l.replace("pò", "po'").replace("Pò", "Po'").replace(" é ", " è ").replace("e\\\'", "è").replace("cioé", "cioè")
    if l[-2:]==" é":
        l = l[:-1] + "è"
    if l[0:2]=="é ":
        l = "è" + l[1:]
        
    return l


def checkAdd(ln, title, flag):
    if ln=="":
        if title.startswith("Art."):
            title = "**" + title + "**"
        print(title)
        flag = 0
    else:
        ln = ln[0] + ln[1:].lower()
        title = title + " " + ln
    return title, flag


def checkLetter(ln):
    if ln!="":
        for lat in latin:
            if (re.match(r'^[a-z]'+lat+'\) ', ln)): return True
            elif (re.match(r'^[a-z][a-z]'+lat+'\) ', ln)): return True
        else: return False
    else: return False



def checkNumber(ln):
    if ln!="":
        for lat in latin:
            if re.match(r'^[0-9]'+lat+'\. ', ln): return True
        else: return False    
    else: return False


# === Main script

filename = sys.argv[1]

latin = ["",
"-bis",
"-ter",
"-quater",
"-quinquies",
"-sexies",
"-septies",
"-octies",
"-novies",
"-decies",
"-undecies",
"-duodecies"]


with open(filename, 'r') as f:
    text = f.read().split('\n')

ctxt = [line.strip().replace(" "*5, " ").replace(" "*4, " ").replace(" "*3, " ").replace(" "*2, " ") for line in text]

# remove beginning and end of text
startLine = next((l for l in ctxt if l.startswith("Vigente al:")), -1)
if startLine!=-1:
    startInd = ctxt.index(startLine)
    ctxt = ctxt[startInd+1:]

endLine = next((l for l in ctxt if l.startswith("TABELLA DI")), -1)
if endLine==-1:
    endLine = next((l for l in ctxt if l.startswith("Il presente decreto,")), -1)
if endLine!=-1:
    endInd = ctxt.index(endLine)
    ctxt = ctxt[:endInd]


# replace "((...))" with nothing
ctxt = [line.replace("(( ... ))","").replace("((...))","") for line in ctxt]
# replace "((" "))" with nothing
ctxt = [line.replace("(( ","").replace(" ))","").replace("((","").replace("))","") for line in ctxt]
ctxt = [line.replace(" . . .","") for line in ctxt]
# replace line with nothing
ctxt = [removeDash(line) for line in ctxt]

ctxt = [subsAccent(line) for line in ctxt]


new_ctxt = []

for (line, ind) in zip(ctxt, range(len(ctxt))):
    if ((line[:4]=="Capo") | (line[:4]=="SEZI")| (line[:4]=="Sezi") | (line[:4]=="Art.")) & (ctxt[ind-1]!=""):
        new_ctxt.append("")
    new_ctxt.append(line)


isArt = 0
isCapo = 0
isSezi = 0
capoList = []
isLetter = 0
isNumber = 0
isIntro = 1
for line in new_ctxt:
    if line.startswith("Capo"):
        isLetter = 0
        isNumber = 0
        isCapo = 1
        capoTitle = line + "."
    elif (line.startswith("Sezione ")) | (line.startswith("SEZIONE ")):
        isLetter = 0
        isNumber = 0
        isSezi=1
        isCapo = 0
        isArt = 0
        seziTitle = "Sezione" + line[7:] + "."
    elif line.startswith("Art. "):
        isLetter = 0
        isNumber = 0
        isArt=1
        isCapo=0
        isSezi=0
        isIntro=0
        if line[-1]!=".":
            line = line + "."
        artTitle = line
        
    elif isCapo == 1:
        capoTitle, isCapo = checkAdd(line, capoTitle, isCapo)
        if isCapo==0:
            print("="*len(capoTitle))
            print("")

    elif isSezi == 1:
        seziTitle, isSezi = checkAdd(line, seziTitle, isSezi)     
        if isSezi==0:
            print("-"*len(seziTitle))
            print("")
            
    elif isArt == 1:
        artTitle, isArt = checkAdd(line, artTitle, isArt)
        if isArt==0:
#             print("^"*len(artTitle))
            print("")
    
    else:
        if isIntro==1:
            if line!="":
                if line[-1]==";":
                    print(line)
                    print("")
                    continue
        
        indent = ""
        if checkNumber(line):
            print("")
            isNumber=1
            isLetter=0
            pos = line.find(".")
            line = line[:pos] + "\\" + line[pos:]
#             indent=" "*(14-pos-2)
            indent = ""
        elif checkLetter(line):
            print("")
            isNumber=0
            isLetter=1
            pos = line.find(")")
            line = line[:pos] + "\\" + line[pos:]
#             indent=" "*(17-pos-2)
            indent = " "*3
        elif isNumber==1:
#             indent=" "*14
            indent=""
        elif isLetter==1:
#             indent=" "*17
            indent = " "*3
       
        print(indent + line)

