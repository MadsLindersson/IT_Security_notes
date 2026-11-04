# Hash Functions
- Hashes bliver brugt til checksum
- Et hash skal helst være symmetrisk, altså altid samme størrelse. Det er fordi at hvis hashen fik forskellige størrelser, ville det være nemmere at regne tilbage og finde frem til originalværditen

> [!info] Hashing CIA
> Hashing hører til integritet i CIA

> [!Info] Digest
> Resultet på en hash algoritme kaldes for en "Digest"

> [!info] Deterministic
> Et hash skal være deterministic, dvs. en værdi skal altid give det samme hash, en værdig må aldrig kunne give 2 digests

Der er forskellige måder at lave hash funktioner på. F.eks.:
- Merkle-Damgård
	- <mark style="background: #FF5582A6;">Vigtig at forstå!</mark>
- Sponge function
	- Skal vi ikke kunne forklare


> [!info] avalance effect
> Det skal være svært at ændre på en værdi uden også at ændre hashet


> [!info] Collision resistance
> 2 værdier må ikke kunne give samme hash. dette er en kollision og hash funktionen vil være broken

> [!info] Preimage resistance
> Det må aldrig være muligt at "gå den anden vej", altså man må ikke kunne hashe en værdi og så kunne få værdien ud igen. Dette er imod brute forcing. Det handler om at det skal tage for meget computer kraft. 

> [!info] Second-preimage resistance
> <mark style="background: #FF5582A6;">Læs op!</mark>

> [!info] Birthday attacks
> Man generere hash værdier og prøver at finde collisions.
> <mark style="background: #FF5582A6;">Læs op!</mark>

# Password protection

> [!warning]
> Kun at køre hashing er ikke sikkert nok!

> [!info] offline attacks / salt
> Brug af "salt"!
> Salt skal gemmes i databasen
> Salt er en random værdi, helst unik for hver bruger, der ligges sammen passworded og derefter hashes der.

# Key Derivation Functions (KDF)
Gør hashing langsommere og mere krævende ift. computerkraft.
