![[Pasted image 20261116121151.png]]

# Add two lines to 10-hardening.conf
![[Pasted image 20261116125749.png]]

# Restart and then test
![[Pasted image 20261116130012.png]]
<mark style="background: #FFB8EBA6;">password and kbdinteractive er begge sat til "no"</mark>

# Force a password login
![[Pasted image 20261116130121.png]]

![[Pasted image 20261116130156.png]]
Uden nøgle eller en TGT kræver det at Jens bliver added til KDC eller også vil jeg mene at der skal kopieres en public key ind, men det er en med adgang til serveren som skal kopiere den ind for Jens. 

![[Questions.png]]

- Det stopper en angriber som har fået fat i et password i at komme ind på serveren da det nu vil kræve noget andet end et password. 
- Det beskytter stadig ikke fra at hvis en angriber får fat i en private key så kan de stadig komme ind. Det stopper heller ikke hvis de har fået adgang til en medarbejders PC, altså fået fat i deres password, så kan angriberen stadig komme ind fordi medarbejderen jo har adgang med enten en KDC eller en key.