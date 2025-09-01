import time
import csv
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options


def dogum_tarihi_formatla(dt):
    aylar = {
        "Ocak": "01", "Şubat": "02", "Mart": "03", "Nisan": "04", "Mayıs": "05", "Haziran": "06",
        "Temmuz": "07", "Ağustos": "08", "Eylül": "09", "Ekim": "10", "Kasım": "11", "Aralık": "12"
    }
    try:
        parcalar = dt.split()
        if len(parcalar) == 3:
            gun = parcalar[0].zfill(2)
            ay = aylar.get(parcalar[1], "00")
            yil = parcalar[2]
            return f"{yil}/{ay}/{gun}"
        else:
            return dt
    except:
        return dt


def uyruk_kodunu_donustur(uyruk):
    uyruk = uyruk.strip().upper()
    if uyruk == "TC":
        return "tur"
    return uyruk.lower()


def oyuncu_bilgisi_cek(url):
    service = Service('msedgedriver.exe')
    options = Options()
    options.add_argument('--headless')
    try:
        driver = webdriver.Edge(service=service, options=options)
    except Exception as e:
        print(f"Edge WebDriver başlatılamadı: {e}")
        return None
    try:
        driver.get(url)
        time.sleep(2)
        try:
            ad = driver.find_element(By.ID, 'ctl00_MPane_m_30_202_ctnr_m_30_202_OyuncuDisplay1_oyuncuBilgileri_lblAdi').text.strip()
        except:
            ad = ''
        try:
            dogum_yeri = driver.find_element(By.ID, 'ctl00_MPane_m_30_202_ctnr_m_30_202_OyuncuDisplay1_oyuncuBilgileri_Label1').text.strip()
        except:
            dogum_yeri = ''
        try:
            dogum_tarihi_raw = driver.find_element(By.ID, 'ctl00_MPane_m_30_202_ctnr_m_30_202_OyuncuDisplay1_oyuncuBilgileri_Label2').text.strip()
            dogum_tarihi = dogum_tarihi_formatla(dogum_tarihi_raw)
        except:
            dogum_tarihi = ''
        try:
            uyru_raw = driver.find_element(By.ID, 'ctl00_MPane_m_30_202_ctnr_m_30_202_OyuncuDisplay1_oyuncuBilgileri_Label3').text.strip()
            uyru = uyruk_kodunu_donustur(uyru_raw)
        except:
            uyru = ''
        try:
            kulup = driver.find_element(By.ID, 'ctl00_MPane_m_30_202_ctnr_m_30_202_OyuncuDisplay1_oyuncuBilgileri_oyuncuLisansBilgileri_Label5').text.strip()
        except:
            kulup = ''
        driver.quit()
        return [ad, dogum_tarihi, uyru, kulup, dogum_yeri]
    except Exception as e:
        print(f"Oyuncu bilgisi çekiminde hata: {e}")
        driver.quit()
        return None


def main():
    print("Takım Kadro Bilgisi Çekici (Otomatik)")
    print("\nTFF Kadro Çekimi Bilgilendirme:")
    print("1. Kadro sezonunu seçin.")
    print("2. Kadro sezonu bölümünün yanında bulunan 'Ara' butonuna tıklayın.")
    print("3. Sonrasında bu uygulamaya dönüp işlemi başlatın ve Enter'a basın.\n")
    url = input("Takım kadro sayfası linkini girin: ")
    dosya_adi = input("Kaydedilecek dosya adını girin (sadece isim, .csv yazmanıza gerek yok): ")
    if not dosya_adi.endswith('.csv'):
        dosya_adi += '.csv'
    dosya_yolu = f"csv/{dosya_adi}"
    EDGE_DRIVER_PATH = "msedgedriver.exe"
    service = Service(EDGE_DRIVER_PATH)
    driver = webdriver.Edge(service=service)
    driver.get(url)
    time.sleep(3)
    input("Kadro sezonunu seçip 'Ara' butonuna tıkladıktan sonra Enter'a basın...")
    print("Oyuncu linkleri toplanıyor...")
    oyuncu_linkleri = []
    try:
        rows = driver.find_elements(By.XPATH, '//tr[contains(@class, "GridRow_TFF_Contents") or contains(@class, "GridAltRow_TFF_Contents")]')
        for row in rows:
            try:
                td = row.find_element(By.TAG_NAME, "td")
                a = td.find_element(By.TAG_NAME, "a")
                link = a.get_attribute("href")
                if link and link.startswith("http"):
                    oyuncu_linkleri.append(link)
            except:
                continue
    except Exception as e:
        print(f"Oyuncu linkleri alınamadı: {e}")
    driver.quit()
    print(f"Toplam {len(oyuncu_linkleri)} oyuncu linki bulundu. Bilgiler çekiliyor...")
    bilgiler = []
    for link in oyuncu_linkleri:
        veri = oyuncu_bilgisi_cek(link)
        if veri:
            print(f"Çekilen: {veri}")
            bilgiler.append(veri)
        else:
            print(f"Veri çekilemedi! {link}")
    if bilgiler:
        with open(dosya_yolu, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Ad", "Doğum Tarihi", "Uyruk", "Kulüp", "Doğum Yeri"])
            writer.writerows(bilgiler)
        print(f"{dosya_yolu} kaydedildi.")
    else:
        print("Hiç veri kaydedilmedi.")

if __name__ == "__main__":
    main()
