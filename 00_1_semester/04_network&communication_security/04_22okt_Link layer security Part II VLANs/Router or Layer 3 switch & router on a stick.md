For at to VLAN's kan kommunikere er vi nød til at have noget der kan "route" data. Typisk vil enheder på et VLAN også tilhøre det samme subnet, derfor er det også nødvendigt at enheden der skal route data kan udføre IP routing. Det er vigtigt at enheden har en IP adresse i hvert netværk så klienterne kan bruge det som deres [[Default gateway]].

Her kan en router eller en layer 3 switch bruges. 
- Router
	- Sættes med fysisk kabel til switchen, 1 port pr. VLAN. 
		- <mark style="background: #FF5582A6;">Dette er ikke det smartest da det ikke scaler til mange VLAN's</mark>
- Layer 3 switch
	- En layer 3 switch kan bruges til at sætte router funktioner op

# Router on a stick


