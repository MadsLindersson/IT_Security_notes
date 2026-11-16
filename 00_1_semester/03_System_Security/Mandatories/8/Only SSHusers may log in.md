![[Pasted image 20261116131232.png]]

# Create group sshusers in LAM
![[Pasted image 20261116131529.png]]

# Clear cache and getent sshusers - Desktop 2
![[Pasted image 20261116131609.png]]

# Update 10-hardening.conf -Desktop 2
![[Pasted image 20261116131646.png]]

# Test if Lars gets in - Desktop 1
![[Pasted image 20261116131759.png]]
<mark style="background: #BBFABBA6;">Lars gets in</mark>

# Test if Maria gets in - Desktop 1
![[Pasted image 20261116131845.png]]
<mark style="background: #FF5582A6;">Maria is refused</mark>

![[Questions.png]]

- Det stopper ikke som sådan en trussel, men det aktivere yderligere "least priviledge" da vi nu kan styre præcis hvem der får SSH adgang. Det gør at hvis en person får adgang til f.eks. Maria's bruger, så har de stadig ikke SSH adgang.
- Det beskytter ikke mod at en angriber får adgang til Lars' PC og derved har SSH adgang.