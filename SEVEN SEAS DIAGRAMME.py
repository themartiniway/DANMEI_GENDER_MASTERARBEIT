import os
import pandas as pd
import matplotlib.pyplot as plt

# Excel-Datei
excel_datei = "Ergebnisse Annotation.xlsx"  # Excel-Datei
sheet_name = "Kategorie-Zusammenfassung"  # Tabellenblattname

# Erstellen eines Ordners zum Speichern der Bilder am Ende
balkendiagramm_ordner = "Gruppierte_Balkendiagramme"
kreisdiagramm_ordner = "Normierte_Kreisdiagramme"

# Für Notfälle und möglichen Fehlermeldungen zu umgehen,
# wird hier geprüft, ob ein Ornder existiert
# Wenn nicht, wird eins erstellt
os.makedirs(balkendiagramm_ordner, exist_ok=True)
os.makedirs(kreisdiagramm_ordner, exist_ok=True)

# Daten aus der Tabelle einlesen
df = pd.read_excel(excel_datei, sheet_name=sheet_name)

# Spaltennamen bereinigen von Leerzeichen
df.columns = df.columns.str.strip()

# Pastellfarben für die Balkendiagramme
# Pastell, damit es nicht zu intensiv wirkt
farben = {
    'f-Emotionen': '#FFCCCC',  # hell rot
    'f-Handeln': '#FF9999',  # rot
    'f-Körperlichkeit': '#FF6666',  # dunkleres rot
    'm-Emotionen': '#CCFFCC',  # Hell grün
    'm-Handeln': '#99FF99',  # grün
    'm-Körperlichkeit': '#66FF66'  # dunkleres grün
}

# Pastellrot/Grün für die Kreisdiagramme
farben_kreis = ['#FF9999', '#99FF99']  # Dabei Pastellrot für f, Pastellgrün für m

# Gruppiertes Balkendiagramm ->
# 2 Charaktere pro 1 Werk werden dann angezeigt
for werk in df['werk'].unique():
    df_werk = df[df['werk'] == werk]
    if len(df_werk) < 2:
        continue  # um Fehlermeldungen zu vermeiden

    df_werk_plot = df_werk.set_index('character')[farben.keys()]

    ax = df_werk_plot.plot(kind='bar', figsize=(10, 6), color=[farben[col] for col in df_werk_plot.columns])
    plt.title(f'{werk}')
    plt.xlabel('Charakter')
    plt.ylabel('Anzahl der Annotationen')
    plt.xticks(rotation=0)
    plt.legend(loc='upper right')
    plt.tight_layout()

    #  JPG Speicherung
    filename = f"{balkendiagramm_ordner}/{werk.replace(' ', '_')}_Balkendiagramm.jpg"
    plt.savefig(filename, format='jpg')
    plt.close()
    print(f"📁 Gespeichert: {filename}")

#  Kreisdiagramme pro Hauptkategorie für jeden Charakter
# Erstellen von drei Kreisen pro Annotationskategorie
for idx, row in df.iterrows():
    charakter = row['character']

    # Daten für die Kreisdiagramme
    emotionen = [row['f-Emotionen'], row['m-Emotionen']]
    handeln = [row['f-Handeln'], row['m-Handeln']]
    körperlichkeit = [row['f-Körperlichkeit'], row['m-Körperlichkeit']]

    kategorien = ['f', 'm']

    #  3 Kreisdiagramme nebeneinander
    fig, axs = plt.subplots(1, 3, figsize=(18, 6))

    axs[0].pie(emotionen, labels=[f"{k}-Emotionen" for k in kategorien], autopct='%1.1f%%', colors=farben_kreis,
               startangle=140)
    axs[0].set_title(f'Emotionen – {charakter}')

    axs[1].pie(handeln, labels=[f"{k}-Handeln" for k in kategorien], autopct='%1.1f%%', colors=farben_kreis,
               startangle=140)
    axs[1].set_title(f'Handeln – {charakter}')

    axs[2].pie(körperlichkeit, labels=[f"{k}-Körperlichkeit" for k in kategorien], autopct='%1.1f%%',
               colors=farben_kreis, startangle=140)
    axs[2].set_title(f'Körperlichkeit – {charakter}')

    plt.suptitle(f'{charakter}', fontsize=16)
    plt.tight_layout()

    # JPG Speicherung
    filename = f"{kreisdiagramm_ordner}/{charakter.replace(' ', '_')}_Kreisdiagramm.jpg"
    plt.savefig(filename, format='jpg')
    plt.close()
    print(f"Gespeichert: {filename}")
    # Um den Prozess beobachten zu können,
    # und bei möglichen Fehlern irgendwie eingreifen zu können
    # bzw. darüber Bescheid zu wissen

# Endmeldung zum Signal
print("geschafft!")
