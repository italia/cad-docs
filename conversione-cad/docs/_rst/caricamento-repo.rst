Caricamento delle versioni nel repo locale
==========================================

Prima di caricare la successione delle versioni del CAD, è necessario creare un repo contenente i file di base per la compilazione dei documenti con Sphinx. La struttura è quella della cartella *repo-base* contenuta in `questo repo <https://github.com/italia/cad-docs/tree/master/conversione-cad>`_. 
Una volta salvati i file ed effettuato un commit, è possibile cominciare.

Il caricamento successivo delle varie versioni del CAD può essere nuovamente automatizzato con uno script Bash. 

La struttura dello script è la seguente:

.. code-block:: bash

   #!bin/bash
   
   for NAME in $( ls output); do
   cd percorso-assoluto-a/repo-base
   cp -R percorso-assoluto-a/output/"$NAME"/* .
   git add *
   git commit -m $NAME
   git tag $NAME
   done 

Per ciascuna cartella contenuta nella cartella *output*, lo script si assicura di operare all'interno del repo, poi copia tutti i file relativi a una versione nel repo. Infine, vengono effettuate le classiche operazioni di Git: *add*, *commit* e *tag*. 
