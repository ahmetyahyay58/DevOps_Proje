# Kayıp Eşya

Kampüste kaybolan ve bulunan eşyaları buluşturan bir web uygulaması.

## Problem

Kampüste kaybolan eşyalar (cüzdan, telefon, anahtar, öğrenci kartı…) genellikle WhatsApp gruplarında ve panolarda duyuruluyor. Bu mesajlar kısa sürede kayboluyor, eşyayı bulan kişi sahibine ulaşamıyor, eşyasını kaybeden kişi de nereye bakacağını bilmiyor.

## Kimin için?

- **Eşyasını kaybeden öğrenci ve personel:** Kaybettiği eşya için ilan açar, olası eşleşmeleri görür.
- **Bir eşya bulan kişi:** Bulduğu eşyayı kaydeder, eşyanın sahibine ulaşmasına yardım eder.

Uygulama kayıp ve bulunan ilanlarını tek bir yerde toplar; kategori, konum ve tarih bilgisine göre eşleştirme önerir.

## İş Takip Panosu

Görevler ve kabul kriterleri GitHub Projects panosunda takip ediliyor:
👉 **[Kayıp Eşya Panosu](https://github.com/users/ahmetyahyay58/projects/1)**

Panodaki görevlerden **#1 İlan oluşturma** ve **#2 Otomatik eşleştirme** geliştirilip tamamlandı.

## Projeyi Çalıştırma

### Seçenek 1: Kendi bilgisayarınızda

Python 3.10 veya üstü ve Git gerekir. Terminalde sırayla çalıştırın:

```bash
git clone https://github.com/ahmetyahyay58/DevOps_Proje.git
cd DevOps_Proje
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Terminalde `Application startup complete` yazınca uygulama hazırdır. Açmak için:

- Terminaldeki **`http://127.0.0.1:8000`** linkine `Ctrl` tuşuna basılı tutarak tıklayın, **ya da**
- Tarayıcıda **http://127.0.0.1:8000** adresini açın.

> **Windows'ta `WinError 10013` hatası alırsanız** 8000 portu başka bir uygulama tarafından kullanılıyordur. Başka bir port seçin:
> `python -m uvicorn app.main:app --reload --port 8080` → **http://127.0.0.1:8080**

Uygulamayı durdurmak için terminalde `Ctrl + C`.

### Seçenek 2: Kurulum yapmadan, tarayıcıda (GitHub Codespaces)

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/ahmetyahyay58/DevOps_Proje?quickstart=1)

1. Yukarıdaki butona tıklayın, açılan sayfada **Create codespace**'e basın.
2. 2–3 dakika bekleyin. Kurulum bitince uygulama kendiliğinden başlar ve ekranın sağında bir önizleme panelinde açılır.
3. Önizleme açılmazsa ya da uygulamayı ayrı bir sekmede görmek isterseniz, alttaki terminalde **`http://0.0.0.0:8000`** linkine `Ctrl` tuşuna basılı tutarak tıklayın.

Geliştirme ortamı `.devcontainer/devcontainer.json` dosyasında tanımlıdır; Codespaces bu dosyayı okuyarak Python'u, bağımlılıkları ve uygulamayı kendisi kurup başlatır.

## Örnek Veriler

Uygulama her açıldığında aşağıdaki 6 ilanla başlar, böylece hiçbir veri girmeden denenebilir. Tarihler uygulamanın açıldığı güne göre hesaplanır. Veriler bellekte tutulur; uygulama yeniden başlatılınca bu hâline döner.

| # | Tür | Kategori | Açıklama | Konum | Tarih |
|---|---|---|---|---|---|
| 1 | KAYIP | Cüzdan | Kahverengi deri cüzdan, içinde öğrenci kartı var | Kütüphane | 3 gün önce |
| 2 | KAYIP | Telefon | Siyah telefon, kırık ekran koruyuculu | Yemekhane | 2 gün önce |
| 3 | BULUNDU | Cüzdan | Kahverengi cüzdan bulundu, danışmaya teslim edildi | Kütüphane | 2 gün önce |
| 4 | BULUNDU | Cüzdan | Siyah cüzdan, kantinin yanında | Mühendislik Fakültesi | 1 gün önce |
| 5 | BULUNDU | Anahtar | Mavi anahtarlıklı ev anahtarı | Yemekhane | 1 gün önce |
| 6 | BULUNDU | Cüzdan | Küçük bozuk para cüzdanı | Kütüphane | 5 gün önce |

## Özellikleri Deneme

Uygulama açıldığında ana sayfada solda **Yeni ilan** formu, sağda **İlanlar** listesi görünür. Aşağıdaki adımlar uygulama ilk açıldığı hâliyle (yalnızca örnek verilerle) yazılmıştır.

> #1 ve #2 uygulamanın arka ucunda (API) geliştirildi. Ana sayfadaki arayüz, bu iki özelliği tarayıcıdan kolayca denemek için sonradan eklendi ([PR #9](https://github.com/ahmetyahyay58/DevOps_Proje/pull/9)).

### Özellik 1: Kayıp / bulunan eşya ilanı oluşturma ([#1](https://github.com/ahmetyahyay58/DevOps_Proje/issues/1))

Kullanıcı kaybettiği ya da bulduğu bir eşya için ilan açar ve ilanları türüne göre listeleyebilir.

**Nasıl denenir?**

1. **Yeni ilan** formunda **Buldum**'u seçin. Kategori: **Telefon**, Açıklama: `Siyah telefon, kılıfı yok`, Konum: **Yemekhane**. Tarih bugünün tarihiyle dolu gelir.
2. **İlanı yayınla**'ya basın → formun altında *"İlan #7 yayınlandı."* yazar, ilan listenin en üstünde **#7** numarasıyla görünür. (Sağdan açılan eşleşme panelini şimdilik kapatabilirsiniz; Özellik 2'de kullanacağız.)
3. Listenin üstündeki **Kayıp** / **Bulundu** / **Tümü** sekmelerine tıklayın → liste seçilen türe göre filtrelenir.
4. Açıklama kutusuna yalnızca birkaç boşluk yazıp, konuma `Kantin` yazarak yayınlamayı deneyin → *"Bu alan boş bırakılamaz"* hatası görünür, ilan oluşmaz.
5. Tarih alanında yarının tarihini seçmeyi deneyin → takvim bugünden sonraki günleri seçtirmez.

**Kabul kriterleri ve nasıl görüleceği**

| Kabul kriteri | Arayüzde nasıl görülür |
|---|---|
| Tür, kategori, açıklama, konum ve tarih bilgisiyle ilan oluşturulabiliyor ve sistem ilana bir ID veriyor | Adım 1–2: ilan yayınlanır ve **#7** numarasını alır |
| Zorunlu alan eksikse ya da kategori geçersizse hata dönüyor | Adım 4: boş açıklama reddedilir. Kategori listeden seçildiği için geçersiz kategori girilemez |
| Tüm ilanlar listelenebiliyor ve türe göre filtrelenebiliyor | Adım 3: sekmelerle filtreleme |
| Gelecek tarihli ilan oluşturulamıyor | Adım 5: takvim gelecek tarihi seçtirmez; sunucu da bu tarihi reddeder |

### Özellik 2: Kayıp ve bulunan ilanları otomatik eşleştirme ([#2](https://github.com/ahmetyahyay58/DevOps_Proje/issues/2))

Bir ilan için karşı türdeki ilanlar taranır (kayıp ilanı için bulunanlar, bulunan ilanı için kayıplar) ve olası eşleşmeler **uyum puanına** göre sıralanır.

**Puanlama (en fazla 100)**

| Kural | Etkisi |
|---|---|
| Kategori farklı | Önerilmez |
| Eşya kaybolmadan önce bulunmuş görünüyor | Önerilmez |
| Kategori aynı | 50 puan |
| Konum aynı (büyük/küçük harf fark etmez) | +30 puan |
| Tarih yakınlığı | Aynı gün +20, her gün farkı için −2 (en az 0) |

Arayüzde 80 ve üstü puan **Güçlü**, 60–79 **Olası**, 60'ın altı **Zayıf** eşleşme olarak etiketlenir.

**Nasıl denenir?**

1. Listenin en altındaki **#1 Kahverengi deri cüzdan** (KAYIP) kartında **Eşleşmeleri gör**'e basın → sağda bir panel açılır:
   - **98 · Güçlü eşleşme:** #3 Kütüphane'de bulunan kahverengi cüzdan (aynı kategori + aynı konum + 1 gün fark)
   - **66 · Olası eşleşme:** #4 Mühendislik Fakültesi'nde bulunan siyah cüzdan (aynı kategori, farklı konum)
   - #6 Küçük bozuk para cüzdanı **önerilmez**: aynı kategori ve aynı konumda olsa da eşya kaybolmadan önce bulunmuş görünüyor.
2. Paneli kapatıp **#2 Siyah telefon** (KAYIP) kartında **Eşleşmeleri gör**'e basın → *"Şu an uygun bir bulunan ilan yok"* yazar. Yemekhane'de bulunmuş bir anahtar (#5) olsa da kategorisi farklı olduğu için önerilmez.
   *(Özellik 1'i denediyseniz #7 telefon ilanı burada yüksek puanla görünür; bu, yeni eklenen bir ilanın eşleştirmeye hemen dahil olduğunu gösterir.)*
3. Ters yönde de çalışır: **#3** (BULUNDU) kartında **Eşleşmeleri gör** → #1 kayıp cüzdan önerilir.

**Kabul kriterleri ve nasıl görüleceği**

| Kabul kriteri | Arayüzde nasıl görülür |
|---|---|
| Bir kayıp ilanı için eşleşme önerileri puana göre büyükten küçüğe sıralı dönüyor | Adım 1: 98, ardından 66 |
| Kategorisi farklı olan ilanlar önerilmiyor | Adım 2: #5 anahtar, #2 telefona önerilmez |
| Bulunma tarihi kayıp tarihinden önce olan ilanlar önerilmiyor | Adım 1: #6 önerilmez |
| Aynı konum ve yakın tarih daha yüksek puan alıyor | Adım 1: aynı konumdaki #3 (98) farklı konumdaki #4'ün (66) üstünde |
| Eşleşme yoksa boş liste dönüyor | Adım 2: *"Şu an uygun bir bulunan ilan yok"* |

> API'yi doğrudan denemek isterseniz uygulama adresinin sonuna **`/docs`** ekleyin; tüm uç noktalar orada **Try it out** butonuyla denenebilir.

## Geliştirme Süreci

Her görev panoda bir karta (GitHub issue) karşılık gelir ve kendi branch'inde geliştirilir. Kabul kriterleri testlerle doğrulandıktan sonra pull request açılır; PR açıklamasındaki `Closes #<issue>` ifadesi PR'ı karta bağlar ve merge edildiğinde kartı **Tamamlandı** sütununa taşır.

| Görev | Branch | Pull request |
|---|---|---|
| [#1 İlan oluşturma](https://github.com/ahmetyahyay58/DevOps_Proje/issues/1) | `feature/1-ilan-olusturma` | [PR #7](https://github.com/ahmetyahyay58/DevOps_Proje/pull/7) |
| [#2 Otomatik eşleştirme](https://github.com/ahmetyahyay58/DevOps_Proje/issues/2) | `feature/2-eslestirme` | [PR #8](https://github.com/ahmetyahyay58/DevOps_Proje/pull/8) |
| Web arayüzü (ek) | `feature/web-arayuzu` | [PR #9](https://github.com/ahmetyahyay58/DevOps_Proje/pull/9) |

## Testler

Kabul kriterlerinin her biri otomatik testlerle de doğrulanır:

```bash
python -m pytest -v
```

| Test dosyası | Doğruladığı görev |
|---|---|
| `tests/test_ilan_olusturma.py` | #1 İlan oluşturma |
| `tests/test_eslestirme.py` | #2 Otomatik eşleştirme |
| `tests/test_arayuz.py` | Web arayüzü |

## Kullanılan Teknolojiler

- Python 3.12, FastAPI, Pydantic
- HTML, CSS ve JavaScript (ek kütüphane ya da derleme adımı olmayan tek sayfalık arayüz)
- Pytest (otomatik testler)
- GitHub Codespaces + Dev Container (geliştirme ortamı kod olarak tanımlı, herkes aynı ortamı alır)
