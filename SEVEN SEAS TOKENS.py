import os
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

# NLTK-Ressourcen herunterladen
nltk.download("punkt")
nltk.download("stopwords")

# Ordner mit den txt-Dateien, deren Tokens gezählt werden sollen
ordner_pfad = "seven_seas_txt_korpus cleaned"  # kann theoretisch mit anderen Korpora geändert werden

# Englische Stoppwörter aus NLTK laden, da es sich um englische Texte handelt
stopwords_en = set(stopwords.words("english"))

# Speichern der Ergebnisse
token_statistik_werke = []
token_statistik_serien = {}

# Ordner anschauen und die Tokens zählen lassen
for txt_file in os.listdir(ordner_pfad):
    if txt_file.endswith(".txt"):
        file_path = os.path.join(ordner_pfad, txt_file)

        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

        #  Tokenisierung selbst
        tokens = word_tokenize(text)
        token_count_before = len(tokens)

        # Entfernung der Stoppwörter nach der Liste
        filtered_tokens = [word for word in tokens if word.lower() not in stopwords_en]
        token_count_after = len(filtered_tokens)

        # Ergebnisse pro Werk speichern und Spaltennamen angeben
        token_statistik_werke.append({
            "Werk": txt_file,
            "Tokens_vor_Stoppwortentfernung": token_count_before,
            "Tokens_nach_Stoppwortentfernung": token_count_after
        })

        # Seriennamen extrahieren zur Zuordnung der Sachen
        serien_name = txt_file.split("Vol")[0].strip().replace(".txt", "").strip()

        # Um Fehlermeldungen bei möglichen Nullmeldungen zu vermeiden
        if serien_name not in token_statistik_serien:
            token_statistik_serien[serien_name] = {"Tokens_vor_Stoppwortentfernung": 0,
                                                   "Tokens_nach_Stoppwortentfernung": 0}

        # Tokenanzahl zur Serie addieren, da es mehrere Volumes hier gibt
        token_statistik_serien[serien_name]["Tokens_vor_Stoppwortentfernung"] += token_count_before
        token_statistik_serien[serien_name]["Tokens_nach_Stoppwortentfernung"] += token_count_after

# DataFrames erstellen
df_werke = pd.DataFrame(token_statistik_werke)
df_serien = pd.DataFrame([{"Serie": name,
                           "Tokens_vor_Stoppwortentfernung": data["Tokens_vor_Stoppwortentfernung"],
                           "Tokens_nach_Stoppwortentfernung": data["Tokens_nach_Stoppwortentfernung"]}
                          for name, data in token_statistik_serien.items()])

# Tabelle ist eine Excel-Datei mit zwei Blättern: Tokenanzahl pro Werk / pro Serie
excel_path = "Token_Analyse_Seven_Seas.xlsx"
with pd.ExcelWriter(excel_path) as writer:
    df_werke.to_excel(writer, sheet_name="Pro Werk", index=False)
    df_serien.to_excel(writer, sheet_name="Pro Serie", index=False)

print(f"DONE !  '{excel_path}'.") # Signal des Erfolgs
