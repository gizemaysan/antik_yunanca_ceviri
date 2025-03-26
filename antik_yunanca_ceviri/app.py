import sqlite3
import re
import requests
from collections import Counter
from deep_translator import GoogleTranslator

# Veri tabanı oluşturma

def create_db():
    conn = sqlite3.connect("greek_dictionary.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS greek_words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT UNIQUE,
            translation TEXT
        )
    """)
    conn.commit()
    conn.close()

# Yeni kelimeleri veritabanına ekleme

def insert_word(word, translation):
    conn = sqlite3.connect("greek_dictionary.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO greek_words (word, translation) VALUES (?, ?)", (word, translation))
    conn.commit()
    conn.close()

# Veritabanında kelimenin olup olmadığını kontrol etme

def translate_from_db(word):
    conn = sqlite3.connect("greek_dictionary.db")
    cursor = conn.cursor()
    cursor.execute("SELECT translation FROM greek_words WHERE word = ?", (word,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

# Google Translate ile çeviri

def translate_google(word, source_lang="el", target_lang="en"):
    try:
        return GoogleTranslator(source=source_lang, target=target_lang).translate(word)
    except:
        return "Translation not found."

# Antik Yunanca metni temizleme ve ayrıştırma

def tokenize_text(text):
    text = re.sub(r"[^α-ωΑ-Ωάέήίόύώϊϋΐΰ]", " ", text)  
    words = text.lower().split()
    return words

# Frekans analizi yapma

def analyze_text(text):
    words = tokenize_text(text)
    word_counts = Counter(words)
    return word_counts

# Main fonksiyon

def process_text(text):
    word_counts = analyze_text(text)
    results = {}
    
    for word, count in word_counts.items():
        translation = translate_from_db(word)
        if not translation:
            translation = translate_google(word)
            insert_word(word, translation)
        
        results[word] = {"count": count, "translation": translation}
    
    return results

user_input = input("Lütfen Antik Yunanca bir metin girin: ")

# Metni analiz etme
results = process_text(user_input)

# Analiz Sonucu Yazdırma
for word, data in results.items():
    print(f"Kelime: {word}, Frekans: {data['count']}, Çeviri: {data['translation']}")
