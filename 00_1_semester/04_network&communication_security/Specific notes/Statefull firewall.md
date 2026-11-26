Statefull firewall monitorere selve netværksforbindelse samt "packet header" og det data der er i pakken. Den monitorere altså konteksten for pakken, og ikke kun headeren som i en stateless firewall. 
Den monitorere opførslen af pakkens data og netværksforbindelse og kan ud fra det se mønstre og evt. blokere eller varsle ved pakker der opføre sig mærkeligt eller anerledes. 
Det giver mere sikkerhed end en stateless firewall, men den er samtidig også langsommere og kræver mere for netværket, da pakkerne skal analyseres meget mere i dybden. 

En stor fordel ved statefull firewalls er at de kan logge angreb og derefter være bedre til at stoppe angrebet en anden gang, uden at behøve at opdatere. 

En svaghed er at den er nødsaget til at være opdateret med det nyeste software for at undgå at hackere kan udnytte sårbarhedder.  

En statefull firewall lær generelt løbende og bliver bedre til at beskytte mod angreb.

![[New, Established & Related]]