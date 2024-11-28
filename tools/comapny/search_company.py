import requests
from bs4 import BeautifulSoup
import json

# Заголовки запроса
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

#функция которая по ОГРН формирует ссылку с нужными реквизитами
def generate_requisites_url(base_url, ogrn):
    initial_url = f"{base_url}{ogrn}"
    response = requests.get(initial_url, headers=headers, allow_redirects=True)

    if response.status_code == 200:
        # Получаем фактический URL после редиректа
        final_url = response.url
        # Добавляем /requisites для получения ссылки с реквизитами
        requisites_url = f"{final_url}/requisites"
        return requisites_url
    else:
        raise Exception(f"Ошибка при запросе URL: {response.status_code}")

#функция для получения данных о компании с страницы сайта с реквизитами
def fetch_requisites(ogrn):
    base_url = "https://zachestnyibiznes.ru/company/ul/"
    url = generate_requisites_url(base_url, ogrn)

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        data = {}

        # Ищем юридический адрес
        rekv2 = soup.find("div", id="rekv2")
        if rekv2:
            text = rekv2.get_text(separator="\n", strip=True)
            lines = text.split("\n")

            # Извлекаем название компании (первая строка)
            if len(lines) > 0:
                data["CompanyName"] = lines[0].strip()

            # Извлекаем юридический адрес
            for line in lines:
                if "Юридический адрес" in line:
                    data["address"] = line.replace("Юридический адрес:", "").strip()
                    break

        # Ищем поля по ключам
        fields = {
            "OGRN": "ОГРН",
            "INN": "ИНН",
            "KPP": "КПП",
            "OKPO": "ОКПО",
            "OKATO": "ОКАТО",
            "OKTMO": "ОКТМО",
            "OKOGU": "ОКОГУ",
            "OKOPF": "ОКОПФ",
            "OKFS": "ОКФС"
        }

        rows = soup.find_all("div", class_="row m-b-10")
        for row in rows:
            label = row.find("div", class_="col-md-6 sub-title-content")
            value = row.find("div", class_="col-md-6 text-content")
            if label and value:
                label_text = label.get_text(strip=True).split("&")[0].strip()
                value_text = value.get_text(strip=True)
                for key, field_name in fields.items():
                    if field_name in label_text:
                        data[key] = value_text
                        break

        return data
    else:
        raise Exception(f"Ошибка при запросе страницы: {response.status_code}")



#ogrn = "1027739405540" #пример входных данных

#функция которую надо вызывать для извлечения данных, принимает на вход ОГРН
def get_info(ogrn):
    company_data = fetch_requisites(ogrn)
    # Сохраняем в JSON
    with open("company_data.json", "w", encoding="utf-8") as f:
        json.dump(company_data, f, ensure_ascii=False, indent=4)
