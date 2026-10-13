Task 1:

![[Pasted image 20261007094253.png|494]]

1. 192.168.64.130
2. 192.168.64.2 
3. Type A - returner en IPv4 addressee
	1. Har en additional record type OPT
4. 4 addresser
	1. 3.174.18.87
	2. 3.174.18.13
	3. 3.174.18.119
	4. 3.174.18.27

![[Pasted image 20261007100335.png|534]]

1. Source er Kali IP - 192.168.64.129
2. Dest. IP er min ubuntu desktop - 192.168.64.130
3. ![[Pasted image 20261007111554.png]]
4. ![[Pasted image 20261007111605.png]]
5. MAC addresses are:
	1. Src: 00:0c:29:8a:74:52
	2. Dest. 00:0c:29:8a:0a:00
		 ![[Pasted image 20261007111852.png]]
6. Kan ses på hvilken Type i ICMP protokollen det er, *8* for request og *0* for reply
	1. ![[Pasted image 20261007112133.png]]
	2. ![[Pasted image 20261007112143.png]]

![[Pasted image 20261007112935.png|541]]

![[Pasted image 20261007114006.png]]
![[Pasted image 20261007114036.png]]

1. Client IP is my Kali - 192.168.64.130
2. Server IP is my ubuntu - 192.168.64.129

#### Task 4
![[Pasted image 20261013102728.png|499]]

![[Pasted image 20261013104145.png]]

![[Pasted image 20261013104210.png]]

![[Pasted image 20261013104235.png]]

1. .130
2. .129
3. 54732
4. 4444
5. ![[Pasted image 20261013104344.png]]

#### Task 5

![[Pasted image 20261013104457.png|439]]

![[Pasted image 20261013104803.png]]

1. 192.168.64.2
2. ![[Pasted image 20261013104836.png]]
3. it's an A record. (an AAAA record with the ipv6 address was also sent)
4. 80
5. ![[Pasted image 20261013105154.png]]
6. There is nothing exciting in the http request, but in the http response i can basically read all of the html.