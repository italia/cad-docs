import re
import numpy as np
import os

for fn in os.listdir("rst"):
    
    print(str(fn))
    
    filename = "rst/" + fn

    outputFolder = "output/"
    
    with open(filename, "r") as f:
        text = f.read().splitlines()

    folderName = "v" + filename.replace(".rst","").split("_")[2]
    
    if (not os.path.exists(outputFolder)):
        os.mkdir(outputFolder)

    if (not os.path.exists(outputFolder + folderName + "/")):
        os.mkdir(outputFolder + folderName)
        os.mkdir(outputFolder + folderName + "/" + "_rst")

    outputFolder = outputFolder + folderName + "/"

    roman = {"I":1, "II":2, "III":3, "IV":4, "V":5, "VI":6, "VII":7, "VIII":8, "IX":9, "X":10}

    def typeOf(par):
        if par.startswith("Capo "):
            return 0
        if par.startswith("Sezione "):
            return 1
        if par.startswith("**Art. "):
            return 2
        else:
            return -1

    capi = []
    sezi = []
    arti = []
    for par in text:
        if (typeOf(par) == 0):
            capi.append(par)
        if (typeOf(par) == 1):
            sezi.append(par)
        if (typeOf(par) == 2):
            arti.append(par)

    def splitPar(par):
        if par.startswith("**Art."):
            line = par.split(". ")[1]
            numb=str(line.replace(" ", "-"))
        else:
            line = par.split(". ")[0]
            numb = str(roman[line.split(" ")[1]])
        return numb

    cap=""
    sez=""
    art=""
    structure = []
    newText = []
    for par in text:
        if typeOf(par)==0:
            sez=""
            art=""
            cap="capo"+splitPar(par)
        if typeOf(par)==1:
            sez="sezione"+splitPar(par)
        if typeOf(par)==2:
            if sez=="":
                sez="sezione"+str(0)
            if ("Non ancora esistente o vigente" in par):
                continue
            art="art"+splitPar(par)        
            struc = cap+"_"+sez+"_"+art
            structure.append(struc)
            newText.append("--NEWART")
            newText.append(".. _" + str(art) + ":\n")
            par = par.replace("*","")
            par = par + "\n" + ("^"*len(par)) + "\n"
        newText.append(par)

    arts = ("\n".join(newText)).split("--NEWART")

    structure.insert(0,"intro")

    def checkCapoOrSez(l):
        if (l.startswith("Capo ")) | (l.startswith("Sezione ")) | (l.startswith("==")) | (l.startswith("---")):
            return False
        return True

    # === This section implements soft-wrap in the text ==========
    artsClean = []
    for art in arts:
        theArt = []
        theLines = art.split("\n\n")
        for line in theLines:
            if (line.startswith("Art. ")) | (line.startswith("Sezione ")) | (line.startswith("Capo ")):
                if line.startswith("Art. 62-bis"):
                    line = line + "\n\n"
                theArt.append(line)
            else:
                if line.startswith("\n"):
                    line = line[1:]
                theArt.append(line.replace("\n         "," ").replace("\n      "," ").replace("\n   "," ").replace("\n"," "))
        artsClean.append("\n\n".join(theArt))

    # === END OF SOFT-WRAP ========================================
    
    ## Write article files

    for (article,name) in zip(artsClean,structure):
        lines = article.splitlines()
        toOutput = [line for line in lines if checkCapoOrSez(line)]

        # "Articolo abrogato" come titolo
        for line in toOutput:
            if ("ARTICOLO ABROGATO" in line):
                num = name.split("_")[2].replace("art","").replace(".**","")
                abrogo = line.lower().replace("articolo","Articolo").replace("d.lgs.","D.Lgs.")
                title = "Art. "+str(num)+". "+abrogo
                toOutput = ["",".. _art"+str(num)+":", "", title, "^"*len(title)]

        with open(outputFolder + "_rst/" + str(name.replace("sezione0_","").replace(".**",""))+".rst", "w") as f:
            theText = str("\n".join(toOutput))
            f.write(theText)

    num = name.split("_")[2].replace("art","")

    ## Write index.rst

    indexList = structure[1:]

    theTitle2 = "Decreto Legislativo 7 marzo 2005, n. 82"
    theTitle1 = "Codice dell'amministrazione digitale"
    toOutput = [theTitle1, "#"*len(theTitle1), "", theTitle2, "#"*len(theTitle2), "", ".. toctree::", ""]
    for ii in range(len(capi)):
        toOutput.append("   _rst/capo"+str(ii+1)+".rst")

    with open(outputFolder+"index.rst", "w") as f:
            theText = str("\n".join(toOutput))
            f.write(theText)

    ## Write capo#.rst

    indSplit = [a.split("_") for a in indexList]

    capiList = [a[0] + "_" + a[1] for a in indSplit]
    indexCapi = list(np.sort(list(set(capiList))))

    count = 0
    for capo in capi:
        count+=1
        theTitle = capo
        toOutput = [theTitle, "="*len(theTitle), "", ".. toctree::", ""]

        for line in indexCapi:
            if (line.startswith("capo"+str(count))):
                if (line[-1]!="0"):
                    toOutput.append("   "+line.replace("sezione0_","")+".rst")

        with open(outputFolder+"_rst/"+"capo"+str(count)+".rst", "w") as f:
            theText = str("\n".join(toOutput))
            f.write(theText)

    ## Write capo#-sezione#.rst

    count = 0
    for seziFile in indexCapi:
        toOutput=[]
        if (seziFile[-1]!="0"):
            theTitle = sezi[count]
            toOutput = [theTitle, "-"*len(theTitle), ""]
            count+=1
        if (seziFile.startswith("capo1_sezione1")):
            with open(outputFolder + "_rst/" +"intro.rst",'r') as fin:
                textIntro = fin.read()
                toOutput.append(textIntro)

        toOutput.append("")
        if (seziFile[-1]!="0"): 
            toOutput.append(".. toctree::")
            toOutput.append("")

        for artTitle in indexList:
            if artTitle.startswith(seziFile):
                toOutput.append("   "+artTitle.replace("sezione0_","").replace(".**","")+".rst")

        if (seziFile[-1]=="0"):
            with open(outputFolder+"_rst/"+ seziFile.replace("_sezione0","")+".rst", "a") as f:
                theText = str("\n".join(toOutput))
                f.write(theText)
        else:
            with open(outputFolder+"_rst/"+ seziFile+".rst", "w") as f:
                theText = str("\n".join(toOutput))
                f.write(theText)
                
    os.remove(outputFolder + "_rst/intro.rst")
