import os
import time
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk

# Ladda ner nödvändiga språkresurser (görs bara första gången)
nltk.download('punkt', quiet=True)

def hämta_wikipedia_text(ämne):
    """Hämtar och rensar text från Wikipedia"""
    url = f"https://en.wikipedia.org/wiki/{ämne}"
    headers = {'User-Agent': 'MinAvanceradeAI/2.0'}
    try:
        respons = requests.get(url, headers=headers)
        if respons.status_code == 200:
            soup = BeautifulSoup(respons.text, 'html.parser')
            # Hämta alla paragrafer och slå ihop dem
            paragrafer = soup.find_all('p')
            text = " ".join([p.text for p in paragrafer if len(p.text) > 20])
            return text
    except Exception:
        return ""
    return ""

# --- HUVUDPROGRAM ---
print("=== VÄLKOMMEN TILL DIN AVANCERADE AI ===")

# Träningsfasen
ämnen = ["Artificial_intelligence", "Machine_learning", "Python_(programming_language)", "Deep_learning", "Data_science"]
print(f"Tillgängliga ämnen för träning: {', '.join(ämnen)}")

try:
    antal_ämnen = int(input("Hur många ämnen vill du att AI:n ska träna på? (1-5): "))
    ämnen_att_träna = ämnen[:antal_ämnen]
except ValueError:
    print("Felaktig inmatning. Tränar på standard (2 ämnen).")
    ämnen_att_träna = ämnen[:2]

print("\n[TRAINING] Startar avancerad träning...")
rå_text = ""

for ämne in ämnen_att_träna:
    print(f" -> Läser in och analyserar: {ämne}...")
    rå_text += hämta_wikipedia_text(ämne) + " "
    time.sleep(1) # Snyggt mot Wikipedias servrar

# Avancerad textbearbetning: Dela upp all text i enskilda meningar
meningar = nltk.sent_tokenize(rå_text)

if len(meningar) < 2:
    print("Kunde inte hämta tillräckligt med data för att träna. Försök igen.")
    exit()

print(f"\n[AI] Träning klar! Memoriserat {len(meningar)} språkliga matriskopplingar.")
print("AI: My brain is ready! Ask me anything based on what I learned (in English).")
print("-" * 60)

# Frågestund med den avancerade algoritmen
while True:
    användar_fråga = input("\nYou: ")
    if användar_fråga.lower() in ['exit', 'quit', 'hejdå']:
        print("AI: Goodbye!")
        break
        
    if not användar_fråga.strip():
        continue

    # Algoritmen (TF-IDF) startar:
    # Den gör om din fråga och alla sparade meningar till matematiska vektorer (koordinater)
    vektoriserare = TfidfVectorizer()
    
    # Vi lägger till din fråga till listan av meningar temporärt för att jämföra
    alla_meningar = meningar + [användar_fråga]
    
    # Tränar upp matrisen på orden
    tfidf_matris = vektoriserare.fit_transform(alla_meningar)
    
    # Cosinussimilaritet: Räknar ut vinkeln mellan din fråga och alla meningar.
    # Ju närmare 1.0, desto bättre matchar meningen din fråga!
    matchnings_poäng = cosine_similarity(tfidf_matris[-1], tfidf_matris[:-1])
    
    # Hitta meningen med högst poäng
    bästa_match_index = matchnings_poäng.argsort()[0][-1]
    högsta_poäng = matchnings_poäng[0][bästa_match_index]
    
    # Om AI:n hittar ett svar med hyfsad matematisk relevans
    if högsta_poäng > 0.1:
        print(f"AI: {meningar[bästa_match_index]}")
    else:
        print("AI: I am sorry, my algorithm could not find a confident answer to that in my training data.")
