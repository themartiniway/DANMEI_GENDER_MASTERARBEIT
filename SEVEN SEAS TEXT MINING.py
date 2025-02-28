import os
import re
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize, pos_tag, ngrams, FreqDist
from nltk.stem import WordNetLemmatizer
from collections import Counter
from openpyxl import Workbook

# NLTK-Setup
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('wordnet')

# Ordnerpfad
korpus_ordner = "seven_seas_txt_korpus cleaned"

# Excel-Datei als Ergebnis
output_excel = "Text_Mining_Ergebnisse.xlsx"

# Stoppwörter (Englisch), da es englische Texte sind
stop_words = set(stopwords.words('english'))

# Chinesische Silben, die ausgeschlossen werden sollen
# Zweiteilige Wörte usw. werden behalten, um vielleicht auf Fälle mit "Shizun" o.ä. zu stoßen
chinese_syllables = {
    "a", "ai", "an", "ang", "ao", "ba", "bai", "ban", "bang", "bao", "bei", "ben", "beng", "bi", "bian", "biao", "bie", "bin", "bing",
    "bo", "bu", "ca", "cai", "can", "cang", "cao", "ce", "cen", "ceng", "cha", "chai", "chan", "chang", "chao", "che", "chen", "cheng", "chi",
    "chong", "chou", "chu", "chuan", "chuang", "chui", "chun", "chuo", "ci", "cong", "cou", "cu", "cuan", "cui", "cun", "cuo", "da", "dai", "dan",
    "dang", "dao", "de", "deng", "di", "dian", "diao", "die", "ding", "diu", "dong", "dou", "du", "duan", "dui", "dun", "duo", "e", "ei", "en",
    "er", "fa", "fan", "fang", "fei", "fen", "feng", "fo", "fou", "fu", "ga", "gai", "gan", "gang", "gao", "ge", "gei", "gen", "geng", "gong",
    "gou", "gu", "gua", "guai", "guan", "guang", "gui", "gun", "guo", "ha", "hai", "han", "hang", "hao", "he", "hei", "hen", "heng", "hong", "hou",
    "hu", "hua", "huai", "huan", "huang", "hui", "hun", "huo", "ji", "jia", "jian", "jiang", "jiao", "jie", "jin", "jing", "jiong", "jiu", "ju", "juan",
    "jue", "jun", "ka", "kai", "kan", "kang", "kao", "ke", "ken", "keng", "kong", "kou", "ku", "kua", "kuai", "kuan", "kuang", "kui", "kun", "kuo", "la",
    "lai", "lan", "lang", "lao", "le", "lei", "leng", "li", "lia", "lian", "liang", "liao", "lie", "lin", "ling", "liu", "long", "lou", "lu", "luan",
    "lue", "lun", "luo", "ma", "mai", "man", "mang", "mao", "me", "mei", "men", "meng", "mi", "mian", "miao", "mie", "min", "ming", "miu", "mo", "mou",
    "mu", "na", "nai", "nan", "nang", "nao", "ne", "nei", "nen", "neng", "ni", "nian", "niang", "niao", "nie", "nin", "ning", "niu", "nong", "nou", "nu",
    "nuan", "nue", "nuo", "o", "ou", "pa", "pai", "pan", "pang", "pao", "pei", "pen", "peng", "pi", "pian", "piao", "pie", "pin", "ping", "po", "pou", "pu",
    "qi", "qia", "qian", "qiang", "qiao", "qie", "qin", "qing", "qiong", "qiu", "qu", "quan", "que", "qun", "ran", "rang", "rao", "re", "ren", "reng", "ri",
    "rong", "rou", "ru", "ruan", "rui", "run", "ruo", "sa", "sai", "san", "sang", "sao", "se", "sen", "seng", "sha", "shai", "shan", "shang", "shao", "she",
    "shen", "sheng", "shi", "shou", "shu", "shua", "shuai", "shuan", "shuang", "shui", "shun", "shuo", "si", "song", "sou", "su", "suan", "sui", "sun", "suo",
    "ta", "tai", "tan", "tang", "tao", "te", "teng", "ti", "tian", "tiao", "tie", "ting", "tong", "tou", "tu", "tuan", "tui", "tun", "tuo", "wa", "wai", "wan",
    "wang", "wei", "wen", "weng", "wo", "wu", "xi", "xia", "xian", "xiang", "xiao", "xie", "xin", "xing", "xiong", "xiu", "xu", "xuan", "xue", "xun", "ya",
    "yan", "yang", "yao", "ye", "yi", "yin", "ying", "yo", "yong", "you", "yu", "yuan", "yue", "yun", "za", "zai", "zan", "zang", "zao", "ze", "zei", "zen",
    "zeng", "zha", "zhai", "zhan", "zhang", "zhao", "zhe", "zhen", "zheng", "zhi", "zhong", "zhou", "zhu", "zhua", "zhuai", "zhuan", "zhuang", "zhui", "zhun",
    "zhuo", "zi", "zong", "zou", "zu", "zuan", "zui", "zun", "zuo"
}


# Lemmatizer zur Verallgemeinerung
lemmatizer = WordNetLemmatizer()

# Protagonisten-Namen pro Werk
protagonists = {"Guardian": ("Zhao Yunlan", "Shen Wei"),
                "Heaven's Official Blessing": ("Hua Cheng", "Xie Lian"),
                "Grandmaster of Demonic Cultivation": ("Wei Wuxian", "Lan Wangji"),
                "Thousand Autumns": ("Yan Wushi", "Shen Qiao"),
                "Stars of Chaos": ("Gu Yun", "Chang Geng"),
                "Ballad of Sword and Wine": ("Shen Zechuan", "Xiao Chiye"),
                "Peerless": ("Cui Buqu", "Feng Xiao"),
                "Remnants of Filth": ("Gu Mang", "Mo Xi"),
                "The Husky and His White Cat Shizun": ("Mo Ran", "Chu Wanning"),
                "The Scum Villain's Self-Saving System": ("Shen Yuan", "Luo Binghe"),
                "Case File Compendium": ("He Yu", "Xie Qingcheng"),
                "The Disabled Tyrant's Pet Palm Fish": ("Li Yu", "Jing Wang")
                }

# Texte einlesen

def lade_texte(korpus_ordner):
    texte = ""
    for dateiname in os.listdir(korpus_ordner):
        if dateiname.endswith(".txt"):
            with open(os.path.join(korpus_ordner, dateiname), "r", encoding="utf-8") as file:
                texte += file.read().lower() + " "
    return texte

texte = lade_texte(korpus_ordner)
tokens = word_tokenize(texte)
lemmatized_tokens = [lemmatizer.lemmatize(word) for word in tokens if word.isalpha() and word not in stop_words and word not in chinese_syllables]
tagged_words = pos_tag(lemmatized_tokens)

# Wortfrequenzanalyse -> 100 häufigsten Wörter
word_freq = FreqDist(lemmatized_tokens)
most_common_words = word_freq.most_common(100)

# Kollokationsanalyse -> jeweils die 200 häufigsten Bi- oder Trigramme erstellen
bigrams = list(ngrams(lemmatized_tokens, 2))
trigrams = list(ngrams(lemmatized_tokens, 3))
bigram_freq = FreqDist(bigrams).most_common(200)
trigram_freq = FreqDist(trigrams).most_common(200)

# Häufigste Adjektive extrahieren
adjectives = [word for word, pos in tagged_words if pos in ["JJ", "JJR", "JJS"]]
adjective_freq = FreqDist(adjectives).most_common(200)

# Ergebnisse in Excel speichern
with pd.ExcelWriter(output_excel) as writer:
    pd.DataFrame(most_common_words, columns=['Word', 'Frequency']).to_excel(writer, sheet_name='Word Frequency', index=False)
    pd.DataFrame(bigram_freq, columns=['Bigram', 'Frequency']).to_excel(writer, sheet_name='Bigrams', index=False)
    pd.DataFrame(trigram_freq, columns=['Trigram', 'Frequency']).to_excel(writer, sheet_name='Trigrams', index=False)
    pd.DataFrame(adjective_freq, columns=['Adjective', 'Frequency']).to_excel(writer, sheet_name='Adjectives', index=False)

print("DONE! Siehe ", output_excel)
