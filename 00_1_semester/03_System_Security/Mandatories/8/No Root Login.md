![[Pasted image 20261116114809.png]]

# What does sshd use now? does it have a password?
![[Pasted image 20261116115956.png]]
output betyder at vi godt må logge ind med root, hvis vi bruger en SSH key pair, men ikke med et password 

![[Pasted image 20261116120040.png]]
Output betyder at root ikke har et password, det er disabled. "L" betyder locked.

# Create 10-hardneing.conf og sæt PermitRootLogin til "no"
![[Pasted image 20261116120356.png]]

![[Pasted image 20261116120429.png]]

Den er nu sat til "no" hvilket betyder at der ikke kan logges in med root over SSH.

![[Questions.png]]

- At nægte root adgang over SSH stopper en angriber i at kunne gøre alt hvad de vil hvis de nu får adgang til en medarbejders maskine eller SSH nøgle. 
- Det stopper ikke angriberen i at få adgang til det som brugeren har adgang til, så hvis brugeren f.eks. er en admin konto med sudo rettigheder så er der stadig rigtigt angriberen kan se og pille ved. 
