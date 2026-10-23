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

