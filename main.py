import requests


def find_legal_form(code, codebook):
    for item in codebook:
        if item["kod"] == code:
            return item["nazev"]


headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
}

data = '{"kodCiselniku": "PravniForma", "zdrojCiselniku": "res"}'
response = requests.post("https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ciselniky-nazevniky/vyhledat",
                         headers=headers, data=data)
codebook = response.json()["ciselniky"][0]["polozkyCiselniku"]


if __name__ == "__main__":
    while True:
        input_text = input("Zadejte IČO nebo název subjektu, který chcete vyhledat "
                        "(nebo zadejte 'exit' pro ukončení programu): ")

        if input_text.lower() == "exit":
            break

        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }

        # Odstranění mezer při zadávání IČO uživatelem
        input_text_strip = input_text.replace(" ", "")

        # Kontrola, zda uživatelský vstup je číslo a má délku 8 znaků
        if input_text_strip.isdigit() and len(input_text_strip) == 8:
            ico = input_text_strip
            url = f"https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/{ico}"
            response = requests.get(url)
            data = response.json()

            if "obchodniJmeno" in data:
                obchodni_jmeno = data["obchodniJmeno"]
                adresa = data["sidlo"].get("textovaAdresa", "Adresa není k dispozici")
                print("\n")
                print(obchodni_jmeno)
                print(adresa)
                print("-" * 120)
            else:
                print("Subjekt s uvedeným IČO nebyl nalezen!")
        else:
            data = {"obchodniJmeno": input_text}
            response = requests.post("https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/vyhledat",
                                    headers=headers, json=data)
            data = response.json()

            if "pocetCelkem" in data:
                print("\n")
                print(f"Bylo nalezeno {data['pocetCelkem']} subjektů!")
                print("\n")

                for subject in data["ekonomickeSubjekty"]:
                    legal_form_code = subject.get("pravniForma")
                    if legal_form_code:
                        legal_form = find_legal_form(legal_form_code, codebook)
                    else:
                        # pokud neexistuje klíč 'právníForma', pak se vytvoří proměnná 'legal_form' s defaultní hodnotou
                        legal_form = "Neznámá právní forma"

                    # pokud neexistuje klíč 'ico', pak se vytvoří proměnná 'ico' s defaultní hodnotou
                    ico = subject.get("ico", "IČO není uvedeno")
                    print(f"{subject.get('obchodniJmeno', 'Název není uveden')}, IČO: {ico}, právní forma: "
                        f"{legal_form[0]['nazev']}")
                    print("-" * 120)
            else:
                print("Dle zadaného názvu nebyly nalezeny žádné subjekty!")
        print("\n")
