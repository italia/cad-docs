Conversione in formato reStructuredText
=======================================

Ottenuti i testi delle versioni del CAD, è possibile eseguire una prima conversione in `formato reStructuredText (RST) <http://docutils.sourceforge.net/rst.html>`_. Questo è il formato utilizzato dal tool `Sphinx <http://www.sphinx-doc.org/>`_ per produrre la documentazione.

Lo script :code:`normattiva2rst.py` è un programma in Python che accetta un file di testo in input e restituisce un file convertito in formato RST. La sintassi per l'uso dello script è:

.. code-block:: bash
   
   python3 normattiva2rst.py source-file > output.rst

Le funzioni principali dello script sono:

1. Correggere la grafia delle parole accentate, che nei testi di Normattiva appaiono sempre con l'apostrofo.

2. Rimuovere le doppie parentesi *(( ... ))*, che in Normattiva denotano una eliminazione di testo dalla legge.

3. Riconoscere *Capi*, *Sezioni* e *Articoli* e creare le decorazioni per i titoli, secondo una precisa gerarchia. A Capi e Sezioni sono assegnati rispettivamente titoli di primo e secondo livello, mentre gli Articoli vengono contrassegnati in grassetto. Agli articoli non viene assegnata una decorazione per il titolo per evitare problemi nella gerarchia: la sintassi RST non permette a un titolo di terzo livello (un Articolo) di seguire un titolo di primo livello (un Capo), come invece avviene all'interno del CAD. 

4. Indentare i commi e i paragrafi in maniera consistente con la sintassi RST.

Il processo di conversione delle varie versioni del CAD è stato automatizzato con uno script in Bash, :code:`bulk-text2rst.sh`, che applica lo script :code:`normattiva2rst.py` a tutti i testi contenuti nella cartella *input*. I file risultanti vengono salvati nella cartella *rst* in `questo repo <https://github.com/italia/cad-docs/tree/master/conversione-cad>`_.
