"""Web arayüzünün sunulduğunu ve API ile birlikte çalıştığını doğrulayan testler."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_ana_sayfa_arayuzu_sunar():
    yanit = client.get("/")

    assert yanit.status_code == 200
    assert "text/html" in yanit.headers["content-type"]
    assert "Kayıp Eşya" in yanit.text


def test_arayuz_api_uc_noktalarini_kullanir():
    html = client.get("/").text

    assert "/ilanlar" in html
    assert "/eslesmeler" in html


def test_saglik_kontrolu_calisir():
    yanit = client.get("/saglik")

    assert yanit.status_code == 200
    assert yanit.json()["durum"] == "çalışıyor"


def test_api_dokumantasyonu_hala_erisilebilir():
    assert client.get("/docs").status_code == 200
