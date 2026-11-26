New, established og related er tilstande der bruges i en statefull firewall til at beskrive og håndtere forbindelser mellem enheder på et netværk.

# New
Dette er tilstanden en forbindelse typisk får når den første pakke bliver sendt, f.eks. en SYN i et TCP handshake. 
Det er her at firewallen tjekker om forbindelsen er godkendt eller ej.
# Established
Established er den tilstand en forbindelse får når der er etableret en forbindelse, sker typisk efter den første pakke, altså efter tilstanden "new". F.eks. SYN/ACK - ACK efter den første SYN i et TCP handshake. 

Der er blevet tjekket om forbindelsen er godkendt af firewallen, derfor godkendes alle pakker når forbindelsen har fået tilstanden "established".
# Related
Denne tilstand gives til forbindelser der er relateret til en established forbindelse, men som ikke er en egentlig del af den forbindelse. 
Samme som established, forbindelsen er godkendt, derfor bliver alle pakkerne godkendt. 