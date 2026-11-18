from fastapi import FastAPI, HTTPException, status

from app.matching import eslesmeleri_bul
from app.models import Eslesme, Ilan, IlanOlustur, IlanTuru
from app.storage import depo

app = FastAPI(
    title="Kayıp Eşya API",
    description="Kampüste kaybolan ve bulunan eşyaları buluşturan servis.",
    version="0.3.0",
)


@app.get("/", tags=["Genel"])
def ana_sayfa():
    """Servisin çalıştığını gösterir."""
    return {"servis": "Kayıp Eşya API", "durum": "çalışıyor", "dokumantasyon": "/docs"}


@app.post("/ilanlar", response_model=Ilan, status_code=status.HTTP_201_CREATED, tags=["İlanlar"])
def ilan_olustur(veri: IlanOlustur):
    """Kayıp ya da bulunan bir eşya için yeni ilan oluşturur."""
    return depo.ekle(veri)


@app.get("/ilanlar", response_model=list[Ilan], tags=["İlanlar"])
def ilanlari_listele(tur: IlanTuru | None = None):
    """Tüm ilanları listeler. `tur` verilirse yalnızca kayıp ya da bulunan ilanları döner."""
    return depo.listele(tur)


@app.get("/ilanlar/{ilan_id}", response_model=Ilan, tags=["İlanlar"])
def ilan_getir(ilan_id: int):
    """ID'si verilen ilanı getirir."""
    return _ilan_bul(ilan_id)


@app.get("/ilanlar/{ilan_id}/eslesmeler", response_model=list[Eslesme], tags=["Eşleştirme"])
def eslesmeleri_getir(ilan_id: int):
    """Verilen ilan için olası eşleşmeleri puana göre (yüksekten düşüğe) listeler.

    Kayıp ilanı için bulunan ilanlara, bulunan ilanı için kayıp ilanlara bakılır.
    Kategori farklıysa ya da eşya kaybolmadan önce bulunmuşsa öneri yapılmaz.
    """
    ilan = _ilan_bul(ilan_id)
    return eslesmeleri_bul(ilan, depo.listele())


def _ilan_bul(ilan_id: int) -> Ilan:
    ilan = depo.getir(ilan_id)
    if ilan is None:
        raise HTTPException(status_code=404, detail="İlan bulunamadı")
    return ilan
