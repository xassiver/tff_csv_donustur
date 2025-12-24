import time
import csv
import os
import subprocess
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options

def main():
    print("Lig Tablosu Çekici")
    url = input("Tabloyu çekmek istediğiniz sayfa linkini girin: ")
    dosya_adi = input("Kaydedilecek dosya adını girin (sadece isim, .csv yazmanıza gerek yok): ")
    if not dosya_adi.endswith('.csv'):
        dosya_adi += '.csv'
    dosya_yolu = f"csv/{dosya_adi}"
    
    # WebDriver'ı başlat
    service = Service('msedgedriver.exe')
    options = Options()
    options.add_argument('--headless')
    try:
        driver = webdriver.Edge(service=service, options=options)
    except Exception as e:
        print(f"Edge WebDriver başlatılamadı: {e}")
        return None
    
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
                tablo = []
                toplam = len(rows)
                for idx, row in enumerate(rows, 1):
                    cols = row.find_elements(By.TAG_NAME, "td")
                    if not cols:
                        cols = row.find_elements(By.TAG_NAME, "th")
                    tablo.append([col.text for col in cols])
                    # İlerleme barı
                    bar_len = 30
                    dolu = int(bar_len * idx / toplam)
                    bos = bar_len - dolu
                    print(f"[{('='*dolu)+'>'+(' '*bos)}] {idx}/{toplam}", end='\r')
                print() # Son ilerleme barı satırı
                # Tablo şeklinde göster
                print("\nÇekilen Lig Tablosu:")
                for t in tablo:
                    print(" | ".join(t))
                with open(dosya_yolu, "w", newline='', encoding="utf-8") as f:
                    writer = csv.writer(f)
                    for t in tablo:
                        writer.writerow(t)
                print(f"\n{dosya_yolu} kaydedildi.")
                # Özet rapor
                print("\n--- Özet Rapor ---")
                print(f"Toplam satır: {toplam}")
                print(f"Başarıyla çekilen: {len(tablo)}")
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
