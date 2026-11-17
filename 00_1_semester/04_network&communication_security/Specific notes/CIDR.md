CIDR er en metode for at inddele IP-adresser i mindre grupper. En CIDR defineres som en IP-adresse efterfulgt af et /Num:
192.168.64.131/24

Tallet efter skårstregen kaldes for et prefix length og er det der definere hvor mange bits der bruges til at definere netværks-delen af IP-adressen. 
- Jo højere tallet er, jo færre IP-adresser.
- Jo lavere tallet er, jo flere IP-adresser.


> [!info] IP-adresse bits
> En IP-adresse er 32 bits lang. Altså 8 bits for hvert tal.

Når man f.eks. ser /24, betyder det at de første 24 bits i IP-adressen bruges til at definere netværket og de sidste 8 definere værten, altså en enhed på netværket. 
<mark style="background: #FFF3A3A6;">192.168.64.131/24</mark>
I dette eksempel:
Netværket = 192.168.64.
Enheden = 131
CIDR = /24

<mark style="background: #ABF7F7A6;">192.168.64.131/16</mark>
I dette eksempel:
Netværket = 192.168.
Enheden = 64.131
CIDR = 16

|CIDR-notation|Præfikslængde|Antal bits til værtsdelen|Antal adresser|Antal ledige adresser|
|---|---|---|---|---|
|`/32`|32|0|1|1 (bruges til enkeltstående enheder)|
|`/30`|30|2|4|2|
|`/28`|28|4|16|14|
|`/24`|24|8|256|254|
|`/16`|16|16|65.536|65.534|
|`/8`|8|24|16.777.216|16.777.214|
