import os
import time
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk

# FIX: Ladda ner nödvändiga språkresurser (inklusive den saknade punkt_tab)
print("[SYSTEM] Initierar språkmodeller...")
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

def hämta_slumpmässigt_ämne():
    """Hämtar en slumpmässig artikel-titel från engelska Wikipedia via deras API"""
    url = "https://en.wikipedia.org/w/api.php?action=query&list=random&rnnamespace=0&format=json&rnlimit=1"
    headers = {'User-Agent': 'MinAvanceradeAI/2.0'}
    try:
        respons = requests.get(url, headers=headers)
        if respons.status_code == 200:
            data = respons.json()
            titel = data['query']['random'][0]['title']
            # Ersätt mellanslag med understreck för URL:en
            return titel.replace(" ", "_")
    except Exception:
        pass
    return "Artificial_intelligence" # Fallback om API:et strular

def hämta_wikipedia_text(ämne):
    """Hämtar och rensar hela texten från en specifik Wikipedia-sida"""
    url = f"https://en.wikipedia.org/wiki/{ämne}"
    headers = {'User-Agent': 'MinAvanceradeAI/2.0'}
    try:
        respons = requests.get(url, headers=headers)
        if respons.status_code == 200:
            soup = BeautifulSoup(respons.text, 'html.parser')
            # Hämta alla paragrafer och slå ihop dem till en stor textmassa
            paragrafer = soup.find_all('p')
            text = " ".join([p.text for p in paragrafer if len(p.text) > 20])
            return text, respons.headers.get('Content-Length', len(respons.content))
    except Exception:
        return "", 0
    return "", 0

# --- HUVUDPROGRAM ---
print("\n=== VÄLKOMMEN TILL DIN AVANCERADE AI ===")

try:
    minuter = float(input("Hur länge vill du att AI:n ska träna och läsa från Wikipedia? (t.ex. 1, 2 eller 5 minuter): "))
    sekunder_att_köra = minuter * 60
except ValueError:
    print("Felaktig inmatning. Tränar i standard (1 minut).")
    sekunder_att_köra = 60

print(f"\n[TRAINING] Startar avancerad träning över hela Wikipedia i {minuter} minut(er)...")
rå_text = ""
start_tid = time.time()
antal_sidor = 0

# Loopar runt och läser nya, slumpmässiga sidor tills tiden är ute
while time.time() - start_tid < sekunder_att_köra:
    återstående_tid = int(sekunder_att_köra - (time.time() - start_tid))
    aktivt_ämne = hämta_slumpmässigt_ämne()
    
    print(f"\n[LOADING URL] -> https://en.wikipedia.org/wiki/{aktivt_ämne} ({återstående_tid} seconds remaining)")
    
    artikel_text, bytes_hämtat = hämta_wikipedia_text(aktivt_ämne)
    
    if artikel_text.strip():
        antal_ord = len(artikel_text.split())
        print(f"  [SUCCESS] Successfully downloaded {bytes_hämtat} bytes of data.")
        print(f"  [TRAINING] Reading {antal_ord} words of pure article text...")
        print(f"  [PREVIEW] First words read: '{artikel_text[:80].strip()}...'")
        
        rå_text += artikel_text + " "
        antal_sidor += 1
    else:
        print("  [SKIP] Kunde inte hämta text från denna sida, hoppar till nästa...")
        
    time.sleep(2) # Paus i 2 sekunder för att vara snäll mot Wikipedias servrar

# Avancerad textbearbetning: Dela upp all insamlad text i enskilda meningar
print("\n[AI] Bearbetar insamlad data och bygger språkmatris...")
meningar = nltk.sent_tokenize(rå_text)

if len(meningar) < 2:
    print("Kunde inte hämta tillräckligt med data för att träna. Kör programmet igen och ge den mer tid!")
    exit()

# Räkna unika ord för att visa i loggen
unika_ord = len(set(rå_text.lower().split()))

print(f"\n=== [AI] Training finished! ===")
print(f"Memorized {unika_ord} unique words and {len(meningar)} language matrix connections from {antal_sidor} articles.")
print("\nAI: My brain is ready! Let's talk in English.")
print("-" * 60)

# Frågestund med den avancerade algoritmen (TF-IDF & Cosine Similarity)
while True:
    användar_fråga = input("\nYou: ")
    if användar_fråga.lower() in ['exit', 'quit', 'hejdå', 'bye']:
        print("AI: Goodbye!")
        break
        
    if not användar_fråga.strip():
        continue

    # Bygg TF-IDF vektorer
    vektoriserare = TfidfVectorizer()
    alla_meningar = meningar + [användar_fråga]
    
    try:
        tfidf_matris = vektoriserare.fit_transform(alla_meningar)
        
        # Räkna ut likheten mellan frågan och alla sparade meningar
        matchnings_poäng = cosine_similarity(tfidf_matris[-1], tfidf_matris[:-1])
        
        bästa_match_index = matchnings_poäng.argsort()[0][-1]
        högsta_poäng = matchnings_poäng[0][bästa_match_index]
        
        # Skriv ut svaret om det är matematiskt relevant
        if högsta_poäng > 0.15:
            print(f"AI: {meningar[bästa_match_index]}")
        else:
            print("AI: I am sorry, my algorithm could not find a confident answer to that in my training data.")
    except Exception:
        print("AI: Something went wrong while calculating the mathematical answer. Try another question!")
