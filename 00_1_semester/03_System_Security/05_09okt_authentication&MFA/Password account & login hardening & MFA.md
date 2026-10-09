**KDF** - Key Derivation functions
- Lavet til at være langsomme
**Salt**
- En random værdi foran hash som ikke er hashet

**Proofs for who you are**
![[Pasted image 20261009084504.png]]

**AAA**
![[Pasted image 20261009084827.png|516]]

**Sæt en expiry date for en bruger**
useradd: ved oprettelse
usermod: ved eksisterende bruger
![[Pasted image 20261009091451.png|523]]

**Lås eller lås op for en brugers account**
![[Pasted image 20261009092235.png|542]]

##### PAM - Pluggable Authentication Modules
```
A shared layer that login, sudo, sshd, su and other programs all use
for authentication — instead of each one inventing its own logic.
```

4 Regler:
![[Pasted image 20261009094942.png|582]]

```
En forkert linje kan smadre en del, så en god ide at tage snapshit inden man går igang
```

![[Pasted image 20261009095305.png|489]]

Der kan sættes google MFA op med PAM

##### ACCT 
![[Pasted image 20261009100647.png|486]]

