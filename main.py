import subprocess
import sys

print(r"""
 ___    ___ ________  ________  ________  ________     
|\  \  /  /|\   __  \|\   ____\|\   __  \|\   ____\    
      
\ \  \/  / | \  \|\  \ \  \___|\ \  \|\  \ \  \___|    
 \ \    / / \ \   __  \ \_____  \ \   __  \ \  \       
  /     \/   \ \  \ \  \|____|\  \ \  \ \  \ \  \____  
 /  /\   \    \ \__\ \__\____\_\  \ \__\ \__\ \_______\
/__/ /\ __\    \|__|\|__|\_________\|__|\|__|\|_______|
|__|/ \|__|             \|_________|                   
""")
print("XASAC tarafından yapılmıştır | XASAC: https://xasac.com.tr\n")
input("Devam etmek için ENTER'a basın...")

print("Ana Menü\n")
print("1 - Takım Fikstürü Çek: Bir takımın fikstürünü çekmek için takım sayfa linkini girersiniz, tüm maçları ve tarihleri CSV'ye kaydeder.")
print("2 - Lig Tablosu Çek: Herhangi bir lig tablosu için istediğiniz sayfa linkini girersiniz, puan durumu ve sıralama CSV'ye kaydedilir.")
print("3 - Takım Kadrosu Çek: Takım kadrosu sayfası linkini girersiniz, tüm oyuncu isimleri CSV'ye kaydedilir.")
print("4 - Oyuncu Bilgisi Çek (Link ile): Oyuncu profil linklerini girersiniz, doğum tarihi, uyruk, kulüp ve doğum yeri bilgileri CSV'ye kaydedilir.")
secim = input("Lütfen bir seçenek girin (1/2/3/4): ")

if secim.strip() == "1":
    subprocess.run([sys.executable, "takim_fikstur_scraper.py"])
elif secim.strip() == "2":
    subprocess.run([sys.executable, "lig_tablosu_scraper.py"])
elif secim.strip() == "3":
    subprocess.run([sys.executable, "takim_kadro_scraper.py"])
elif secim.strip() == "4":
    subprocess.run([sys.executable, "oyuncu_bilgi_scraper.py"])
else:
    print("Geçersiz seçim. Lütfen 1, 2, 3 veya 4 girin.")
