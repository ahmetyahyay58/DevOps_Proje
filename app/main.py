from fastapi import FastAPI, HTTPException, status

from app.models import Ilan, IlanOlustur, IlanTuru
from app.storage import depo

app = FastAPI(
    title="Kayıp Eşya API",
    description="Kampüste kaybolan ve bulunan eşyaları buluşturan servis.",
    version="0.2.0",
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
    ilan = depo.getir(ilan_id)
    if ilan is None:
        raise HTTPException(status_code=404, detail="İlan bulunamadı")
    return ilan
