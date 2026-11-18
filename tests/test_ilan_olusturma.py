"""Issue #1 — Kayıp / bulunan eşya ilanı oluşturma: kabul kriterleri testleri."""

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


def ornek_ilan(**degisiklikler):
    veri = {
        "tur": "kayip",
        "kategori": "cuzdan",
        "aciklama": "Kahverengi deri cüzdan",
        "konum": "Kütüphane",
        "tarih": str(date.today() - timedelta(days=1)),
    }
    veri.update(degisiklikler)
    return veri


# Kriter 1: Tüm bilgilerle ilan oluşturulabiliyor ve ID veriliyor
def test_ilan_olusturulur_ve_id_verilir():
    yanit = client.post("/ilanlar", json=ornek_ilan())

    assert yanit.status_code == 201
    govde = yanit.json()
    assert govde["id"] == 1
    assert govde["kategori"] == "cuzdan"
    assert govde["konum"] == "Kütüphane"


def test_her_ilan_farkli_id_alir():
    birinci = client.post("/ilanlar", json=ornek_ilan()).json()
    ikinci = client.post("/ilanlar", json=ornek_ilan(tur="bulundu")).json()

    assert birinci["id"] != ikinci["id"]


# Kriter 2: Zorunlu alan eksikse ya da kategori geçersizse 422
def test_zorunlu_alan_eksikse_422():
    veri = ornek_ilan()
    del veri["kategori"]

    assert client.post("/ilanlar", json=veri).status_code == 422


def test_gecersiz_kategori_422():
    assert client.post("/ilanlar", json=ornek_ilan(kategori="uzay_gemisi")).status_code == 422


def test_bos_aciklama_422():
    assert client.post("/ilanlar", json=ornek_ilan(aciklama="   ")).status_code == 422


# Kriter 3: İlanlar listelenebiliyor ve türe göre filtrelenebiliyor
def test_ilanlar_listelenir():
    client.post("/ilanlar", json=ornek_ilan())
    client.post("/ilanlar", json=ornek_ilan(tur="bulundu"))

    yanit = client.get("/ilanlar")

    assert yanit.status_code == 200
    assert len(yanit.json()) == 2


def test_ilanlar_ture_gore_filtrelenir():
    client.post("/ilanlar", json=ornek_ilan(tur="kayip"))
    client.post("/ilanlar", json=ornek_ilan(tur="bulundu"))
    client.post("/ilanlar", json=ornek_ilan(tur="bulundu"))

    bulunanlar = client.get("/ilanlar", params={"tur": "bulundu"}).json()

    assert len(bulunanlar) == 2
    assert all(ilan["tur"] == "bulundu" for ilan in bulunanlar)


def test_olmayan_ilan_404():
    assert client.get("/ilanlar/999").status_code == 404


# Kriter 4: Gelecek tarihli ilan oluşturulamıyor
def test_gelecek_tarihli_ilan_reddedilir():
    yarin = str(date.today() + timedelta(days=1))

    assert client.post("/ilanlar", json=ornek_ilan(tarih=yarin)).status_code == 422


def test_bugunun_tarihi_kabul_edilir():
    bugun = str(date.today())

    assert client.post("/ilanlar", json=ornek_ilan(tarih=bugun)).status_code == 201
