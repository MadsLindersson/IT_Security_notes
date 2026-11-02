
> [!info] Native VLAN's are set on trunk PORTS
> Når et VLAN skal sættes op, sætter vi trunk PORTE til at have et native VLAN. Det er altså ikke en switch der har et native VLAN men en trunk PORT!

Grunden til vi sætter native VLAN's op er for at fortælle hvad en trunk PORT skal gøre ved en untagged frame. Altså en frame der ikke har fået sat et tag af en access PORT. 

> [!warning] IMPORTANT
> Native VLAN number has to be the same on each trunk PORT, if not you get a native VLAN mismatch that can lead to errors and security risks!

Man kan opsætte hvilke VLAN's der der kan sende traffik over et trunk link, dette kan give yderlige sikkerhed da et trunk link som default sender alt traffik. Man kan derfor f.eks. sætte en trunk PORT til kun at lade VLAN's 10, 20 og 30 ind og på den anden side, altså den anden trunk PORT, kun lade 20 og 40. Dette gør at det kun er VLAN(20) der er tilladt at sende over trunk linket.