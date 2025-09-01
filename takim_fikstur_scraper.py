import time
import csv
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By


def main():
    print("Takım Fikstür Çekici")
    print("\nTFF Fikstür Çekimi Bilgilendirme:")
    print("1. Fikstür sezonunu seçin.")
    print("2. Sezon bölümünün yanında bulunan 'Ara' butonuna tıklayın.")
    print("3. Fikstürün 1. veya 2. sayfasını seçin.")
    print("4. Sonrasında bu uygulamaya dönüp işlemi başlatın ve Enter'a basın.\n")
    url = input("Takım sayfası linkini girin: ")
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
        input_deger = input("Fikstür verisini çekmek için Enter'a basın (iptal için herhangi bir şey yazıp Enter'a basın): ")
        if input_deger.strip() == "":
            rows = driver.find_elements(By.XPATH, '//tr[contains(@class, "GridRow_TFF_Contents") or contains(@class, "GridAltRow_TFF_Contents")]')
            if not rows:
                print("Fikstür satırı bulunamadı.")
            else:
                with open(dosya_yolu, "w", newline='', encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Hafta", "Ev Sahibi", "Skor", "Deplasman", "Tarih", "Organizasyon"])
                    for row in rows:
                        cols = row.find_elements(By.TAG_NAME, "td")
                        if len(cols) >= 6:
                            hafta = cols[0].text.strip()
                            ev_sahibi = cols[1].text.strip()
                            skor = cols[2].text.strip()
                            deplasman = cols[3].text.strip()
                            tarih = cols[4].text.strip()
                            organizasyon = cols[5].text.strip()
                            writer.writerow([hafta, ev_sahibi, skor, deplasman, tarih, organizasyon])
                print(f"Fikstür başarıyla kaydedildi: {dosya_yolu}")
        else:
            print("İşlem iptal edildi.")
    except Exception as e:
        print("Tablo bulunamadı veya hata oluştu:", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
