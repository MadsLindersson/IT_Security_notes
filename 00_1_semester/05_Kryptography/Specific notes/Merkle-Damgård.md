Merkel-Damgård er en designmetode til hashfunktioner, ikke en hashfunktion i sig selv. 
Den går ud på at kunne tage en vilkårlig størrelse input og stadig kunne producere den samme størrelse hash værdi, altid. 

Det sker ved at opdele inputtet i blokke, det kunne være 512 bits, og hvis der så er en rest som ikke er 512 bits, så bruges der padding til at udfylde den sidste blok. 
Der bliver brugt en [[kompressions function]] hvor der bliver sendt 2 inputs ind i. Første 2 værdier er en startværdi (kaldet IV), som er en fast værdi, og den først blok.

Når alle blokke har været igennem kompressions funktionen så er der en hashværdi tilbage. 