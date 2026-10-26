[[https://www.networkacademy.io/ccna/ethernet/vlan-concept]]

# LAN switches and BUM traffic

 
> [!info] BUM traffic - Broadcast, Unknown unicast, Multicast
> Når en LAN switch modtager en fram der tilhører en af typerne fra BUM, sendes denne frame ud til alle porte på nær den port som den kommer fra


> [!info] Broadcast domain
> LAN = Broadcast Domain = Subnet
> 
> Et broadcast domain inkludere alle tilknyttede enheder som modtager BUM traffik fra hinanden. Dvs. når en enhed sender en frame som er af en af typerne fra BUM, så modtager alle de andre enheder på samme broadcast domain en kopi af denne frame.

### Problemet uden VLAN's
Hvis en virksomhed gerne vil opdele finans og HR men de sidder på samme broadcast domain (LAN) vil de stadig modtage BUM traffik fra hinanden som giver sikkerheds og privacy problemer. Derfor vil vi gerne have opdelt dem i forskellige broadcast domains. 
Uden VLAN's kan dette gøres ved at opsætte en switch til hvert gruppe af brugere. Dette er ikke så smart, hvad hvis en virksomhed skal bruge 200 opdelte grupper? det er mange switches at skulle sætte op. 
Derfor er det smartere at opdele det logisk ved brug af VLAN's

### Hvad er VLAN's?
Et VLAN er et *Virtuel LAN*. Det er en måde at opdele et LAN logisk, så 1 switch kan fungere som flere broadcast domains (LAN's). Dette opsættes på en port-til-port metode, dvs. at man opsætter hvilke porte på switchen som f.eks. gælder som <mark style="background: #FFB86CA6;">VLAN(10)</mark> og hvilke porte på switchen som gælder som <mark style="background: #BBFABBA6;">VLAN(20)</mark>. Dette gør at de enheder som sidder på <mark style="background: #FFB86CA6;">VLAN(10)</mark> porte kun kan snakke med andre enheder som sidder på <mark style="background: #FFB86CA6;">VLAN(10)</mark> porte. Det gør også at BUM traffik kun bliver sendt indenfor eget broadcast domain (VLAN) og derfor ikke længere giver en sikkerhed eller privacy problem. 

### Hvordan virker VLAN's

> [!quote] VLAN's
> VLANs are actually a very simple concept (but very powerful at the same time). ==A VLAN is simply a number== between 1 and 4096. **Each switch port is always assigned to a specific VLAN number**. Ports assigned to the same VLAN number are in the same broadcast domain. That's it. That is what VLANs are.

**pr. default er alle porte på en switch sat til <mark style="background: #FFB8EBA6;">VLAN(1)</mark> , så alle enheder på switchen kører på samme broadcast domain (LAN) medmindre andet er blevet sat.**

### Fordele ved VLAN's
1. **Bedre sikkerhed** - Ved at færre enheder får kopier af BUM traffik
2. **Smaller fault domains** - Ved at isolere grupper af enheder i forskellige broadcast domains
3. **Reducere CPU overhead** - Færre BUM frames giver mindre traffik til de enkelte enheder
4. **Forbedre netværk performance**  

