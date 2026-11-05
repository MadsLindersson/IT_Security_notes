**WAN** - wide area network
**LAN** - local area network
**Loopback** - til kommunikation inde i samme computer


> [!info] IP spoofing
> At lave en IP packet med en "hjemmelavet" ip adresse for at ligne en anden end sig selv
> 
> - Hide the real sender
> - Impersonate another host
> - Abuse trust based on source IP
> - Redirect replies toward a victim
> - Support reflection/amplification attacks 



> [!info] ICMP
> - Bruges til host descovery
> - Bruges til network mapping: traceroute
> - Bruges til at troubleshout connectivity
> - Bliver ofte abused til reconnaissance
>   
>   ### Hvorfor restricte ICMP?
>   - enables network discovery
>   - Reveals active hosts
>   - can expose firewall behaviour
>   - may assist lateral movement
>     
>    ## ICMP attacks
>    - ICMP reconnaisance / ping sweep
>    - ICMP flood / ping flood
>    - smurf attacks
>    - ping of death
>    - ICMP redirect attack
> 	   - Sends malicious redirect messages to influence a hosts routing decision
>    - ICMP tunneling
> 	   - F.eks. gemme data i timestamps i ICMP packets - der bruges millisekund pladsen til at sende ASCII
> 	   - Tunneling findes i mange andre protokoller, TCP og DNS osv.
>    -  ICMP destination unreachable abuse
>    - ICMP fragmentation abuse <mark style="background: #FF5582A6;">(uden for scope)</mark>
>
>### Reverse-path filtering - anti-spoofing
>Prevent ip-spoofing by validating the source ip address of incoming packets
>
>### TTL manipulation - Firewall Reconnaissance
>Attackers manipulate IPv4 TTL to probe firewall boundaries
>

> [!info] ACL
>Et sæt af regler der bruges til at permit eller deny netværks traffik
>
>*ACL = Who is allowed to communicate with who?*
>
>- Rules are evaluated TOP ➡️ DOWN
>- FIRST MATCH WINS
>- Specific rules BEFORE generel rules
>- remember the IMPLICIT DENY (applied at the end)


> [!linfo] Firewall
> a firewall controls network traffic according to security rules
> 
> Firewall mindre om ACL men kan mere
> 
> En firewall kan tage beslutninger baseret på information som:
> - Source IP
> - Dest. IP
> - IP protocol
> - TCP/UDP porte
> - Connection state
>   
>Firewall regler er ligesom ACL TOP ➡️ DOWN
>   
>- Network firewall
>- Host firewall
>  
>  #### Default policies
>- Default ALLOW
>- Default DENY



