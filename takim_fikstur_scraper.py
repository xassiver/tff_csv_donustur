import time
import csv
import os
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options

def get_match_links(driver):
    # Fikstür tablosundaki maç linklerini (skor hücresindeki href) toplar
    links = []
    rows = driver.find_elements(By.XPATH, '//tr[contains(@class, "GridRow_TFF_Contents") or contains(@class, "GridAltRow_TFF_Contents")]')
    for row in rows:
        try:
            skor_a = row.find_element(By.XPATH, './/td[3]/a')
            href = skor_a.get_attribute('href')
            if href and href.startswith('http'):
                links.append(href)
        except:
            continue
    return links

def get_match_details(driver, url, fields):
    driver.get(url)
    time.sleep(2)
    result = {}
    if 'stadyum' in fields or 'sehir' in fields:
        try:
            stadyum_full = driver.find_element(By.ID, 'ctl00_MPane_m_29_194_ctnr_m_29_194_MacBilgiDisplay1_dtMacBilgisi_lnkStad').text.strip()
            if 'stadyum' in fields:
                result['stadyum'] = stadyum_full.split('-')[0].strip() if '-' in stadyum_full else stadyum_full
            if 'sehir' in fields:
                if '-' in stadyum_full:
                    result['sehir'] = stadyum_full.split('-')[1].strip()
                else:
                    result['sehir'] = ''
        except:
            if 'stadyum' in fields:
                result['stadyum'] = ''
            if 'sehir' in fields:
                result['sehir'] = ''
    if 'ev_takim' in fields:
        try:
            result['ev_takim'] = driver.find_element(By.ID, 'ctl00_MPane_m_29_194_ctnr_m_29_194_MacBilgiDisplay1_dtMacBilgisi_lnkTakim1').text.strip()
        except:
            result['ev_takim'] = ''
    if 'deplasman_takim' in fields:
        try:
            result['deplasman_takim'] = driver.find_element(By.ID, 'ctl00_MPane_m_29_194_ctnr_m_29_194_MacBilgiDisplay1_dtMacBilgisi_lnkTakim2').text.strip()
        except:
            result['deplasman_takim'] = ''
    if 'tarih_saat' in fields:
        try:
            result['tarih_saat'] = driver.find_element(By.ID, 'ctl00_MPane_m_29_194_ctnr_m_29_194_MacBilgiDisplay1_dtMacBilgisi_lblTarih').text.strip()
        except:
            result['tarih_saat'] = ''
    if 'organizasyon' in fields:
        try:
            result['organizasyon'] = driver.find_element(By.ID, 'ctl00_MPane_m_29_194_ctnr_m_29_194_MacBilgiDisplay1_dtMacBilgisi_lblOrganizasyonAdi').text.strip()
        except:
            result['organizasyon'] = ''
    if 'hakemler' in fields:
        hakemler = []
        try:
            hakem_divs = driver.find_elements(By.CSS_SELECTOR, '.dtMacBilgisiHakemler div')
            for div in hakem_divs:
                hakemler.append(div.text.strip())
        except:
            pass
        result['hakemler'] = ', '.join(hakemler)
    if 'gozlemci' in fields:
        try:
            result['gozlemci'] = driver.find_element(By.CSS_SELECTOR, '.dtMacBilgisiGozlemciler div').text.strip()
        except:
            result['gozlemci'] = ''
    if 'temsilci' in fields:
        try:
            result['temsilci'] = driver.find_element(By.CSS_SELECTOR, '.dtMacBilgisiTemsilciler div').text.strip()
        except:
            result['temsilci'] = ''
    return result

def main():
    print("Takım Fikstür Detaylı Çekici (Yeni)")
    print("1 - Tek sayfa fikstür çek")
    print("2 - İki sayfa fikstür çek (her sayfa için Enter'a bas)")
    secim = input("Seçiminizi girin (1/2): ").strip()
    url = input("Takım fikstür sayfası linkini girin: ")
    dosya_adi = input("Kaydedilecek dosya adını girin (sadece isim, .csv yazmanıza gerek yok): ")
    if not dosya_adi.endswith('.csv'):
        dosya_adi += '.csv'
    dosya_yolu = f"csv/{dosya_adi}"
    EDGE_DRIVER_PATH = "msedgedriver.exe"
    alanlar = [
        ('stadyum', 'Stadyum'),
        ('sehir', 'Şehir'),
        ('ev_takim', 'Ev Sahibi Takım'),
        ('deplasman_takim', 'Deplasman Takım'),
        ('tarih_saat', 'Tarih/Saat'),
        ('organizasyon', 'Organizasyon'),
        ('hakemler', 'Hakemler'),
        ('gozlemci', 'Gözlemci'),
        ('temsilci', 'Temsilci')
    ]
    print("\nÇekilecek bilgileri seçin (numaraları virgülle ayırın):")
    for i, (_, label) in enumerate(alanlar, 1):
        print(f"{i}. {label}")
    secim_str = input("Örnek: 1,2,4\nSeçiminiz: ")
    secimler = [int(s) for s in secim_str.replace(' ', '').split(',') if s.isdigit() and 1 <= int(s) <= len(alanlar)]
    fields = [alanlar[i-1][0] for i in secimler]
    fikstur_links = []
    if secim == "2":
        for sayfa_no in [1, 2]:
            service = Service(EDGE_DRIVER_PATH)
            driver = webdriver.Edge(service=service)
            driver.get(url)
            print(f"{sayfa_no}. sayfa için TFF sitesinde 'Ara' butonuna tıklayın ve Enter'a basın...")
            input(f"{sayfa_no}. sayfa hazırsa Enter'a basın: ")
            time.sleep(2)
            links = get_match_links(driver)
            fikstur_links.extend(links)
            driver.quit()
    else:
        service = Service(EDGE_DRIVER_PATH)
        driver = webdriver.Edge(service=service)
        driver.get(url)
        print("Tek sayfa için TFF sitesinde 'Ara' butonuna tıklayın ve Enter'a basın...")
        input("Sayfa hazırsa Enter'a basın: ")
        time.sleep(2)
        fikstur_links = get_match_links(driver)
        driver.quit()
    print(f"Toplam {len(fikstur_links)} maç linki bulundu. Detaylar çekiliyor...")
    bilgiler = []
    service = Service(EDGE_DRIVER_PATH)
    driver = webdriver.Edge(service=service)
    toplam = len(fikstur_links)
    for idx, link in enumerate(fikstur_links, 1):
        detay = get_match_details(driver, link, fields)
        bilgiler.append([detay.get(f, '') for f in fields])
        bar_len = 30
        dolu = int(bar_len * idx / toplam)
        bos = bar_len - dolu
        print(f"[{('='*dolu)+'>'+(' '*bos)}] {idx}/{toplam}", end='\r')
    driver.quit()
    print()
    # Tabloyu göster
    print("\nÇekilen Maç Detayları:")
    print(' | '.join([alanlar[[a[0] for a in alanlar].index(f)][1] for f in fields]))
    print("-"*120)
    for b in bilgiler:
        print(' | '.join(b))
    # CSV kaydet
    with open(dosya_yolu, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([alanlar[[a[0] for a in alanlar].index(f)][1] for f in fields])
        writer.writerows(bilgiler)
    print(f"\n{dosya_yolu} kaydedildi.")
    print("\n--- Özet Rapor ---")
    print(f"Toplam maç: {toplam}")
    print(f"Başarıyla çekilen: {len(bilgiler)}")

if __name__ == "__main__":
    main()
