# Kayıp Eşya API

Kampüste kaybolan ve bulunan eşyaları buluşturan bir web servisi.

## Problem

Kampüste kaybolan eşyalar (cüzdan, telefon, anahtar, öğrenci kartı…) genellikle WhatsApp gruplarında ve panolarda duyuruluyor. Bu mesajlar kısa sürede kayboluyor, eşyayı bulan kişi sahibine ulaşamıyor, eşyasını kaybeden kişi de nereye bakacağını bilmiyor.

## Kimin için?

- **Eşyasını kaybeden öğrenci ve personel:** Kaybettiği eşya için ilan açar, olası eşleşmeleri görür.
- **Bir eşya bulan kişi:** Bulduğu eşyayı kaydeder, eşyanın sahibine ulaşmasına yardım eder.

Kayıp ve bulunan ilanlarını tek bir yerde toplar; kategori, konum ve tarih bilgisine göre eşleştirme önerir.

## İş Takip Panosu

Görevler ve kabul kriterleri GitHub Projects panosunda takip ediliyor:
👉 **[Kayıp Eşya Panosu](PANO_LINKI_BURAYA)**

## Kullanılan Teknolojiler

- Python 3.12, FastAPI, Pydantic
- Pytest (otomatik testler)
- GitHub Codespaces (kurulumsuz çalıştırma)

## Projeyi Çalıştırma

### Seçenek 1: Kurulum yapmadan, tarayıcıda (GitHub Codespaces)

1. Bu repo sayfasında **Code → Codespaces → Create codespace on main** butonuna tıklayın.
2. Ortam kurulduğunda uygulama kendiliğinden başlar ve 8000 portu açılır.
3. Açılan sayfanın adresinin sonuna `/docs` ekleyin.

### Seçenek 2: Kendi bilgisayarınızda

Python 3.10 veya üstü gerekir.

```bash
git clone https://github.com/ahmetyahyay58/DevOps_Proje.git
cd DevOps_Proje
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Tarayıcıda **http://localhost:8000/docs** adresini açın. Tüm uç noktalar bu sayfada **Try it out** butonuyla denenebilir.

## Özellikler

_Geliştirme sürüyor. Tamamlanan özellikler ve nasıl denenecekleri burada listelenecek._
