*authentication* = who are you?
*authorization* = what are you allowed to do?

![[Pasted image 20261002083746.png]]

	- /: root
	- /bin: points to /usr/bin and contains needed utilities to boot
	- /sbin: points to /usr/sbin
	- /usr: user usable programs and data
	- /usr/bin: core/fundamental system utilities (alle brugere)
	- /usr/sbin: system administration commands (admins)
	- /home: personal directories
	- /etc: System wide config files (/etc/passwd)
	- /dev: device files representing hardware (/dev/sda = disc)
	- /tmp: scratch space, wiped on reboot (temp space)
	- /var: data that change while the system runs (log)
	- /lib: shared library
	- /mnt: a temp mount point (usb)

![[Pasted image 20261002085835.png]]

![[Pasted image 20261002102107.png]]


![[Pasted image 20261002102600.png|155]]

![[Pasted image 20261002102626.png]]

![[Pasted image 20261002104444.png]]

**SUID:** If a file has SUID permission it will always execute as the user who owns the file
**SGID:** similar to SUID but with groups
- On a file its the same as SUID but with group instead of user
- On a directory any files created in that directory gets the group as owner
**Sticky bit:** put on a shared folder, makes it so only the owner of the file or the directory can remove the file

