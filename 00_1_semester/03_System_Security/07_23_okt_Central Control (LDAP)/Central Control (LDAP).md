**why central control**
- Avoid inconsistent management
- avoid randomness
- visibiility and managebility

**Central directory** 
- Information about all users and resources in one place
Alle maskiner og servere spørger CD for at se rettigheder

**Eksempler**
- OpenLDAP
- Active Directory
- FreeIPA
- Cloud identity

**directory tree names**
- dc
	- domain component
		- whole address of a place on the tree
- ou
	- organizational unit
		- Container / folder
- cn
	- common name
		- name of a thing
- uid
	- User ID
		- Sammensat af dc, ou og cn
- gid
	- Group ID

>[!warning] Ved at have central control giver det også en risiko i forbindelse med at alt login data nu ligger et sted samlet

**least priviledge**

- Directory admin
	- *break-glass account* - full control 
- User admin
	- CRUD af users og brugere - har ikke rettigheder på systemet
- Machines
	- read only service accounts (sssd)
- Ordinary users
	- Change their own password and red their own entry
- anonymous
	- Sees nothing - skal kun kunne prøve at logge in


**Protects the crown jewels**
- TLS
	- encrypt traffic
- ACL
	- who may try what? priviledge seperation
- x2
	- replicate: no single point of failure
- LOG
	- who queried what?
- BAK
	- Back up and test and restore

[[Kerberos]]

