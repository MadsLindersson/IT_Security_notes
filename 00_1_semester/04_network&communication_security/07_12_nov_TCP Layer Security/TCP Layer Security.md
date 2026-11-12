# Transport layer
## TCP
- Connection oriented
- reliable
- ordered delivery
- keeps track of connections


> [!info] TCP
> TCP header er 32 bits "bred"
> TCP er reliable ved brug af sequence og acknowledgement numrer. 
> 
> **Flow control** - prevents overwhelming the receiving host.
> 
> **Syn cookies:** en TCP sikkerhedsmekanisme der sikrer sig mod SYN flood attacks. Det er hvor en angriber sender mange TCP SYN og der bliver så svarer med en SYNACK og en "session" holdes igang i 60 sek. Men angriberen sender ikke den sidste ACK tilbage men bliver ved med at sende SYN. 
> Det fungere på den måde at der oprettes en cookie når der er en der starter en forbindelse med en SYN, der sendes en SYNACK med et sekvens nummer og hvis den der startede forbindelsen sender en ACK tilbage med en ACK med sekvensnummer +1 starter forbindelsen. <mark style="background: #FF5582A6;">LÆS OP</mark>
> 
> **Multiplexing:** 1 ip har mange services. <mark style="background: #FF5582A6;">LÆS OP</mark>
> 
> 

## UDP
- connectionsless
- no handshake
- no delivery guarentee
- lower overhead

> [!warning] Portnumre
> Det er godt at vide portnumre på de "store" protokoller som SSH/HTTP/HTTPS/FTP/DNS
> 
> Man risikere at arbejde med forensics eller lign. hvor man er nød til at reagere hurtigt og derfor godt at vide defaultportene.

## Reconnaissance / scanning
- NMAP
En angriber tjekker typisk først:
- Which hosts are reachable
- Which TCP/UDP ports are open
- Which services appear to be running
- Which systems are worth investigating further

Man kan se om der er firewall eller ej ved at tjekke de svar eller manglende svar der kommer tilbage.

### Extended ACL
Her kan vi administrere yderligere, som f.eks. at allow eller deny protokoller. 

> [!warning] ACL
> ACL kan ikke tracke connection state


> [!info] Least priviledge
> Least priviledge er lige så vigtigt på netværket som på OS. Det er vigtigt at der ikke er muligheder for at gøre noget der ikke er behov for. 


