import time
import csv
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By

def main():
    print("Lig Tablosu Çekici")
    url = input("Tabloyu çekmek istediğiniz sayfa linkini girin: ")
    dosya_adi = input("Kaydedilecek dosya adını girin (sadece isim, .csv yazmanıza gerek yok): ")
    if not dosya_adi.endswith('.csv'):
        dosya_adi += '.csv'
    dosya_yolu = f"csv/{dosya_adi}"
    EDGE_DRIVER_PATH = "msedgedriver.exe"
    service = Service(EDGE_DRIVER_PATH)
    driver = webdriver.Edge(service=service)
    driver.get(url)
    time.sleep(3)
    try:
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        if iframes:
            driver.switch_to.frame(iframes[0])
        tables = driver.find_elements(By.TAG_NAME, "table")
        found = False
        for table in tables:
            rows = table.find_elements(By.TAG_NAME, "tr")
            if not rows:
                continue
            header_cols = rows[0].find_elements(By.TAG_NAME, "th")
            if not header_cols:
                header_cols = rows[0].find_elements(By.TAG_NAME, "td")
            header = [col.text.strip().upper() for col in header_cols]
            if any(h in header for h in ["O", "G", "B", "M", "A", "Y", "AV", "P"]):
                with open(dosya_yolu, "w", newline='', encoding="utf-8") as f:
                    writer = csv.writer(f)
                    for row in rows:
                        cols = row.find_elements(By.TAG_NAME, "td")
                        if not cols:
                            cols = row.find_elements(By.TAG_NAME, "th")
                        writer.writerow([col.text for col in cols])
                print(f"Tablo başarıyla kaydedildi: {dosya_yolu}")
                found = True
                break
        if not found:
            print("Uygun tablo bulunamadı.")
    except Exception as e:
        print("Tablo bulunamadı veya hata oluştu:", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
