**Principle of least priviledge**
![[Pasted image 20260930093254.png]]

For at undgå at hvis en bruger bliver hacket eller lign. så har hackeren kun adgang til de ting som brugeren har adgang til og ikke mere. Det begrænser hvad der bliver exposed

**Priviledge seperation**
Seperere adgang ifbm. den rolle som brugeren har. 
F.eks. har en admin ikke brug for adgang til alt, kun det nødvendige for en admin.

Handler også om at begrænse hvad en hacker kan få adgang til. 

**Full sudo rettighedder**
![[Pasted image 20260930093718.png]]

![[Pasted image 20260930093837.png]]

#### sudoers file
En fil der indeholder hvilke brugere der har hvilke sudo rettighedder der ejes af root.
Indeholder ikke alle farlige kommandoer, *resten skal restrictes via fil rettigheder*

![[Pasted image 20260930094324.png]]

**Aliases**
En form for variable vi kan ligge data ind i og derefter fortælle f.eks. hvilke rettigheder dem i variablen skal have.

![[Pasted image 20260930095524.png]]

*Bør gælde alle steder, cloud, api keys, fysisk adgang*

**Database rettighedder**
Rettighedder kan også gælde i f.eks. en database:
![[Pasted image 20260930101645.png]]
