
> [!info] Quick Definition
> A default gateway is the network node, usually a router, that devices use to access other networks when no other routes are specified. It acts as the front door to the rest of the connected networks to let traffic in and out of your network. This applies to internet access, or access to other networks within an organization. It is a critical piece of the networking puzzle.
> 
> [Source](https://www.cbtnuggets.com/blog/technology/networking/what-is-default-gateway)

Et default gateway, også bare kaldet gateway, kan forklares som døren mellem et netværk og internettet. Gateway'en er den PORT som forbinder routeren og switchen, den får også en IP adresse som er den adresse enhederne på netværket bruger, når de skal sende til en adresse der ikke er på deres lokale netværk. 

Det fungere på præcis samme måde selvom man ikke bruger et større setup med switches og routere. Den boks man har derhjemme er typisk en all-in-one boks der har et access point, en switch og en router. Dvs. at i stedet for at have en switch og en router der fysisk sidder sammen med et kabel, er det bare indbygget i boksen men fungere på samme måde. Så når man prøver at sende noget over nettet via wi-fi rammer det først acces pointet, som sender det til switchen der kan se det ikke er en lokal IP adresse der skal sendes til, den sender det så til routeren som sender det ud over nettet.