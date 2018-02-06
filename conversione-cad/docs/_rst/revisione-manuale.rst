Revisione manuale
=================

I testi contenuti nella cartella *rst* devono essere corretti manualmente prima di una ulteriore conversione. 

Nel testo di `Normattiva <http://www.normattiva.it>`_, infatti, a volte sono presenti degli errori o delle inconsistenze che impediscono a :code:`normattiva2rst.py` di effettuare la conversione correttamente. 

Per esempio:

* un comma in cui il numero iniziale non è separato dal testo seguente tramite uno spazio ("1.Il testo" invece che "1. Il testo") non viene riconosciuto come comma separato;

* a volte, Normattiva presenta il titolo degli articoli fra parentesi e con carattere minuscolo. Anche in questo caso è necessario intervenire per correggere l'errore; 

* in alcuni casi, le doppie parentesi *((...))* sono accompagnate da spazi extra. Quando queste vengono rimosse, quindi, rimane uno spazio in più che deve essere rimosso.

È possibile che queste correzioni possano essere automatizzate all'interno dello script in futuro, grazie all'inserimento di test più raffinati nel codice. 

Per ottimizzare i tempi ed evitare la propagazione di errori fra le varie versioni, è possibile sfruttare la funzione *diff* di molti editor di testo per correggere solo le parti differenti fra una versione e la successiva. In questo modo, è necessaria una revisione approfondita soltanto della prima versione del CAD. Gli errori eventualmente presenti nelle successive versioni verranno evidenziati dal *diff* e potranno essere corretti. 
