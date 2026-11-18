from fastapi import FastAPI

app = FastAPI(
    title="Kayıp Eşya API",
    description="Kampüste kaybolan ve bulunan eşyaları buluşturan servis.",
    version="0.1.0",
)


@app.get("/", tags=["Genel"])
def ana_sayfa():
    """Servisin çalıştığını gösterir."""
    return {"servis": "Kayıp Eşya API", "durum": "çalışıyor", "dokumantasyon": "/docs"}
