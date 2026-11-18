from datetime import date
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class IlanTuru(str, Enum):
    """İlanın kayıp mı yoksa bulunan eşya için mi açıldığı."""

    kayip = "kayip"
    bulundu = "bulundu"


class Kategori(str, Enum):
    """Kabul edilen eşya kategorileri. Listede olmayan kategori 422 hatası verir."""

    cuzdan = "cuzdan"
    telefon = "telefon"
    anahtar = "anahtar"
    kimlik_kart = "kimlik_kart"
    canta = "canta"
    elektronik = "elektronik"
    kiyafet = "kiyafet"
    diger = "diger"


class IlanOlustur(BaseModel):
    """Kullanıcının yeni ilan açarken gönderdiği bilgiler."""

    tur: IlanTuru
    kategori: Kategori
    aciklama: str = Field(min_length=3, max_length=500, examples=["Kahverengi deri cüzdan"])
    konum: str = Field(min_length=2, max_length=100, examples=["Kütüphane"])
    tarih: date = Field(examples=["2026-11-15"])

    @field_validator("aciklama", "konum")
    @classmethod
    def bosluklari_temizle(cls, deger: str) -> str:
        deger = deger.strip()
        if len(deger) < 2:
            raise ValueError("Bu alan boş bırakılamaz")
        return deger

    @field_validator("tarih")
    @classmethod
    def gelecek_tarih_olamaz(cls, deger: date) -> date:
        if deger > date.today():
            raise ValueError("İlan tarihi gelecekte olamaz")
        return deger


class Ilan(IlanOlustur):
    """Sisteme kaydedilmiş, ID almış ilan."""

    id: int
