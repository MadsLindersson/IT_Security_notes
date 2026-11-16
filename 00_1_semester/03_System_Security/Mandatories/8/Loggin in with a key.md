![[Pasted image 20261116112818.png]]

# Create a key as lars - Desktop 1
![[Pasted image 20261116113148.png]]
![[Pasted image 20261116113201.png]]

# Copy the key to Desktop 2
![[Pasted image 20261116113258.png]]
![[Pasted image 20261116113305.png]]

# Log in as lars again to see if password or phrase it asked is asked
![[Pasted image 20261116113346.png]]

# Check the copied SSH key on desktop 2
![[Pasted image 20261116113441.png]]

![[Pasted image 20261116113542.png]]
Nej "public key" er offentlig og kan ikke bruges til noget uden "private key" der tilhører. 
Key og passphrase er ikke two factor, gættes passphrase til nøglen er nøglen nu brugbar. 

![[Questions.png]]

- At lave en SSH nøgle stopper os fra at sende vores password over netværket. Da det er "serveren" der sender den tilhørende public key og vores maskine kan bevise at den kan åbne den med privat key, så har vi bevist er vi er den vi siger vi er og kan få adgang uden at sende noget over netværket. 
- Det beskytter ikke mod at skulle bruge et stærkt password in case at der er nogen der får adgang til ens PC. 
