
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
> Et trunk link kan transportere en frame mellem flere VLAN's over en enkelt fysisk forbindelse.
> Dvs. at <mark style="background: #FFB86CA6;">VLAN(10)</mark> og <mark style="background: #BBFABBA6;">VLAN(20)</mark> begge kan transportere data over 1 fysisk forbindelse

### How does a Trunk link work?

Et trunk link holder styr på hvilket VLAN som en frame der sendes hører til. 
Dette sker ved at den enhed der sender framen laver en speciel header, kaldet *"tag"*, som indeholder VLAN ID der fortæller hvilket VLAN framen hører til.


> [!note] Trunking protocol
> IEEE 802.1Q er standard protokollen for trunking og er typisk den eneste der er supporteret til det.
> Der er 4096 mulige VLAN numre der kan stå i VLAN ID
> 
> 
> > [!NOTE] VLAN Tagging
> > VLAN Tagging er processen hvorpå en frame får indsat et tag der inkludere VLAN ID. 
> >
> >VLAN Tagging er **KUN** en del af trunking! 


### Switch Interface Modes

![[Switch Interface]]

Da et LAN kan have tusinder af switch interfaces (switch PORT's) har CISCO lavet en protokol kaldet **Dynamic Trunking Protocol (*DTP*)**. Den hjælper switches med at finde ud af hvilken <mark style="background: #FFB8EBA6;">operational mode</mark> de skal være i. 

#### DTP
Hver PORT er sat til at være 1 af 4 modes. 
1. Access
2. Trunk
3. Dynamic auto
	Venter passivt på at den anden ende siger "Let's form a trunk"
4. Dynamic desirable
	Prøver aktivt at blive en trunk PORT
5. nonegotiate
	Slår DTP fra og interfacet skal konfigureres manuelt

Det fungere sådan at når et kabel bliver sat mellem 2 switches, **DTP sker <mark style="background: #FF5582A6;">KUN</mark> mellem switches**, så sender switch(A) en besked til switch(B) der fortæller at den er blevet sat til <mark style="background: #BBFABBA6;">Dynamic Desirable.</mark>Hvis porten som kablet er sat i på switch(B) er kompatibel, dvs. at den er sat til <mark style="background: #FFF3A3A6;">Dynamic Auto,</mark> så sætter de 2 switch de porte til at være trunk porte. 


> [!note] CISCO switches
> PORT's on CISCO switches are by default set to Dynamic Auto and are therefore operational and ready to receive what the other end says


![[Pasted image 20261102105332.png]]


