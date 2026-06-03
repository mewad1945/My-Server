import math
import random
import re
import time
import urllib.request

class UltimataInternetAIn:
    def __init__(self, sammanhang=2):
        self.sammanhang = sammanhang
        self.or_db = {}
        self.ord_till_id = {}
        self.id_till_ord = {}
        
        # De exakta engelska Wikipedia-sidorna som AI:n ska läsa från
        self.start_sidor = [
            "https://wikipedia.org",
            "https://wikipedia.org",
            "https://wikipedia.org",
            "https://wikipedia.org"
        ]

    def _rensa_wikipedia_html(self, html_kod):
        """Kastar bort menyer, språklister och sparar ENDAST brödtexten."""
        # 1. Hitta blocket där själva artikeln ligger
        artikel_block = re.findall(r'<div id="bodyContent".*?>.*?</div>', html_kod, flags=re.DOTALL)
        if artikel_block:
            html_kod = "".join(artikel_block)
            
        # 2. Ta bort donationsbanderoller, menyer och skräp
        html_kod = re.sub(r'<div class="noprint".*?>.*?</div>', '', html_kod, flags=re.DOTALL)
        html_kod = re.sub(r'<style.*?>.*?</style>', '', html_kod, flags=re.DOTALL)
        html_kod = re.sub(r'<script.*?>.*?</script>', '', html_kod, flags=re.DOTALL)
        
        # 3. Gör om till ren text och rensa dubbla mellanslag
        ren_text = re.sub(r'<[^>]*>', ' ', html_kod)
        ren_text = re.sub(r'\s+', ' ', ren_text)
        return ren_text.strip()

    def _tokenisera(self, text):
        return re.findall(r'\b\w+\b', text.lower())

    def dammsug_internet(self, minuter):
        """Surfar på nätet under den valda tiden och visar exakt vad den gör."""
        sekunder_att_trana = minuter * 60
        start_tid = time.time()
        sido_index = 0
        
        print(f"\n[AI] Starting internet training for {minuter} minutes...")
        print("=" * 75)

        while time.time() - start_tid < sekunder_att_trana:
            if sido_index >= len(self.start_sidor):
                print("[AI] Out of target pages! Adding historical science and technology pages...")
                self.start_sidor.append("https://wikipedia.org")
                self.start_sidor.append("https://wikipedia.org")
                self.start_sidor.append("https://wikipedia.org")

            aktuell_url = self.start_sidor[sido_index]
            sido_index += 1
            
            tid_kvar = int(sekunder_att_trana - (time.time() - start_tid))
            print(f"\n[LOADING URL] -> {aktuell_url} ({tid_kvar} seconds remaining)")

            try:
                # Skicka med en User-Agent så Wikipedia ser att vi är en riktig webbläsare
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                req = urllib.request.Request(aktuell_url, headers=headers)
                
                with urllib.request.urlopen(req, timeout=10) as response:
                    html = response.read().decode('utf-8', errors='ignore')
                
                # Rensa och räkna orden
                ren_text = self._rensa_wikipedia_html(html)
                ord_lista = self._tokenisera(ren_text)
                
                if len(ord_lista) < 100:
                    print("   [INFO] Page was too short or empty, skipping...")
                    continue

                # KRAV: Skriv ut exakt vad AI:n läser till konsolen
                print(f"   [SUCCESS] Successfully downloaded {len(html)} bytes of data.")
                print(f"   [TRAINING] Reading {len(ord_lista)} words of pure article text...")
                print(f"   [PREVIEW] First words read: '{' '.join(ord_lista[:12])}...'")

                # Indexera orden (Ollama-metoden)
                for ord in ord_lista:
                    if ord not in self.ord_till_id:
                        nytt_id = len(self.ord_till_id)
                        self.ord_till_id[ord] = nytt_id
                        self.id_till_ord[nytt_id] = ord

                # Bygg de matematiska kopplingarna
                for i in range(len(ord_lista) - self.sammanhang):
                    kontext_ids = tuple(self.ord_till_id[w] for w in ord_lista[i : i + self.sammanhang])
                    naesta_ord_id = self.ord_till_id[ord_lista[i + self.sammanhang]]

                    if kontext_ids not in self.or_db:
                        self.or_db[kontext_ids] = {}
                    self.or_db[kontext_ids][naesta_ord_id] = self.or_db[kontext_ids].get(naesta_ord_id, 0) + 1

                # Vänta 2 sekunder så vi inte överbelastar Wikipedia
                time.sleep(2)

            except Exception as e:
                print(f"   [ERROR] Could not read page due to network limits.")
                continue

        print("=" * 75)
        print(f"[AI] Training finished! Memorized {len(self.ord_till_id)} unique words and {len(self.or_db)} language matrix connections.")

    def _valj_nasta_ord(self, mojliga_val):
        totalt = sum(mojliga_val.values())
        slump = random.uniform(0, totalt)
        summa = 0
        for ord_id, vikt in mojliga_val.items():
            summa += vikt
            if slump <= summa:
                return ord_id
        return list(mojliga_val.keys())

    def generera_svar(self, prompt, max_laengd=25):
        prompt_ord = self._tokenisera(prompt)
        
        # Chatt-hälsningar hanteras direkt så den inte läser menyer
        halsningar = ['hello', 'hi', 'hey', 'tjena', 'hallå']
        if any(h in prompt_ord for h in halsningar):
            return "Hello! I am your local AI. I have successfully analyzed the Wikipedia pages. Ask me about Newton, Python, or Football!"

        kända_ids = [self.ord_till_id[w] for w in prompt_ord if w in self.ord_till_id]

        if len(kända_ids) < self.sammanhang:
            if not self.or_db:
                return "My memory is empty. You did not let me train!"
            nuvarande_kontext = random.choice(list(self.or_db.keys()))
        else:
            nuvarande_kontext = tuple(kända_ids[-self.sammanhang:])
            if nuvarande_kontext not in self.or_db:
                matchningar = [k for k in self.or_db.keys() if kända_ids[-1] in k]
                nuvarande_kontext = random.choice(matchningar) if matchningar else random.choice(list(self.or_db.keys()))

        genererade_ids = list(nuvarande_kontext)

        for _ in range(max_laengd):
            if nuvarande_kontext in self.or_db:
                naesta_id = self._valj_nasta_ord(self.or_db[nuvarande_kontext])
                genererade_ids.append(naesta_id)
                nuvarande_kontext = tuple(genererade_ids[-self.sammanhang:])
            else:
                break

        svar_ord = [self.id_till_ord[oid] for oid in genererade_ids]
        return " ".join(svar_ord).capitalize() + "."

# --- KÖR PROGRAMMET ---
ai = UltimataInternetAIn(sammanhang=2)

print("=" * 75)
print("             REAL-TIME INTERNET LEARNING MODEL FROM SCRATCH")
print("=" * 75)

svar_tid = input("How many minutes do you want the AI to learn from Wikipedia? (e.g. 1, 2 or 5): ")
try:
    valda_minuter = float(svar_tid)
    if valda_minuter <= 0: valda_minuter = 1
except:
    valda_minuter = 1

# Starta dammsugningen på riktigt
ai.dammsug_internet(valda_minuter)

print("\nAI: My brain is ready! Let's talk in English.")
print("-" * 75)

while True:
    din_fraga = input("\nYou: ")
    if din_fraga.lower() in ['avsluta', 'exit', 'quit']:
        print("AI: Goodbye!")
        break
        
    svar = ai.generera_svar(din_fraga)
    print(f"AI: {svar}")
