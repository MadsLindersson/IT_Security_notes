# Add server to /etc/hosts
![[Pasted image 20261027090238.png]]
### Test connection
![[Pasted image 20261027090729.png]]

# Install sssd tools
![[Pasted image 20261027091916.png]]

# Configure SSSD.conf
![[Pasted image 20261027092843.png]]

### Change rights on SSSD.conf - RW only for root
![[Pasted image 20261027093434.png]]

Systemctl enable --now sssd - Sets the sssd service to run on bootup and starts the service

# Create home dir's automatically
![[Pasted image 20261027093802.png|593]]

# Check name resolution
![[Pasted image 20261027093858.png]]

# Test if setup works on Maria

### getent på Maria
![[Pasted image 20261027094217.png]]

### id Maria
![[Pasted image 20261027100934.png]]

### su Maria
![[Pasted image 20261027101305.png]]

### Check if mhansen home directory has been created
![[Pasted image 20261027101833.png]]

