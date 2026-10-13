#### Part 1

##### Task 1
![[Pasted image 20261001112252.png|227]]

![[Pasted image 20261001113331.png]] = Find only unicast packets
![[Pasted image 20261001113515.png]]

![[Pasted image 20261001113647.png]]

**Packet number:** 15 
**Protocol:** TCP
**Source IP address:** 192.168.64.4
**Destination IP Address:** 172.66.147.243
**Source MAC address:** 52:55:c0:a8:40:01
**Destination MAC address:** 08:00:27:33:8c:93

1. Det er 1 til 1 kommunikation - det ses under ethernet II som en "individual address" (unicast)
2. source og destination address

##### Task 2
![[Pasted image 20261001115226.png|224]]

![[Pasted image 20261001120039.png]]

**Packet number:** 291
**Protocol:** ICMP
**Source IP address:** 192.168.64.4
**Destination IP Address:** 192.168.64.255
**Source MAC address:** ff:ff:ff:ff:ff:ff
**Destination MAC address:** 08:00:27:33:8c:93

3. Dest adressen slutter på *.255* hvilket er broadcast ip'en
4. No response

##### Task 3
![[Pasted image 20261001120438.png|233]]
![[Pasted image 20261001120446.png|360]]

![[Pasted image 20261001151714.png]]

**Packet number:** 303
**Protocol:** UDP
**Source IP address:** 192.168.64.4
**Destination IP Address:** 239.10.10.10
**Source MAC address:** ![[Pasted image 20261001151840.png]]
**Destination MAC address:** ![[Pasted image 20261001151828.png]]
**Payload/message:** ![[Pasted image 20261001152020.png]]

2. UDP port 5000 
3. The dest IP differs from uni- and broadcast by being within the multicast range of 224.0.0.0 - 239.255.255.255
4. The broadcast MAC address is a default ff:ff:ff:ff:ff:ff whereas the multicast is an actual MAC address of a unit

##### Task 4

| Type      | Dest. IP       | Dest. MAC          | Intended receiver  |
| --------- | -------------- | ------------------ | ------------------ |
| Unicast   | 172.66.147.243 | 08:00:27:33:8c:93  | 172.66.147.243     |
| Broadcast | 192.168.64.4   | ff:ff:ff:ff:ff:ff  | ff:ff:ff:ff:ff:ff  |
| Multicast | 239.10.10.10   | 01:00:5e:0a:0a:0a: | 01:00:5e:0a:0a:0a: |
