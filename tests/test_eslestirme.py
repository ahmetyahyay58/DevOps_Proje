"""Issue #2 — Kayıp ve bulunan ilanları otomatik eşleştirme: kabul kriterleri testleri."""

from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.storage import depo

client = TestClient(app)


@pytest.fixture(autouse=True)
def depoyu_sifirla():
    depo.temizle()
    yield
    depo.temizle()


def gun_once(gun: int) -> str:
    return str(date.today() - timedelta(days=gun))


def ilan_ekle(tur, kategori="cuzdan", konum="Kütüphane", tarih=None, aciklama="Test eşyası"):
    veri = {
        "tur": tur,
        "kategori": kategori,
        "aciklama": aciklama,
        "konum": konum,
        "tarih": tarih or gun_once(5),
    }
    yanit = client.post("/ilanlar", json=veri)
    assert yanit.status_code == 201
    return yanit.json()["id"]


def eslesmeler(ilan_id):
    yanit = client.get(f"/ilanlar/{ilan_id}/eslesmeler")
    assert yanit.status_code == 200
    return yanit.json()


# Kriter 1: Öneriler puana göre büyükten küçüğe sıralı dönüyor
def test_oneriler_puana_gore_sirali():
    kayip = ilan_ekle("kayip", konum="Kütüphane", tarih=gun_once(5))
    uzak = ilan_ekle("bulundu", konum="Yemekhane", tarih=gun_once(1))
    yakin = ilan_ekle("bulundu", konum="Kütüphane", tarih=gun_once(5))

    sonuc = eslesmeler(kayip)

    assert [e["ilan"]["id"] for e in sonuc] == [yakin, uzak]
    assert sonuc[0]["puan"] > sonuc[1]["puan"]


# Kriter 2: Kategorisi farklı olan ilanlar önerilmiyor
def test_farkli_kategori_onerilmez():
    kayip = ilan_ekle("kayip", kategori="cuzdan")
    ilan_ekle("bulundu", kategori="telefon")

    assert eslesmeler(kayip) == []


# Kriter 3: Kayıp tarihinden önce bulunmuş ilanlar önerilmiyor
def test_kayiptan_once_bulunan_onerilmez():
    kayip = ilan_ekle("kayip", tarih=gun_once(3))
    ilan_ekle("bulundu", tarih=gun_once(4))

    assert eslesmeler(kayip) == []


def test_ayni_gun_bulunan_onerilir():
    kayip = ilan_ekle("kayip", tarih=gun_once(3))
    bulunan = ilan_ekle("bulundu", tarih=gun_once(3))

    assert [e["ilan"]["id"] for e in eslesmeler(kayip)] == [bulunan]


# Kriter 4: Aynı konum ve yakın tarih daha yüksek puan alıyor
def test_ayni_konum_ve_ayni_gun_tam_puan():
    kayip = ilan_ekle("kayip", konum="Kütüphane", tarih=gun_once(2))
    ilan_ekle("bulundu", konum="kütüphane ", tarih=gun_once(2))

    assert eslesmeler(kayip)[0]["puan"] == 100


def test_ayni_konum_farkli_konumdan_yuksek_puan_alir():
    kayip = ilan_ekle("kayip", konum="Kütüphane", tarih=gun_once(5))
    ayni_konum = ilan_ekle("bulundu", konum="Kütüphane", tarih=gun_once(3))
    farkli_konum = ilan_ekle("bulundu", konum="Spor Salonu", tarih=gun_once(3))

    puanlar = {e["ilan"]["id"]: e["puan"] for e in eslesmeler(kayip)}

    assert puanlar[ayni_konum] > puanlar[farkli_konum]


def test_yakin_tarih_uzak_tarihten_yuksek_puan_alir():
    kayip = ilan_ekle("kayip", tarih=gun_once(10))
    yakin = ilan_ekle("bulundu", tarih=gun_once(9))
    uzak = ilan_ekle("bulundu", tarih=gun_once(2))

    puanlar = {e["ilan"]["id"]: e["puan"] for e in eslesmeler(kayip)}

    assert puanlar[yakin] > puanlar[uzak]


# Kriter 5: Eşleşme yoksa boş liste dönüyor
def test_eslesme_yoksa_bos_liste():
    kayip = ilan_ekle("kayip")

    assert eslesmeler(kayip) == []


# Ek: Bulunan ilanı için de kayıp ilanları önerilir, kendi türü önerilmez
def test_bulunan_ilan_icin_kayiplar_onerilir():
    kayip = ilan_ekle("kayip", tarih=gun_once(4))
    ilan_ekle("bulundu", tarih=gun_once(4))
    bulunan = ilan_ekle("bulundu", tarih=gun_once(2))

    assert [e["ilan"]["id"] for e in eslesmeler(bulunan)] == [kayip]


def test_olmayan_ilan_icin_404():
    assert client.get("/ilanlar/999/eslesmeler").status_code == 404
