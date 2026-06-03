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
        # Lista på startsidor som AI:n ska börja läsa från (du kan ändra dessa!)
        self.start_sidor = [
            "https://wikipedia.org",
            "https://wikipedia.org",
            "https://wikipedia.org",
            "https://wikipedia.org"
        ]

    def _rensa_html_och_få_text(self, html_kod):
        """Rensar bort all ful HTML-kod så bara ren text blir kvar."""
        # Ta bort allt inuti <script> och <style> taggar
        clean_text = re.sub(r'<(script|style).*?>.*?</\1>', '', html_kod, flags=re.DOTALL)
        # Ta bort alla vanliga HTML-taggar
        clean_text = re.sub(r'<[^>]*>', ' ', clean_text)
        # Snygga till mellanrum
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

        # Loopa så länge vi har tid kvar och det finns sidor att läsa
        while time.time() - start_tid < sekunder_att_trana:
            if sido_index >= len(self.start_sidor):
                print("[AI] Jag har läst ut alla mina startsidor! Avbryter träningen i förtid.")
                break

            aktuell_url = self.start_sidor[sido_index]
            sido_index += 1
            
            tid_kvar = int(sekunder_att_trana - (time.time() - start_tid))
            print(f"-> Läser: {aktuell_url} ({tid_kvar} sekunder kvar av träningen)")

            try:
                # Surfa till hemsidan och ladda ner innehållet (timeout efter 10 sek så den inte fastnar)
                req = urllib.request.Request(aktuell_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=10) as response:
                    html = response.read().decode('utf-8', errors='ignore')
                
                # Gör om HTML till rena ord
                ren_text = self._rensa_html_och_få_text(html)
                ord_lista = self._tokenisera(ren_text)
                
                if not ord_lista:
                    continue

                # Träna på orden (Ollama-metoden med ID-nummer och vikter)
                for ord in ord_lista:
                    if ord not in self.ord_till_id:
                        nytt_id = len(self.ord_till_id)
                        self.ord_till_id[ord] = nytt_id
                        self.id_till_ord[nytt_id] = ord

                for i in range(len(ord_lista) - self.sammanhang):
                    kontext_ids = tuple(self.ord_till_id[w] for w in ord_lista[i : i + self.sammanhang])
                    nästa_ord_id = self.ord_till_id[ord_lista[i + self.sammanhang]]

                    if kontext_ids not in self.or_db:
                        self.or_db[kontext_ids] = {}
                    self.or_db[kontext_ids][nästa_ord_id] = self.or_db[kontext_ids].get(nästa_ord_id, 0) + 1

                # En liten paus så att hemsidorna inte tror att vi gör en överbelastningsattack
                time.sleep(1)

            except Exception as e:
                print(f"   (Kunde inte läsa sidan på grund av nätverksfel, hoppar över...)")
                continue

        print(f"\n[AI] Träning klar! Jag har memorerat {len(self.ord_till_id)} unika ord och {len(self.or_db)} språkmönster.")

    def _valj_nasta_ord(self, möjliga_val):
        totalt = sum(mojliga_val.values())
        slump = random.uniform(0, totalt)
        summa = 0
        for ord_id, vikt in möjliga_val.items():
            summa += vikt
            if slump <= summa:
                return ord_id
        return list(mojliga_val.keys())[0]

    def generera_svar(self, prompt, max_längd=30):
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

        for _ in range(max_längd):
            if nuvarande_kontext in self.or_db:
                nästa_id = self._valj_nasta_ord(self.or_db[nuvarande_kontext])
                
                # Avbryt om meningen känns klar
                if len(genererade_ids) > 10 and nästa_id in [self.ord_till_id.get('and'), self.ord_till_id.get('the')]:
                    break
                    
                genererade_ids.append(nästa_id)
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

# Fråga användaren hur länge modellen ska träna
svar_tid = input("Hur många minuter vill du träna modellen på internet? (t.ex. 1, 3, 5 eller 10): ")
try:
    valda_minuter = float(svar_tid)
    if valda_minuter <= 0:
        valda_minuter = 1
except:
    print("Felaktigt inmatat värde. Sätter träningstiden till standard: 1 minut.")
    valda_minuter = 1

# Starta internet-inlärningen
ai.dammsug_internet(valda_minuter)

print("\nAI: Nu har jag stängt min internet-dammsugare och sparat allt i minnet!")
print("AI: Testa att fråga mig om 'Newton', 'Python' eller 'Football' (Skriv på engelska då texterna är engelska).")
print("-" * 70)

while True:
    din_fraga = input("\nDu: ")
    if din_fraga.lower() in ['avsluta', 'exit']:
        print("AI: Hejdå! Kul att du lät mig lära känna internet.")
        break
        
    svar = ai.generera_svar(din_fraga)
    print(f"AI: {svar}")
