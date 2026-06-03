import math
import random
import re
import time
import urllib.request

class InternetLaddadAI:
    def __init__(self, sammanhang=2):
        self.sammanhang = sammanhang
        self.or_db = {}
        self.ord_till_id = {}
        self.id_till_ord = {}
        # Vi använder fullständiga Wikipedia-länkar så att den hittar riktig text
        self.start_sidor = [
            "https://wikipedia.org",
            "https://wikipedia.org",
            "https://wikipedia.org",
            "https://wikipedia.org"
        ]

    def _rensa_html_och_fa_text(self, html_kod):
        """Rensar bort all HTML-kod så bara ren text blir kvar."""
        clean_text = re.sub(r'<(script|style).*?>.*?</\1>', '', html_kod, flags=re.DOTALL)
        clean_text = re.sub(r'<[^>]*>', ' ', clean_text)
        clean_text = re.sub(r'\s+', ' ', clean_text)
        return clean_text

    def _tokenisera(self, text):
        return re.findall(r'\b\w+\b', text.lower())

    def dammsug_internet(self, minuter):
        """AI:n surfar på internet under exakt den tid du valt och lär sig ord."""
        sekunder_att_trana = minuter * 60
        start_tid = time.time()
        sido_index = 0
        
        print(f"\n[AI] Startar internet-dammsugning! Jag kommer att läsa i {minuter} minuter...")
        print("-" * 65)

        while time.time() - start_tid < sekunder_att_trana:
            if sido_index >= len(self.start_sidor):
                # Om vi kör slut på sidor lägger vi till några fler automatiskt
                self.start_sidor.append("https://wikipedia.org")
                self.start_sidor.append("https://wikipedia.org")

            aktuell_url = self.start_sidor[sido_index]
            sido_index += 1
            
            tid_kvar = int(sekunder_att_trana - (time.time() - start_tid))
            print(f"-> Läser: {aktuell_url} ({tid_kvar} sekunder kvar)")

            try:
                # FIX: Vi skickar med en mer realistisk webbläsar-id (User-Agent) så Wikipedia tillåter oss att läsa
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }
                req = urllib.request.Request(aktuell_url, headers=headers)
                with urllib.request.urlopen(req, timeout=10) as response:
                    html = response.read().decode('utf-8', errors='ignore')
                
                ren_text = self._rensa_html_och_fa_text(html)
                ord_lista = self._tokenisera(ren_text)
                
                if len(ord_lista) < 50: # Hoppa över trasiga eller tomma sidor
                    continue

                for ord in ord_lista:
                    if ord not in self.ord_till_id:
                        nytt_id = len(self.ord_till_id)
                        self.ord_till_id[ord] = nytt_id
                        self.id_till_ord[nytt_id] = ord

                for i in range(len(ord_lista) - self.sammanhang):
                    kontext_ids = tuple(self.ord_till_id[w] for w in ord_lista[i : i + self.sammanhang])
                    naesta_ord_id = self.ord_till_id[ord_lista[i + self.sammanhang]]

                    if kontext_ids not in self.or_db:
                        self.or_db[kontext_ids] = {}
                    self.or_db[kontext_ids][naesta_ord_id] = self.or_db[kontext_ids].get(naesta_ord_id, 0) + 1

                # Vänta 2 sekunder mellan varje sida så vi är schyssta mot servrarna
                time.sleep(2)

            except Exception as e:
                continue

        print(f"\n[AI] Träning klar! Jag har memorerat {len(self.ord_till_id)} unika ord och {len(self.or_db)} språkmönster.")

    def _valj_nasta_ord(self, mojliga_val):
        """FIXAT: Inga konstiga svenska tecken i variabelnamnen längre."""
        totalt = sum(mojliga_val.values())
        slump = random.uniform(0, totalt)
        summa = 0
        for ord_id, vikt in mojliga_val.items():
            summa += vikt
            if slump <= summa:
                return ord_id
        return list(mojliga_val.keys())[0]

    def generera_svar(self, prompt, max_laengd=25):
        prompt_ord = self._tokenisera(prompt)
        kända_ids = [self.ord_till_id[w] for w in prompt_ord if w in self.ord_till_id]

        if len(kända_ids) < self.sammanhang:
            if not self.or_db:
                return "Mitt minne är tomt. Du lät mig inte träna på internet!"
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

# --- STARTA PROGRAMMET ---
ai = InternetLaddadAI(sammanhang=2)

print("=" * 70)
print(" VÄLKOMMEN TILL DIN INTERNET-TRÄNADE AI FROM SCRATCH")
print("=" * 70)

svar_tid = input("Hur många minuter vill du träna modellen på internet? (t.ex. 1, 3 eller 5): ")
try:
    valda_minuter = float(svar_tid)
    if valda_minuter <= 0:
        valda_minuter = 1
except:
    valda_minuter = 1

# Starta internet-inlärningen
ai.dammsug_internet(valda_minuter)

print("\nAI: Nu har jag stängt min internet-dammsugare och sparat allt i minnet!")
print("AI: Skriv något på engelska som rör de sidor jag besökt.")
print("-" * 70)

while True:
    din_fraga = input("\nDu: ")
    if din_fraga.lower() in ['avsluta', 'exit']:
        print("AI: Hejdå!")
        break
        
    svar = ai.generera_svar(din_fraga)
    print(f"AI: {svar}")
