import json
import requests
from bs4 import BeautifulSoup
import os
import sqlite3 as sq
from BD.create_bd import db_start, db_close, add_recept

# import lxml

url = "https://eda.ru/"

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
}


req = requests.get(url, headers=headers).text
soup = BeautifulSoup(req, "lxml")


def del_num(text):
    rtrn = ''
    for i in text:
        if not i.isdigit():
            rtrn += i
    return rtrn

# Запись основных категорий
def all_cat_json():
    name_href_cat = {}
    all_categories = soup.find_all("div", class_="emotion-1t90gdf")
    for item in all_categories:
        try:
            cat_href = item.find("div", class_="emotion-w5dos9").find("a").get("href")
            cat_name = item.find("h3", class_="emotion-pkdp36").text.replace(' ', '_')
            name_href_cat[del_num(cat_name)] = "https://eda.ru" + cat_href
        except Exception as ex:
            print(ex)
    print(name_href_cat)

    with open("Data/all_categories.json", "w", encoding="utf-8") as file:
        json.dump(name_href_cat, file, indent=4, ensure_ascii=False)


# Запись подкатегорий категорий
def all_subcate_json():
    all_subcategories = soup.find_all("div", class_="emotion-1t90gdf")
    for item in all_subcategories:
        name_href_cubcat = {}
        try:
            name_file = del_num(item.find("h3", class_="emotion-pkdp36").text.replace(' ', '_'))
            subcate_teg = item.find_all("div", class_="emotion-8asrz1")
            for item in subcate_teg:
                subcate_name = del_num(item.find("span", class_="emotion-e9xsk4").text)
                subcate_href = item.find("a").get("href")
                name_href_cubcat[subcate_name] = "https://eda.ru" + subcate_href
            print(name_file, name_href_cubcat)
            with open(f"Data/subcategories_{name_file}.json", "w", encoding="utf-8") as file:
                json.dump(name_href_cubcat, file, indent=4, ensure_ascii=False)
        except Exception as ex:
            print(ex)


# Запись ссыдлок на рецепт и названий блюд
def post_href_recept_bd():
    db = sq.connect('BD/recrpts.db')
    cur = db.cursor()
    files_data = os.listdir("Data")

    for item in files_data:

        name_table = str(item).replace("subcategories_", "").replace(".json", "")
        # db_start(name_table)
        print(f"\nЗаполнение таблицы <{name_table}>\n")

        with open(f"Data/{item}", encoding="utf-8") as file:
            files_subcate = json.load(file)

            for k, href_subcate in files_subcate.items():

                name_subcate = str(k)
                req = requests.get(href_subcate, headers=headers).text
                soup = BeautifulSoup(req, "lxml")
                all_count = soup.find("span", class_="emotion-1jdotsv").text.replace("Найдено ", "").replace("Найден ", "").replace(" рецептов", "").replace(" рецепта", "").replace(" рецепт", "")
                print(f"\nЗаполнение подкатегории <{name_subcate}> таблицы <{name_table}>")
                print(f"Количество рецептов в этой категории: {all_count}\n")
                all_count = round(int(all_count) / 13 + 1)

                for i in range(1, all_count):

                    try:
                        req = requests.get(href_subcate + f"?page={i}", headers=headers).text
                        soup = BeautifulSoup(req, "lxml")

                        all_recept = soup.find_all("div", class_="emotion-m0u77r")

                        for it in all_recept:

                            recept_name = it.find("div", class_="emotion-1eugp2w").find("span", class_="emotion-1pdj9vu").text
                            recept_href = "https://eda.ru" + it.find("div", class_="emotion-1eugp2w").find("a").get("href")
                            print(f"{recept_name} : {recept_href}")
                            recept_data = (name_subcate, recept_name, recept_href)
                            print(recept_data)
                            add_recept(name_table, recept_data)
                            db.commit()

                    except Exception as ex:
                        print(ex)


if __name__ == "__main__":

    post_href_recept_bd()
    db_close()
