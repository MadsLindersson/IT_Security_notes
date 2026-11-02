En switch interface er det samme som en switch PORT. 
Der findes 2 slags:
1. Access interface (Access PORT)
	En access PORT er her en enhed sættes til, der er kun 1 der kan kommunikere med en accessport af gangen (Det er et fysisk ethernet kabel der sættes i porten). En access PORT er sat til at være et specifikt VLAN, hvis ikke er det gældene som native VLAN
2. Trunk interface (Trunk PORT)
	En trunk PORT er port sat til at sende frames fra en switch til en anden switch eller en router. En trunk PORT er ikke sat til at være en del af et VLAN men kan sende frames tilhørende alle VLAN's samtidig.

