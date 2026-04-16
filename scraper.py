import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import date, datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "es-ES,es;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

QUERIES = [
    "fotografo Barcelona",
    "videografo Barcelona",
    "editor video Barcelona",
    "tecnico audiovisual Barcelona",
    "produccion audiovisual Barcelona",
]

def scrape_indeed(query):
    ofertas = []
    try:
        q = query.replace(" ", "+")
        url = f"https://es.indeed.com/jobs?q={q}&fromage=1&sort=date&limit=5"
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        cards = soup.select("div.job_seen_beacon")[:3]
        for card in cards:
            titulo = card.select_one("h2.jobTitle span")
            empresa = card.select_one("span.companyName")
            ubicacion = card.select_one("div.companyLocation")
            link_tag = card.select_one("h2.jobTitle a")
            if titulo:
                href = "https://es.indeed.com" + link_tag["href"] if link_tag and link_tag.get("href") else "https://es.indeed.com"
                ofertas.append({
                    "cargo": titulo.get_text(strip=True),
                    "empresa": empresa.get_text(strip=True) if empresa else "No especificada",
                    "ubicacion": ubicacion.get_text(strip=True) if ubicacion else "Barcelona",
                    "portal": "Indeed",
                    "url": href,
                    "fecha": str(date.today())
                })
    except Exception as e:
        print(f"Error Indeed ({query}): {e}")
    return ofertas

def scrape_infojobs(query):
    ofertas = []
    try:
        q = query.replace(" ", "+")
        url = f"https://www.infojobs.net/jobsearch/search-results/list.xhtml?keyword={q}&province=barcelona&sinceDate=_1&orderBy=PUBLICATION_DATE"
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        cards = soup.select("li.ij-OfferList-item")[:3]
        for card in cards:
            titulo = card.select_one("h2 a") or card.select_one("a.ij-OfferList-itemTitle")
            empresa = card.select_one("span.ij-OfferList-itemCompany") or card.select_one("a.ij-OfferList-itemCompany")
            ubicacion = card.select_one("span.ij-OfferList-itemLocation")
            if titulo:
                href = titulo.get("href", "https://www.infojobs.net")
                if not href.startswith("http"):
                    href = "https://www.infojobs.net" + href
                ofertas.append({
                    "cargo": titulo.get_text(strip=True),
                    "empresa": empresa.get_text(strip=True) if empresa else "No especificada",
                    "ubicacion": ubicacion.get_text(strip=True) if ubicacion else "Barcelona",
                    "portal": "InfoJobs",
                    "url": href,
                    "fecha": str(date.today())
                })
    except Exception as e:
        print(f"Error InfoJobs ({query}): {e}")
    return ofertas

def deduplicar(ofertas):
    vistos = set()
    resultado = []
    for o in ofertas:
        key = o["cargo"].lower().strip()[:40]
        if key not in vistos:
            vistos.add(key)
            resultado.append(o)
    return resultado

def main():
    print(f"Iniciando scraping — {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    todas = []

    for query in QUERIES:
        print(f"  Scraping Indeed: {query}")
        todas += scrape_indeed(query)
        print(f"  Scraping InfoJobs: {query}")
        todas += scrape_infojobs(query)

    todas = deduplicar(todas)
    todas = todas[:10]  # máximo 10

    os.makedirs("data", exist_ok=True)

    resultado = {
        "fecha": str(date.today()),
        "actualizado": datetime.now().strftime('%d/%m/%Y · %H:%M'),
        "total": len(todas),
        "ofertas": todas
    }

    with open("data/trabajos.json", "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)

    print(f"Guardadas {len(todas)} ofertas en data/trabajos.json")

    if len(todas) == 0:
        print("AVISO: No se encontraron ofertas nuevas hoy")

if __name__ == "__main__":
    main()

