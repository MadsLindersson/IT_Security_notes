Datalink layer is where we have routers, switches and wifi access. It handles sending datagrams from on node to another physical adjacent node via links. It only communicates between one link at a time such as a computer and a switch, these 2 decide the protocols used and the next link from the switch to the router might use other protocols. 

Datalink layers encapsulates datagrams into frames, adding a header. 

It uses MAC addresses to identify source and destination, which is an engraved address every unit has that belongs only to that unit. 

| Protocol |                             | Info                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| -------- | --------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Ethernet | IEEE 802.3                  | ![[Ethernet_header.png]]<br><br>*Preamble*: 7 bit pattern of alternating 1's and 0's. It's for indicating starting of a frame and synchronization. (Start of frame delimiter - 1 byte field that tells that the frame starts now)<br>*Dest. address*: MAC address of destined<br>*Source address*: MAC address of the source<br>*Type*: This indicates what protocol is used in the upper layer (usually IP)<br>*Data (payload)*: encapsulated data with headers from other layers<br>*CRC*: Cyclic Redundancy Check - a type of checksum that is more safe than checksum on other layers |
| WiFi     | 802.11                      | ![[WiFi_802.11_header.png]]<br><br>*frame control*: Type of frame<br>*duration*: The period of time in which the medium is occupied<br>*address 1*: The receivers address<br>*address 2*: The transmitters address<br>*address 3*: The destination address<br>*seq control*: Sequence number and fragment number, used to filter out dublicates<br>*address 4*: Used when one AP is forwarding a frame to another AP over a wireless link<br>*payload*: The data<br>*CRC*: Cyclic Redundancy Check - a type of checksum that is more safe than checksum on other layers                   |
| ARP      | Address Resolution protocol | Used to match IP-address to MAC-address if the MAC-address has not been cached. <br><br>TTL (Time To Live): Time after which the address mapping is deleted from cache. Usually 20 minutes.                                                                                                                                                                                                                                                                                                                                                                                               |
|          |                             |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |

#### CSMA
Carrier Sense Multiple Access - Listen before transmit
A protocol used to verify other traffic before transmitting. It listens for another transmission in progress, and if there is one, it waits for that transmission to be over before transmitting.
![[CSMA.png|390]]
#### CSMA/CD
CD is an addon to CSMA that makes it so if a collision is detected, it drops the transmission and sends a jam signal. It then waits a random time interval before trying to transmit again.
![[CSMA_CD.png|535]]

#### RTS / CTS
*RTS*: Request To Send
*CTS*: Clear To Send

Allows the receiver and the transmitter to let each other know of their state. 
A transmitter sends a RTS to the receiver and if the receiver is not busy, it sends back a CTS to let the transmitter know that it can transmit data. 