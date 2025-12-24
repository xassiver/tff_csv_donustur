import csv
import time
import os
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import subprocess

def dogum_tarihi_formatla(dt):
    # "26 Ocak 1998" -> "1998/01/26"
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
        # Oyuncu Adı
        try:
            ad = driver.find_element(By.ID, 'ctl00_MPane_m_30_202_ctnr_m_30_202_OyuncuDisplay1_oyuncuBilgileri_lblAdi').text.strip()
        except:
            ad = ''
        # Doğum Yeri
        try:
            dogum_yeri = driver.find_element(By.ID, 'ctl00_MPane_m_30_202_ctnr_m_30_202_OyuncuDisplay1_oyuncuBilgileri_Label1').text.strip()
        except:
            dogum_yeri = ''
        # Doğum Tarihi
        try:
            dogum_tarihi_raw = driver.find_element(By.ID, 'ctl00_MPane_m_30_202_ctnr_m_30_202_OyuncuDisplay1_oyuncuBilgileri_Label2').text.strip()
            dogum_tarihi = dogum_tarihi_formatla(dogum_tarihi_raw)
        except:
            dogum_tarihi = ''
        # Uyruk
        try:
            uyru_raw = driver.find_element(By.ID, 'ctl00_MPane_m_30_202_ctnr_m_30_202_OyuncuDisplay1_oyuncuBilgileri_Label3').text.strip()
            uyru = uyruk_kodunu_donustur(uyru_raw)
        except:
            uyru = ''
        # Kulüp
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
    print("Oyuncu Bilgisi Çekici - TFF")
    print("1 - Hızlı (önce linkleri gir, sonra hepsini çek)")
    print("2 - Detaylı (her linkte anında veri çek)")
    mod = input("Mod seçin (1/2): ")
    bilgiler = []
    dosya_adi = input("Kaydedilecek dosya adını girin (sadece isim, .csv yazmanıza gerek yok): ")
    if not dosya_adi.endswith('.csv'):
        dosya_adi += '.csv'
    dosya_yolu = f"csv/{dosya_adi}"
    if mod.strip() == "1":
        # Hızlı mod: önce linkleri al, sonra hepsini çek
        linkler = []
        print("Oyuncu linklerini girin. Bitirmek için sadece Enter'a basın.")
        while True:
            link = input("Oyuncu linki: ")
            if link.strip() == "":
                break
            if not link.startswith("http"):
                print("Lütfen tam link girin (https:// ile başlasın)")
                continue
            linkler.append(link)
        print(f"Toplam {len(linkler)} link alındı. Veri çekiliyor...")
        hatali_linkler = []
        toplam = len(linkler)
        for idx, link in enumerate(linkler, 1):
            veri = oyuncu_bilgisi_cek(link)
            bar_len = 30
            dolu = int(bar_len * idx / toplam)
            bos = bar_len - dolu
            print(f"[{('='*dolu)+'>'+(' '*bos)}] {idx}/{toplam}", end='\r')
            if veri:
                bilgiler.append(veri)
            else:
                hatali_linkler.append(link)
        print()
    else:
        # Detaylı mod: her linkte anında veri çek
        print("Oyuncu linkini girin. Bitirmek için sadece Enter'a basın.")
        hatali_linkler = []
        idx = 0
        while True:
            link = input("Oyuncu linki: ")
            if link.strip() == "":
                break
            if not link.startswith("http"):
                print("Lütfen tam link girin (https:// ile başlasın)")
                continue
            idx += 1
            veri = oyuncu_bilgisi_cek(link)
            bar_len = 30
            dolu = int(bar_len * idx / (idx if idx > 0 else 1))
            bos = bar_len - dolu
            print(f"[{('='*dolu)+'>'+(' '*bos)}] {idx}", end='\r')
            if veri:
                bilgiler.append(veri)
            else:
                hatali_linkler.append(link)
        print()
    # Çekilen bilgileri tablo şeklinde göster
    if bilgiler:
        print("\nÇekilen Oyuncu Bilgileri:")
        print(f"{'Ad':<25} {'Doğum Tarihi':<12} {'Uyruk':<6} {'Kulüp':<25} {'Doğum Yeri':<15}")
        print("-"*85)
        for b in bilgiler:
            print(f"{b[0]:<25} {b[1]:<12} {b[2]:<6} {b[3]:<25} {b[4]:<15}")
        with open(dosya_yolu, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Ad", "Doğum Tarihi", "Uyruk", "Kulüp", "Doğum Yeri"])
            writer.writerows(bilgiler)
        print(f"\n{dosya_yolu} kaydedildi.")
    else:
        print("Hiç veri kaydedilmedi.")
    # Özet rapor
    print("\n--- Özet Rapor ---")
    print(f"Toplam oyuncu: {len(bilgiler) + len(hatali_linkler)}")
    print(f"Başarıyla çekilen: {len(bilgiler)}")
    print(f"Hatalı/çekilemeyen: {len(hatali_linkler)}")
    if hatali_linkler:
        print("Hatalı linkler:")
        for l in hatali_linkler:
            print(l)
    else:
        # Detaylı mod: her linkte anında veri çek
        print("Oyuncu linkini girin. Bitirmek için sadece Enter'a basın.")
        while True:
            link = input("Oyuncu linki: ")
            if link.strip() == "":
                break
            if not link.startswith("http"):
                print("Lütfen tam link girin (https:// ile başlasın)")
                continue
            veri = oyuncu_bilgisi_cek(link)
            if veri:
                print(f"Çekilen: {veri}")
                bilgiler.append(veri)
            else:
                print("Veri çekilemedi!")
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
