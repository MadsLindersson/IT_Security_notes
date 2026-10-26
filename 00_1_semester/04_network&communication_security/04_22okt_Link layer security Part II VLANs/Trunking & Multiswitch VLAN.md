
> [!question] Short explanation 
> Hvordan kan vi arbejde med VLAN's over flere switches? Dette svarer trunking på

### Multiswitch Broadcast Domains
Hvis vi sætter 2 default switches <mark style="background: #FFB8EBA6;">(VLAN(1) på alle porte)</mark> sammen, så vil alt BUM traffik ikke bare blive sendt til alle portene på den switch som trafikken ramte, men også videre til den anden switch porte. 
Hvis der er mange switches der alle sidder sammen som er default <mark style="background: #FFB8EBA6;">(VLAN(1) på alle porte)</mark>, kan dette overloade netværket med bum traffik, hvilket er endnu en god grund til at bruge VLAN's

### VLAN on multiple switches

> [!warning] Ikke skalerbart da det kræver fysiske kabler mellem switches - men virker!
> Vi kan sætte VLAN op samtidig med at brugt multiswitches. 
> Dette gøres ved at sætte switches sammen på porte som er sat til samme VLAN.
> 
> > [!warning] 
> > Der skal være en forbindelse (kabel) mellem switches for hvert VLAN
> 
> F.eks. hvis vi har <mark style="background: #FFB86CA6;">VLAN(10)</mark> og <mark style="background: #BBFABBA6;">VLAN(20)</mark> som skal fungere over 2 switches. Så skal vi have en kablet forbindelse sat i en port på begge switches, en som er <mark style="background: #FFB86CA6;">VLAN(10)</mark> og en som er <mark style="background: #BBFABBA6;">VLAN(20)</mark>.   
> 
> ![[Pasted image 20261026111437.png]]

### What is a Trunk link? / VLAN Trunking

> [!info] Trunk link
> Et trunk link kan transportere mellem flere VLAN's over en enkelt fysisk forbindelse.
> Dvs. at <mark style="background: #FFB86CA6;">VLAN(10)</mark> og <mark style="background: #BBFABBA6;">VLAN(20)</mark> begge kan transportere data over 1 fysisk forbindelse

### How does a Trunk link work?

