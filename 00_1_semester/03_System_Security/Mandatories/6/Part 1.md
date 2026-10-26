# Set hostname
![[Pasted image 20261023110254.png]]

# Edit /etc/hosts and add server IP and name
![[Pasted image 20261023110544.png]]

# Install ldap-utils
![[Pasted image 20261023111123.png]]

# Run the configuration wizard
![[Pasted image 20261023112446.png]]

# Check if the server works
![[Pasted image 20261023113606.png|518]]

# Checking if the nis and inetorgperson schema is there
![[Pasted image 20261023113948.png]]

# Create the two containers
### Create base.ldif
![[Pasted image 20261023120826.png]]

### Add containers to base.ldif
![[Pasted image 20261023121007.png|509]]

### Add base.ldif to LDAP
![[Pasted image 20261023121740.png]]

### Install LAM (LDAP-Account-Manager)
![[Pasted image 20261023121924.png]]

### Check if the apche2 webserver is running
![[Pasted image 20261023122059.png|509]]

### Open 192.168.64.130/lam in browser
![[Pasted image 20261023131735.png]]

### Configure LAM
##### General settings
![[Pasted image 20261023133713.png]]

![[Pasted image 20261023133857.png]]

##### Security settings
![[Pasted image 20261023134146.png|555]]

##### Account settings
![[Pasted image 20261023134304.png|531]]

##### Changed password away from lam

##### Login
![[Pasted image 20261023140424.png]]

### Create groups
![[Pasted image 20261023142655.png]]

### Create users
![[Pasted image 20261023143550.png]]

### Make Lars part of ldapadmins group
![[Pasted image 20261023143846.png]]

### Check if users work on the server
##### Search
![[Pasted image 20261023145932.png]]
##### whoami
![[Pasted image 20261023145123.png]]

### 