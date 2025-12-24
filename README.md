[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)
![Downloads](https://img.shields.io/github/downloads/xassiver/tff_csv_donustur/total)
![GitHub Repo stars](https://img.shields.io/github/stars/xassiver/tff_csv_donustur)

# TFF Verilerini CSV’ye Dönüştürme

Bu proje, **TFF (Türkiye Futbol Federasyonu)** sitesinde yer alan bilgileri otomatik olarak çekip **CSV dosyasına dönüştürmek** için hazırlanmıştır.

## 🚀 Nasıl Çalışır?

Projeyi çalıştırmak için tek yapman gereken **`baslat.cmd`** dosyasını çalıştırmaktır.  
Gerekli işlemler otomatik olarak başlatılır.

## 🧰 Gereksinimler

Projeyi çalıştırmadan önce aşağıdaki gereksinimlerin sağlandığından emin ol:

- Bilgisayarında **Python** kurulu olmalı  
- **Microsoft Edge WebDriver** indirilmeli  
- İndirilen **Edge Driver**, `baslat.cmd` dosyasının bulunduğu klasöre konulmalı

## 🌐 Edge Driver İndirme

Edge Driver’ı aşağıdaki bağlantıdan indirebilirsin:

https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

> ⚠️ **Not:** Edge Driver sürümü, bilgisayarındaki Microsoft Edge sürümü ile uyumlu olmalıdır.

## ▶️ Çalıştırma

1. Python’un kurulu olduğundan emin ol  
2. Edge Driver’ı indir ve proje klasörüne koy  
3. `baslat.cmd` dosyasını çift tıklayarak çalıştır  

İşlem tamamlandığında TFF sitesinden çekilen veriler **CSV dosyası** olarak oluşturulur.

## 📄 Çıktı

- Veriler `.csv` formatında kaydedilir  
- CSV dosyası Excel ve benzeri programlarla açılabilir

## 📌 Amaç

- TFF sitesindeki verileri otomatik almak  
- Manuel kopyalama ihtiyacını ortadan kaldırmak  
- Verileri analiz edilebilir CSV formatına dönüştürmek

---

Herhangi bir sorun yaşarsan proje dosyalarını ve Edge Driver sürümünü kontrol etmeyi unutma.
