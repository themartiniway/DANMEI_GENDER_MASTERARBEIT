#Notwendige Packages
import os
import pandas as pd
import difflib
import nltk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
import re

# Download der Synonym-Datenbank
nltk.download("wordnet")
lemmatizer = WordNetLemmatizer()

#  Pfad zum Ordner und Benennen der Excel-Datei, die am Ende erstellt wird
kapitel_ordner = "seven_seas_txt_korpus cleaned"  # TXT-Dateien mit den extrahierten Kapiteln
output_excel = "annotations_analysis_optimizedV2.xlsx"  # Finale Excel-Datei

# Benenen der Werke & Charaktere mit allen bekannten Namen zur Auffindung im Korpus
# Diese Werknamen erscheinen später in der Tabelle
# Dadurch werden nicht die Namen der txt.-Dateien an sich genommen
werke_charaktere = {
    "Guardian": (["Zhao Yunlan"], ["Shen Wei"]),
    "Heaven's Official Blessing": (["Hua Cheng", "Crimson Rain Sought Flower", "San Lang", "Wu Ming"],
                                   ["Xie Lian", "Xianle", "Highness", "Gege", "General Hua"]),
    "Grandmaster of Demonic Cultivation": (["Wei Wuxian", "Wei Ying", "Yiling Patriarch", "Mo Xuanyu"],
                                           ["Lan Zhan", "Lang Wangji", "Hanguang-jun"]),
    "Thousand Autumns": (["Yan Wushi"], ["Shen Qiao", "Ah Qiao"]),
    "Stars of Chaos": (["Gu Yun", "Gu Zixi", "Marshal Gu", "Yifu", "Shen Shiliu", "Marquis of Order"],
                       ["Chang Geng", "Li Min", "Yan Wang", "Yan Bei Wang"]),
    "Ballad of Sword and Wine": (["Shen Zechuan", "Lanzhou", "Shen Lanzhou"],
                                 ["Xiao Chiye", "Ce'an", "A-ye", "Xiao Ce'an"]),
    "Peerless": (["Cui Buqu"], ["Feng Xiao"]),
    "Remnants of Filth": (["Gu Mang"], ["Mo Xi"]),
    "The Husky and His White Cat Shizun": (["Mo Ran", "Mo Weiyu", "Taxian-jun", "Mo Zongshi"],
                                          ["Chu Wanning", "Shizun", "Wanning", "Xia Sini", "Yuheng Elder",
                                           "Yuheng of the Night Sky", "Beidou Immortal"]),
    "The Scum Villain's Self-Saving System": (["Shen Yuan", "Shen Qingqiu", "Shizun"], ["Luo Binghe"]),
    "Case File Compendium": (["He Yu", "Young Master He", "Eldest Young Master He", "Little Devil"],
                             ["Xie Qingcheng", "Doctor Xie", "Professor Xie"]),
    "The Disabled Tyrant's Pet Palm Fish": (["Li Yu", "Fish Daddy", "Xiao Yu", "Li-gongzi"],
                                           ["Jing Wang", "Crown Prince", "Wang Ye", "5th Prince", "Prince Jing", "Mu Tianchi"])
}

# Annotationsschema Nummer 1
# Dieses Schema wurde verwendet für die numerische Tabelle im Text der Masterarbeit selbst
annotationsschema = {
    "f-Körperlichkeit": ["delicate", "elegant", "beautiful", "graceful", "slim"],
   "m-Körperlichkeit": ["strong jawline", "broad shoulders", "muscular", "handsome"],
   "f-Emotionen": ["cry", "blush", "shy", "gentle"],
    "m-Emotionen": ["yell", "strong", "dominant", "angry"],
    "f-Handeln": ["avoids", "hesitant", "uncertain", "listen"],
    "m-Handeln": ["assertive", "protect", "lead", "fight"]
}


# Schema Nummer 2
# Es wurden verschiedene Kombinationen ausprobiert, allerdings blieb die Tendenz ähnlich
annotationsschema = {
    "f-Körperlichkeit": ["delicate", "elegant", "beautiful", "graceful", "slim"],
    "m-Körperlichkeit": ["muscular", "sturdy", "broad", "handsome"],
    "f-Emotionen": ["cry", "blush", "shy", "gentle"],
    "m-Emotionen": ["yell", "strong", "dominant", "angry"],
    "f-Handeln": ["avoids", "hesitant", "uncertain", "listen"],
    "m-Handeln": ["assertive", "protect", "lead", "fight"]
}



# Generierung der Synoyme, um mehr Treffer im Text finden zu können
def erweitere_mit_synonymen(wortliste):
    synonyme = set(wortliste)
    for wort in wortliste:
        for synset in wordnet.synsets(wort):
            for lemma in synset.lemmas():
                synonyme.add(lemma.name().replace("_", " "))
    return list(synonyme)

# Alle Kategorien werden mit Synonymen erweitern und bereichert
annotationsschema = {kategorie: erweitere_mit_synonymen(wörter) for kategorie, wörter in annotationsschema.items()}

# Erkennung von Werk-Namen aus Dateinamen
# , da die Dateien selbst aufgrund der versch. Vol.-Angaben
# verschiedene Namen besitzen.
# Somit werden die Serien auch später zusammengeführt
# Bestimmte Elemente der Dateinamen werden entfernt
def bereinige_dateiname(dateiname):
    dateiname = re.sub(r'[_-]', ' ', dateiname)
    dateiname = re.sub(r'\bvol\.?\s?\d+', '', dateiname, flags=re.IGNORECASE)
    dateiname = re.sub(r'\(.*?\)', '', dateiname)
    dateiname = re.sub(r'\s+', ' ', dateiname).strip()
    return dateiname.lower()

def finde_besten_match(dateiname, werke_liste):
    dateiname_bereinigt = bereinige_dateiname(dateiname)
    matches = difflib.get_close_matches(dateiname_bereinigt, werke_liste, n=1, cutoff=0.4)
    return matches[0] if matches else None

# Annotation der Texte selbst -> Defintion
def annotiere_text(text, werk, dateiname):
    annotationen = []
    if werk not in werke_charaktere:
        print(f"⚠️ Keine Hauptfiguren gefunden für {werk}") # Fehlermeldung zur Sicherheit
        return []

    mann_a_namen = werke_charaktere[werk][0]
    mann_b_namen = werke_charaktere[werk][1]
    alle_charakternamen = mann_a_namen + mann_b_namen

    sätze = re.split(r'(?<=[.!?]) +', text) # Sätze werden gesplittet

    for satz in sätze:
        satz_lower = satz.lower()

        # Kommt der Charaktername im Satz vor?
        gefundene_charaktere = [name for name in alle_charakternamen if name.lower() in satz_lower]

        if not gefundene_charaktere:
            continue  # Überspringen des Satzes, wenn kein Charakter erwähnt wird
            # Vermeidung von Warnungen

        # Satz nach Annotationswörtern durchsuchen
        for kategorie, woerter in annotationsschema.items():
            for wort in woerter:
                if wort in satz_lower:
                    # den Annotationsbegriff wird dem ersten gefundenen Charakter zugewiesen
                    for charakter in gefundene_charaktere:
                        annotationen.append({
                            "filename": dateiname,
                            "werk": werk,
                            "character": charakter,
                            "text_snippet": wort,
                            "category": kategorie
                        })
    return annotationen

# Verarbeitung aller Dateien
alle_annotationen = []
werke_liste = list(werke_charaktere.keys())

for dateiname in os.listdir(kapitel_ordner):
    if dateiname.endswith(".txt"):
        werkname_bereinigt = finde_besten_match(dateiname, werke_liste)
        if werkname_bereinigt:
            dateipfad = os.path.join(kapitel_ordner, dateiname)
            with open(dateipfad, "r", encoding="utf-8") as file:
                text = file.read()
                annotationen = annotiere_text(text, werkname_bereinigt, dateiname)
                alle_annotationen.extend(annotationen)

#  Excel-Tabelle wird erstellt
df_annotations = pd.DataFrame(alle_annotationen)

if not df_annotations.empty:
    # Mapping der anderen Namen auf die richtigen Figuren
    alias_to_main = {}
    for werk, (mann_a_namen, mann_b_namen) in werke_charaktere.items():
        main_a = mann_a_namen[0]
        main_b = mann_b_namen[0]
        for alias in mann_a_namen:
            alias_to_main[alias] = main_a
        for alias in mann_b_namen:
            alias_to_main[alias] = main_b

    # Aliasnamen durch Hauptnamen ersetzt
    df_annotations["character"] = df_annotations["character"].map(alias_to_main)

    # Erstellen der pivot-Tabelle, um die numerischen Werte zu erlangen
    df_pivot = df_annotations.pivot_table(index=["werk", "character"], columns="category", aggfunc="size", fill_value=0)
    df_pivot.reset_index(inplace=True)

    # Speichern der Datei und Benennung der Tabellenseiten
    with pd.ExcelWriter(output_excel) as writer:
        df_annotations.to_excel(writer, sheet_name="Detaillierte Annotationen", index=False)
        df_pivot.to_excel(writer, sheet_name="Kategorie-Zusammenfassung", index=False)

# Angabe des Names, damit signalisiert wird, dass der Prozess fertig ist
    # Zudem, um die Datei dann möglichst schnell finden zu können,
    # wird nochmal an den Namen der Datei erinnert
    print(f"Geschafft! Ergebnisse gespeichert als '{output_excel}'.")
else:
    # Fehlermeldung zur Sicherheit, sollte etwas schief gehen
    print("Keine Annotationen gefunden.")
