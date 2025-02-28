import os
import pandas as pd
import nltk
from nltk import word_tokenize, pos_tag
from collections import Counter
from openpyxl import Workbook
import string

# NLTK-Setup
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Ordnerpfad
korpus_ordner = "seven_seas_txt_korpus cleaned"

# Ausgabe-Excel-Datei
output_excel = "Pronoun_Character_Adjective.xlsx"

# Männliche Pronomen
male_pronouns = {'he', 'him', 'his'}

# Chinesische Silben, die ausgeschlossen werden sollen
# Zweiteilige Wörter usw werden behalten, da ansonsten wertvolle Daten verloren gehen können
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
                "The Scum Villain's Self-Saving System": ("Shen Qingqui", "Luo Binghe"),
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
tokens = [word for word in word_tokenize(texte) if word.isalpha() and word not in chinese_syllables]
tagged_words = pos_tag(tokens)

# Funktion zur Extraktion von Adjektiven
def extract_adj_context(entity_list, tagged_words, window=10):
    adj_contexts = []
    for i in range(len(tagged_words)):
        word, tag = tagged_words[i]
        if word in entity_list:
            window_words = tagged_words[max(0, i - window): min(len(tagged_words), i + window + 1)]
            adj_contexts.extend([adj[0] for adj in window_words if adj[1].startswith('JJ')])
    return Counter(adj_contexts).most_common(50)

# Pronomen-Adjektiv-Kombinationen
pron_adj_freq = extract_adj_context(male_pronouns, tagged_words, window=10)

# Charakter-Adjektiv-Kombinationen
#character_names = {name for pair in protagonists.values() for name in pair}
#char_adj_freq = extract_adj_context(character_names, tagged_words, window=10)

# Ergebnisse in Excel speichern
with pd.ExcelWriter(output_excel) as writer:
    pd.DataFrame(pron_adj_freq, columns=['Adjective', 'Frequency']).to_excel(writer, sheet_name='Pronoun Adjective', index=False)
#   pd.DataFrame(char_adj_freq, columns=['Adjective', 'Frequency']).to_excel(writer, sheet_name='Character Adjective', index=False)

print("Tabelle fertig! Siehe:", output_excel)

