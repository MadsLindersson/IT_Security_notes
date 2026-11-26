En stateless firewall operere op transport laget. I stedet for at monitorere en netværksforbindelse, monitorere den packet-by-packet. Altså bliver alle pakker monitoreret.

Den tillader eller blokere en pakke baseret på pakkens "packet header" f.eks.
- Source IP
- Dest. IP
- Port numre
- Protokoller
- evt. andet
Den er hurtigt og billig at bruge men den har også svaghedder.
En stateless firewall kan ikke se ind i en pakkes data, kun i pakkens header, dvs. den kan ikke beskytte netværket mod ondsindet malware som ligger i en ellers godkendt pakke. 