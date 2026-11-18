"""Kayıp ve bulunan ilanları eşleştirme kuralları.

Puanlama (en fazla 100):
- Kategori aynı olmalı, değilse eşleşme yok          -> 50 puan
- Eşya kaybolmadan önce bulunmuş olamaz              -> eşleşme yok
- Konum aynıysa (büyük/küçük harf fark etmez)        -> +30 puan
- Tarih yakınlığı: aynı gün +20, her gün için -2      -> 0 ile 20 arası
"""

from app.models import Eslesme, Ilan, IlanTuru

KATEGORI_PUANI = 50
KONUM_PUANI = 30
TARIH_PUANI = 20
GUNLUK_DUSUS = 2


def konum_normalize(konum: str) -> str:
    return konum.strip().casefold()


def puan_hesapla(kayip: Ilan, bulunan: Ilan) -> int | None:
    """Bir kayıp ve bir bulunan ilan arasındaki uyum puanını döner.
    Eşleşme mümkün değilse None döner."""
    if kayip.kategori != bulunan.kategori:
        return None
    if bulunan.tarih < kayip.tarih:
        return None

    puan = KATEGORI_PUANI
    if konum_normalize(kayip.konum) == konum_normalize(bulunan.konum):
        puan += KONUM_PUANI

    gun_farki = (bulunan.tarih - kayip.tarih).days
    puan += max(0, TARIH_PUANI - gun_farki * GUNLUK_DUSUS)
    return puan


def eslesmeleri_bul(ilan: Ilan, tum_ilanlar: list[Ilan]) -> list[Eslesme]:
    """Verilen ilan için karşı türdeki ilanlar arasından eşleşmeleri puana göre sıralı döner.
    Kayıp ilanı için bulunanlara, bulunan ilanı için kayıplara bakar."""
    eslesmeler = []
    for aday in tum_ilanlar:
        if aday.tur == ilan.tur:
            continue
        if ilan.tur == IlanTuru.kayip:
            puan = puan_hesapla(kayip=ilan, bulunan=aday)
        else:
            puan = puan_hesapla(kayip=aday, bulunan=ilan)
        if puan is not None:
            eslesmeler.append(Eslesme(puan=puan, ilan=aday))

    eslesmeler.sort(key=lambda e: (-e.puan, e.ilan.id))
    return eslesmeler
