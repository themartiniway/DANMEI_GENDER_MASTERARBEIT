import os
import re
import warnings
from ebooklib import epub
from bs4 import BeautifulSoup

# Warnungen ignorieren
warnings.filterwarnings("ignore", category=FutureWarning)

# Ornder erstellen
INPUT_FOLDER = "seven seas epub korpus"  # Ordner mit EPUB-Dateien
OUTPUT_FOLDER = "seven_seas_txt_korpus"  # Ordner für die TXT-Ausgabe

# Sicherstellen, dass der auch wirklich Ausgabeordner existiert
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Extrahieren der Kapitel und dann Rückgabe als ganze txt Datei
def extract_chapters(epub_path):
    try:
        book = epub.read_epub(epub_path)
        chapters = []

        for item in book.get_items():
            if item.media_type == "application/xhtml+xml":  # Nur HTML-Dateien auslesen
                # Keine Bilder o.ä. sollen aufgenommen werden
                soup = BeautifulSoup(item.get_body_content(), "html.parser")

                # Kapitel anhand von Schlüsselwörtern filtern und erkennen
                # Beim Seven Seas-Korpus einfach, da es vom gleichen Verlag stammt
                # Es herrscht Einheitlichkeit bezüglich der Paratexte
                chapter_text = soup.get_text()
                if re.search(r"\bChapter\b", chapter_text, re.IGNORECASE):
                    chapters.append(chapter_text.strip())

        return "\n\n".join(chapters) if chapters else None  # Alle Kapitel zusammenführen

    except Exception as e:
        print(f"Fehler ! Schau nach: {epub_path}: {e}")
        return None


def process_epub_files():
    for filename in os.listdir(INPUT_FOLDER):
        if filename.endswith(".epub"):
            epub_path = os.path.join(INPUT_FOLDER, filename)
            txt_content = extract_chapters(epub_path)

            if txt_content:  # Falls Kapitel gefunden wurden
                txt_filename = os.path.splitext(filename)[0] + ".txt"
                txt_path = os.path.join(OUTPUT_FOLDER, txt_filename)

                with open(txt_path, "w", encoding="utf-8") as f:
                    f.write(txt_content)

                print(f"DONE: {txt_filename}")


if __name__ == "__main__":
    process_epub_files()
