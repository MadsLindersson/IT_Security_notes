
##### Link Layer

##### ARP
- *ARP Request* - "Who has X? Tell Y"
	- Request broadcast - svar unicast
- *ARP Prope* - "Is anyone using this IP?"
	- For at tjekke om der er en anden host der bruger denne IP adresse
- *ARP annnouncement* - "This IP is mine"
	- Bruges når en host advertiser sin egen IP-to-MAC mapping
- *ARP / Neigbour table* 
	- når en host lær en IP-to-MAC mapping gemmes det i den neighbour table
		- REACHABLE
		- STALE
		- FAILED
		- PERMANENT
##### DHCP
- Uses UDP port 53
- Tildeler IP adresser

**DORA**
- Discover
- Offer
- Request
- Acknowledge

**Attacks**
- Rogue DHCP Server
	- Attacker-controlled default gateway
	- Attacker-controlled DNS server
	- Incorrect subnet mask
	- Invalid routes
	- Very short lease duration

**Detection**
- Multiple DHCP offers for one discover
- Unexpected DHCP server addresses
- Incorrect gateway or DNS config
- DHCP responses originating from user-facing ports
##### Ethernet switching
##### Switch security
**Possible problems:**
- *MAC address spoofing* - en enhed spoofer sin MAC til at ligne en andens MAC
- *MAC table overflow*
- *MAC flapping*
- *Unauthorized devices*
- *Broadcast storms*
- *Rogue switches*
- *Incorrect trunk config*

**Potential consequences:**
- Traffic flooding
- Connectivity instability
- Unauthorized network access
- Increased traffic visibility
- DOS