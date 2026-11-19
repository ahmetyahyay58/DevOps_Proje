# Kayıp Eşya API

Kampüste kaybolan ve bulunan eşyaları buluşturan bir web servisi.

> **Hızlıca denemek için:** [Projeyi Çalıştırma](#projeyi-çalıştırma) bölümündeki **Open in GitHub Codespaces** butonuna tıklayın; kurulum gerekmez.

## Problem

Kampüste kaybolan eşyalar (cüzdan, telefon, anahtar, öğrenci kartı…) genellikle WhatsApp gruplarında ve panolarda duyuruluyor. Bu mesajlar kısa sürede kayboluyor, eşyayı bulan kişi sahibine ulaşamıyor, eşyasını kaybeden kişi de nereye bakacağını bilmiyor.

## Kimin için?

- **Eşyasını kaybeden öğrenci ve personel:** Kaybettiği eşya için ilan açar, olası eşleşmeleri görür.
- **Bir eşya bulan kişi:** Bulduğu eşyayı kaydeder, eşyanın sahibine ulaşmasına yardım eder.

Kayıp ve bulunan ilanlarını tek bir yerde toplar; kategori, konum ve tarih bilgisine göre eşleştirme önerir.

## İş Takip Panosu

Görevler ve kabul kriterleri GitHub Projects panosunda takip ediliyor:
👉 **[Kayıp Eşya Panosu](https://github.com/users/ahmetyahyay58/projects/1)**

## Kullanılan Teknolojiler

- Python 3.12, FastAPI, Pydantic
- HTML, CSS ve JavaScript (ek kütüphane ya da derleme adımı olmayan tek sayfalık arayüz)
- Pytest (otomatik testler)
- GitHub Codespaces + Dev Container (kurulumsuz çalıştırma; geliştirme ortamı `.devcontainer/devcontainer.json` dosyasında kod olarak tanımlı, herkes aynı ortamı alır)

## Projeyi Çalıştırma

### Seçenek 1: Kurulum yapmadan, tarayıcıda (önerilen)

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/ahmetyahyay58/DevOps_Proje?quickstart=1)

1. Yukarıdaki butona tıklayın, açılan sayfada **Create codespace**'e basın.
2. 2–3 dakika bekleyin. Kurulum bitince uygulama, ekranın içinde kendiliğinden açılır.

Uygulamayı ayrı bir sekmede tam ekran görmek isterseniz, açılan önizleme panelinin sağ üstündeki **Tarayıcıda aç** simgesine tıklayın. API dokümantasyonu için adresin sonuna `/docs` ekleyin.

### Seçenek 2: Kendi bilgisayarınızda

Python 3.10 veya üstü gerekir.

```bash
git clone https://github.com/ahmetyahyay58/DevOps_Proje.git
cd DevOps_Proje
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Tarayıcıda **http://localhost:8000** adresini açın: uygulamanın web arayüzü görünür. API dokümantasyonu **http://localhost:8000/docs** adresindedir; tüm uç noktalar orada **Try it out** butonuyla denenebilir.

> **Not:** Windows'ta 8000 portu için `WinError 10013` hatası alırsanız başka bir port kullanın:
> `python -m uvicorn app.main:app --reload --port 8080` → http://localhost:8080

### Örnek veriler

Uygulama her açıldığında 6 örnek ilanla başlar (2 kayıp, 4 bulunan). Böylece hiçbir veri girmeden eşleştirme denenebilir. Veriler bellekte tutulur; uygulama yeniden başlatılınca örnek verilere döner.

## Özellikler

| # | Özellik | Durum |
|---|---|---|
| 1 | Kayıp / bulunan eşya ilanı oluşturma | ✅ Tamamlandı |
| 2 | Kayıp ve bulunan ilanları otomatik eşleştirme | ✅ Tamamlandı |

Ayrıca bu iki özelliği tarayıcıdan kullanmayı sağlayan bir **web arayüzü** eklendi (aşağıda).

### Özellik 1: Kayıp / bulunan eşya ilanı oluşturma

Kullanıcı kaybettiği ya da bulduğu bir eşya için ilan açar. İlanda tür (`kayip` / `bulundu`), kategori, açıklama, konum ve tarih bulunur.

**Uç noktalar**

| Yöntem | Adres | Açıklama |
|---|---|---|
| `POST` | `/ilanlar` | Yeni ilan oluşturur |
| `GET` | `/ilanlar` | İlanları listeler (`?tur=kayip` veya `?tur=bulundu` ile filtrelenir) |
| `GET` | `/ilanlar/{id}` | Tek bir ilanı getirir |

Geçerli kategoriler: `cuzdan`, `telefon`, `anahtar`, `kimlik_kart`, `canta`, `elektronik`, `kiyafet`, `diger`

**Nasıl denenir?** (`/docs` sayfasında)

1. `POST /ilanlar` → **Try it out** → aşağıdaki gövdeyi yapıştırıp **Execute**'a basın:
   ```json
   {
     "tur": "kayip",
     "kategori": "cuzdan",
     "aciklama": "Kahverengi deri cüzdan, içinde öğrenci kartı var",
     "konum": "Kütüphane",
     "tarih": "2026-11-15"
   }
   ```
   **Beklenen:** `201` yanıtı ve yeni bir `id` içeren ilan (örnek veriler 1–6 numaraları kullandığı için ilk yeni ilan `7` olur).
2. Aynı şekilde `"tur": "bulundu"` olan ikinci bir ilan ekleyin.
3. `GET /ilanlar` → **Execute**: eklediğiniz ilanlar örnek ilanlarla birlikte listelenir. `tur` alanına `bulundu` yazarsanız yalnızca bulunan ilanları görürsünüz.
4. **Hatalı girişler** (hepsi `422` döner):
   - `"kategori": "uzay_gemisi"` → geçersiz kategori
   - `kategori` alanını silmek → zorunlu alan eksik
   - `"tarih"` olarak yarının tarihi → gelecek tarihli ilan açılamaz

### Özellik 2: Kayıp ve bulunan ilanları otomatik eşleştirme

Bir ilan için karşı türdeki ilanlar taranır (kayıp ilanı için bulunanlar, bulunan ilanı için kayıplar) ve olası eşleşmeler **uyum puanına** göre sıralanır.

**Puanlama (en fazla 100)**

| Kural | Etkisi |
|---|---|
| Kategori aynı değil | Önerilmez |
| Eşya kaybolmadan önce bulunmuş görünüyor | Önerilmez |
| Kategori aynı | 50 puan |
| Konum aynı (büyük/küçük harf fark etmez) | +30 puan |
| Tarih yakınlığı | Aynı gün +20, her gün farkı için −2 (en az 0) |

**Uç nokta**

| Yöntem | Adres | Açıklama |
|---|---|---|
| `GET` | `/ilanlar/{id}/eslesmeler` | İlan için önerilen eşleşmeleri puanıyla birlikte listeler |

**Nasıl denenir?** (`/docs` sayfasında, hiçbir veri girmeden)

1. `GET /ilanlar/{ilan_id}/eslesmeler` → **Try it out** → `ilan_id` = **1** → **Execute**
   **Beklenen:** 1 numaralı ilan (Kütüphane'de kaybolan kahverengi cüzdan) için iki öneri:
   - **98 puan** — Kütüphane'de bulunan kahverengi cüzdan (aynı kategori + aynı konum + 1 gün fark)
   - **66 puan** — Mühendislik Fakültesi'nde bulunan siyah cüzdan (aynı kategori, farklı konum)
   - 6 numaralı cüzdan **önerilmez**, çünkü eşya kaybolmadan önce bulunmuş görünüyor.
2. `ilan_id` = **2** ile deneyin (kayıp telefon) → **boş liste `[]`**, çünkü bulunan ilanlar arasında telefon yok.
3. `ilan_id` = **3** ile deneyin (bulunan cüzdan) → ters yönde de çalışır: 1 numaralı kayıp ilanı önerilir.
4. Kendi senaryonuz: `POST /ilanlar` ile bir `bulundu` ilanı ekleyin (`"kategori": "telefon"`, `"konum": "Yemekhane"`, bugünün tarihi), sonra tekrar `ilan_id` = **2** ile eşleşmelere bakın → yeni ilan yüksek puanla çıkar.

### Web arayüzü

Ana sayfada (`/`) iki özelliği tarayıcıdan kullanmayı sağlayan bir arayüz bulunur:

- **İlan oluşturma formu:** Kaybettim/Buldum seçimi, kategori, açıklama, konum ve tarih. Hatalı girişlerde API'nin hata mesajı formun altında gösterilir.
- **İlan listesi:** Tümü / Kayıp / Bulundu filtreleri.
- **Eşleşme paneli:** Bir ilanda **Eşleşmeleri gör** butonuna basınca olası eşleşmeler puan çubuğu ve *Güçlü / Olası / Zayıf* etiketiyle listelenir. Yeni ilan yayınlanınca eşleşmeleri kendiliğinden açılır.

**Nasıl denenir?**
1. Ana sayfada listenin en altındaki **Kahverengi deri cüzdan** (#1, KAYIP) kartında **Eşleşmeleri gör**'e basın → 98 ve 66 puanlı iki öneri görünür.
2. Formda **Buldum** seçin, kategori **Telefon**, konum **Yemekhane**, bugünün tarihiyle bir ilan yayınlayın → eşleşme paneli açılır ve 2 numaralı kayıp telefon yüksek puanla önerilir.
3. Açıklamayı yalnızca boşluklardan oluşacak şekilde girip yayınlamayı deneyin → *Bu alan boş bırakılamaz* hatası görünür.

## Geliştirme Süreci

Her görev panoda bir karta (GitHub issue) karşılık gelir ve kendi branch'inde geliştirilir. Kabul kriterleri testlerle doğrulandıktan sonra pull request açılır; PR açıklamasındaki `Closes #<issue>` ifadesi PR'ı karta bağlar ve merge edildiğinde kartı **Tamamlandı** sütununa taşır.

| Görev | Branch | Pull request |
|---|---|---|
| [#1 İlan oluşturma](https://github.com/ahmetyahyay58/DevOps_Proje/issues/1) | `feature/1-ilan-olusturma` | [PR #7](https://github.com/ahmetyahyay58/DevOps_Proje/pull/7) |
| [#2 Otomatik eşleştirme](https://github.com/ahmetyahyay58/DevOps_Proje/issues/2) | `feature/2-eslestirme` | [PR #8](https://github.com/ahmetyahyay58/DevOps_Proje/pull/8) |
| Web arayüzü (ek) | `feature/web-arayuzu` | [PR #9](https://github.com/ahmetyahyay58/DevOps_Proje/pull/9) |

## Testler

Kabul kriterlerinin her biri otomatik testlerle doğrulanır:

```bash
python -m pytest -v
```

| Test dosyası | Doğruladığı görev |
|---|---|
| `tests/test_ilan_olusturma.py` | #1 İlan oluşturma |
| `tests/test_eslestirme.py` | #2 Otomatik eşleştirme |
| `tests/test_arayuz.py` | Web arayüzü |
