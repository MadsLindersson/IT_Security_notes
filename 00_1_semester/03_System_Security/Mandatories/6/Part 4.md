# Add Sofie
![[Pasted image 20261027104532.png]]

### getent desktop 1
![[Pasted image 20261027104738.png]]
### getent desktop 2
![[Pasted image 20261027104754.png]]

# Edit Jens' login shell to false
Setting to false is the same as nologin, just with no message other than "false" being shown to the user when trying to log in. nologin has a user friendly message displayed. 
<mark style="background: #FFB8EBA6;">nologin does not exist in LAM</mark>
![[Pasted image 20261027105746.png|610]]

### Clear cache
![[Pasted image 20261027110218.png]]
### su Jens
No message because he is set to "false" and not "nologin"
![[Pasted image 20261027110155.png]]

# Check if the groups are visibel on the desktops
![[Pasted image 20261027110813.png]]

# id Lars
![[Pasted image 20261027110916.png]]

# Creating sudo rule for ldapadmins
### Create 90-ldapadmins file
![[Pasted image 20261027111916.png]]

### Checking new sudo rule as Lars
![[Pasted image 20261027112541.png]]
### Checking new sudo rule as Maria
![[Pasted image 20261027112625.png]]

### Who decides who is an admin now?
Det bliver bestemt på directory og ikke pr. maskine. Vi har sat reglen op på hver maskine, men hvem der er en del af ldapadmins er bestemt af LDAP

# Set up file ownership and ACL's 
![[Pasted image 20261027113130.png|562]]![[Pasted image 20261027113252.png]]
##### Kun Maria der har RW på report.txt
##### Lars har R rettighed på filen selvom han ikke er en del af Sales gruppen

### Desktop 2
![[Pasted image 20261027113756.png]]

# Nået til 4.5
