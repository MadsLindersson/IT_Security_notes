
> [!info] Prepare Desktop 2
> ![[Pasted image 20261113135148.png]]

> [!info] Give Desktop 2 a key
> #### Add principle - randkey
> ![[Pasted image 20261113142229.png]]
> 
> #### Check if a key was made
> ![[Pasted image 20261113142318.png]]
> 
> #### Look at who can red the keytab file (root)
> ![[Pasted image 20261113142402.png]]
> 


> [!info] Create kerberos.conf
> ![[Pasted image 20261116092418.png]]
> Set GSSAPIAuthentication to "yes"
> 
> GSSAPIAuthentication is the interface that SSH uses to talk to Kerberos


> [!info] Test if it works - log in as maria
> #### Ticket Granting Ticket (TGT) active
> ![[Pasted image 20261116092823.png]]
> 
> #### SSH from Desktop 1 into Desktop 2 
> ![[Pasted image 20261116093002.png]]
> ![[Pasted image 20261116093014.png]]
> 
> #### There are now also a service ticket
> ![[Pasted image 20261116093104.png]]
> 
> #### Testing login with debug output
> ![[Pasted image 20261116093531.png]]
> It works but it also stays as is and does not really let me do anything
> ![[Pasted image 20261116093654.png]]
> I got both tickets
> 
> #### Checking login without TGT
> ![[Pasted image 20261116094011.png]]
> It does not ask for a password, because an SSH key has been saved - therefore it uses the key instead and maria has logged in on Desktop 2
> 
