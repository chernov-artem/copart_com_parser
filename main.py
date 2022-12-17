''' С фриланса.
Описание задания:
Есть сайт https://copart.com
Парсер собирает все лоты машин с главной страницы(12 шт),
открывает каждый лот и сохраняет оттуда 1, 3, 5 и 7 фото,
а также название лота, пробег и наличие повреждений.
Фото сохраняются в папку "Cars" в папке проэкта, остальные данные
сохраняются в текстовом файле в этой же папке.
'''
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time
import requests
import os

options = webdriver.ChromeOptions()

# disable webdriver mode
options.add_argument("--disable-blink-features=AutomationControlled")

# user agent
my_user_agent = "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727)"
options.add_argument(f"user-agent={my_user_agent}")
driver = webdriver.Chrome(executable_path='Chrom/chromedriver.exe', options=options)

url = 'https://www.copart.com'
# указываем нужное количество страниц для парсинга. (2 машины на страницу)
pages = 6

def card():
    driver.implicitly_wait(6)
    try:
        driver.implicitly_wait(13)
        car_name = driver.find_element(By.XPATH, '//*[@id="lot-details"]/div/div[1]/div/div/div[1]/div[1]/h1')
        car_odometr = driver.find_element(By.XPATH,
                                          '//*[@id="lot-details"]/div/div[2]/div/div/div[1]/div[1]/div[1]/div[2]/div[1]/div/div[1]/div[1]/div/div[4]/div/span/p')
        car_damage = driver.find_element(By.XPATH,
                                         '//*[@id="lot-details"]/div/div[2]/div/div/div[1]/div[1]/div[1]/div[2]/div[1]/div/div[1]/div[1]/div/div[9]/span')
        print(car_name.text, car_odometr.text, car_damage.text)
        ft1 = driver.find_element(By.XPATH, '//*[@id="show-img"]')  # foto 1
        list_foto = []
        foto1 = ft1.get_attribute('src')
        list_foto.append(foto1)  # добавляем foto1 в список фотографий
        roll = driver.find_elements(By.CLASS_NAME, "thumbImgblock")  # находим последовательность фотографий
        time.sleep(1)
        roll[2].click()  # кликаем по foto3
        ft3 = driver.find_element(By.XPATH, '//*[@id="show-img"]')  # foto 3
        foto3 = ft3.get_attribute('src')
        list_foto.append(foto3)
        time.sleep(1)
        roll[4].click()
        ft5 = driver.find_element(By.XPATH, '//*[@id="show-img"]')  # foto 5
        foto5 = ft5.get_attribute('src')
        list_foto.append(foto5)
        time.sleep(1)
        roll[6].click()
        ft7 = driver.find_element(By.XPATH, '//*[@id="show-img"]')  # foto 7
        foto7 = ft7.get_attribute('src')
        list_foto.append(foto7)
        time.sleep(1)
        # сохраняем фото
        for i in range(len(list_foto)):
            with open(f'Cars/{car_name.text}_foto{i + 1}.png', "wb+") as foto:
                foto.write(requests.get(list_foto[i]).content)
        with open("Cars/cars_info.txt", "a") as file:
            file.write(f"{car_name.text};{car_odometr.text};{car_damage.text}\n")
    except NoSuchElementException:
        print('элемент не найден!')


def main():
    # Создаем папку Cars
    if not os.path.isdir("Cars"):
        os.makedirs('Cars')
    try:
        driver.get(url)
        driver.implicitly_wait(7)
        list = []
        # Добавляем нужное количество страниц(по 2 машины) в список
        for i in range(pages):
            item1 = driver.find_element(By.XPATH,
                                        '//*[@id="Search Rec Engine"]/div/div/div/div/div/recommendation-engine/div/div/div/div/span/span[1]/span/div/div[2]/div[2]/div[1]/a')
            link1 = item1.get_attribute("href")
            list.append(link1)
            item2 = driver.find_element(By.XPATH,
                                        '//*[@id="Search Rec Engine"]/div/div/div/div/div/recommendation-engine/div/div/div/div/span/span[2]/span/div/div[2]/div[2]/div[1]/a')
            link2 = item2.get_attribute("href")
            btn_next = driver.find_element(By.XPATH,
                                           '//*[@id="Search Rec Engine"]/div/div/div/div/div/recommendation-engine/div/div/div/div/div/span/span[3]')
            list.append(link2)
            time.sleep(3)
            btn_next.click()

        foto1 = list[0]
        for i in list:
            driver.get(i)
            driver.implicitly_wait(5)
            card()

    except Exception as ex:
        print(ex)

    finally:
        driver.close()
        driver.quit()


if __name__ == '__main__':
    main()
