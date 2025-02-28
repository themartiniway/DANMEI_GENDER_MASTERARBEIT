Hier folgt ein Überblick aller relevanten Ordner und Python-Skripte mit kurzer Erklärung. 



PYTHON SKRIPTE: 

Für den SEVEN SEAS-Korpus:
SEVEN SEAS DIAGRAMME.py
	Hiermit werden Balkendiagramme erstellt, 
	die pro Serie die Ergebnisse der Annotation beider Charaktere auf einmal zeigen. 
	Dabei handelt es sich um die numerischen Werte, 
	es wird somit die Anzahl der Treffer gezeigt. 
	Zudem werden Kreisdiagramme erstellt. 
	Zu jeden einzelnen Charakter werden drei Kreisdiagramme erschaffen, 
	die jeweils in Prozentzahlen die Verteilung 
	bezüglich der drei Oberkategorien der Annotation 
	- Körperlichkeit, Handeln, Emotionen - zeigen. 


SEVEN SEAS REGEX ANNOTATION.py
	Das hier annotiert Danmei-Texte automatisch basierend
	auf einem vordefinierten Annotationsschema. 
	Dabei werden die beiden Hauptcharaktere jedes Werks anhand ihrer Namen gesucht 
	und ihre Beschreibung hinsichtlich Körperlichkeit, Emotionen und Handeln analysiert.
	Die Annotation erfolgt auf Satzebene, wobei Schlüsselwörter (reguläre Ausdrücke) 
	und deren Synonyme erkannt werden.
	Die Ergebnisse werden in einer Excel-Datei gespeichert. 


SEVEN SEAS EPUB ZU TXT.py
	Hiermit wurden die originalen ePub-Dateien in txt.-Dateien umgewandelt. 
	Die Ergebnisse hiervon werden im Ordner seven_seas_txt_korpus gespeichert. 

SEVEN SEAS TOKENS.py
	Durch dieses Skript wurde die Tokenanzahl pro Werk und pro Serienname gezählt. 

SEVEN SEAS PRONOUN USAGE.py
	Hiermit wird geschaut, welche Pronomen mit welchen Adjektiven in Verbindung stehen. 

SEVEN SEAS-MINING
	Hier werden im gesamten Korpus 
	die 100 häufigsten Wörter, 
	die 200 häufigsten Bigramme (Kollokationsanalyse), 
	die 200 häufigsten Trigramme (Kollokationsanalyse),
	sowie die 200 häufigsten Adjektive gesucht und
	am Ende in einer Excel-Tabelle gespeichert. 



Für den CG-Korpus: 
CG epub zu txt.py
	Hiermit wurden die originalen ePub-Dateien in txt.-Dateien umgewandelt.
	Die Ergebnisse hiervon werden im Ordner epub_als_txt gespeichert. 

CG KORPUS Erste Auswahl	
	Hier wurden die ersten zehn Werke zufällig ausgewählt. 
	Später sind ab hier die Probleme langsam aufgetaucht
	wie im Text der MA beschrieben wird. 

CG Extraktion der epub mit chapters.py
	Nach der zufälligen Kapitelauswahl
	werden hier gezielt die Kapitel extrahiert,
	indem nach der angegebenen Kapitelnummer gesucht wird. 
	Sie werden im Ordner extrahierte_kapitel gespeichert. 

CG Korpus Bereicherung.py
	Nachdem es sich herausstellte, 
	dass leider nicht zu allen Werken auf CG.com epub-Dateien existieren, 
	wurden hier manuell Werke zu einer Tabelle hinzugefügt,
	um eine zufällige Auswahl der Kapitel
	basierend auf der angegebenen Gesamtanzahl eines Werkes zu treffen. 

CG Html Bereinigung der txt file.py
	Einige extrahierten txt-Dateien besaßen html-Entities, 
	die hiermit entfernt bzw. umgewandelt wurden. 







ORDNER: 

Für den SEVEN SEAS-Korpus: 
seven seas epub korpus
	Hier befinden sich die originalen ePub-Dateien 
	der Danmei-Werke des SEVEN SEAS-Korpus.
 
seven_seas_txt_korpus
	Hier befinden sich die umgewandelten txt.-Dateien des SEVEN SEAS-Korpus. 

seven_seas_txt_korpus cleaned
	Hier befinden sich die manuell gesäuberten txt.-Dateien.
	Aufgrund der Einheitlichkeit der Originale 
	musste hierbei nur das Glossar und Inhaltsverzeichnis entfernt werden. 

Gruppierte_Balkendiagramme
	In diesem Ordner werden die durch ein Python-Skript 
	erstellten jpg-Dateien gespeichert. 

nltk_data
	Hier befindet sich das wordnet Paket für die Synonyme.  

Normierte_Kreisdiagramme
	In diesem Ordner werden die durch ein Python-Skript 
	erstellten jpg-Dateien gespeichert. 





Für den CG-Korpus: 
CG-Korpus
	Hier befinden sich alle relevanten Ordner und Skripte, 
	die für das CG-Korpus benutzt worden sind. 
	Da sie und jegliche daraus gewonnenen Ergebnisse 
	leider im weiteren Verlauf der Arbeit dann unwichtig geworden sind, 
	aber sie aus Gründen der Archivierung und Reflexion weiterhin von Bedeutung sein können, 
	wurden sie alle an einem Ort gruppiert. 

epub_als_txt
	Hier befinden sich die umgewandelten txt.-Dateien der Danmei-Werke. 

epub_werke
	Hier befinden sich die originalen ePub-Dateien der Danmei-Werke des CG-Korpus. 
	
edited chapters
	Hier befinden sich die gesäuberten txt-Dateien nach der Kapitelextraktion. 
	Alle Dateien wurden hierbei manuell gesäubert, 
	indem jegliche Parataxe entfernt wurden. 

edited chapters annotate	
	Hier befinden sich die Werke, die annotiert werden sollen. 

extrahierte_kapitel
	Nach der zufälligen Auswahl der Kapitel,
	erscheinen hier die extrahierten Kapitel der Danmei-Werke als txt-Dateien. 




