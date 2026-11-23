1. Start Wireshark on your active network interface.

2. Open an incognito browser window and visit `https://ek.dk`.

3. Locate the TLS handshake and inspect ClientHello, ServerHello and available certificate information.

4. Use the browser certificate viewer or OpenSSL to inspect certificate details not visible in the capture.


# ClientHello, ServerHello & available certificate info
![[Pasted image 20261120094118.png]]

![[Pasted image 20261120094416.png]]

# Certificate viewer
![[Pasted image 20261120094451.png]]

# Check tls-weak-cipher-demo on wireshark and compare
![[Pasted image 20261120100207.png]]

Der sker en masse ClientHello request men der kommer intet ServerHello

![[Pasted image 20261120100241.png]]

Der ligger også en anden extension.