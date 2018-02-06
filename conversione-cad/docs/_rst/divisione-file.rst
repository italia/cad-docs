Divisione del CAD nei singoli file
==================================

In questa fase, i testi contenuti nella cartella *rst* vengono sottoposti a un ulteriore trattamento tramite lo script :code:`splitRST-softwrap.py`. Per ciascuna versione, lo script esegue le seguenti operazioni:

1. Creare una cartella con le relative sottocartelle in cui salvare i file.

2. Leggere la struttura del testo, individuando Capi, Sezioni e Articoli e salvandoli in array differenti.

3. Rimuovere gli "a capo" all'interno di ciascun Articolo, unendo righe successive tramite spazio.

4. Per ciascun Articolo individuato, creare un file con un nome che dipende dal Capo ed eventualmente dalla Sezione in cui si trova.

5. Creare il file *index.rst*, includendo il titolo del documento e i link a tutti i Capi.

6. Per ciascun Capo, creare un file con tutti i link alle Sezioni o direttamente agli Articoli contenuti.

7. Per ciascuna Sezione, creare un file con tutti i link agli Articoli contenuti.

Quando lo script termina l'esecuzione, ciascuna cartella all'interno di *output* contiene i file nella versione corretta per creare la documentazione in `Read the Docs <https://readthedocs.org>`_. 
