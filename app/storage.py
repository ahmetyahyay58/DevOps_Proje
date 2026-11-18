from datetime import date, timedelta

from app.models import Ilan, IlanOlustur, IlanTuru


class IlanDeposu:
    """İlanları bellekte tutan basit depo. Uygulama yeniden başlayınca veriler sıfırlanır."""

    def __init__(self) -> None:
        self._ilanlar: dict[int, Ilan] = {}
        self._sonraki_id = 1

    def ekle(self, veri: IlanOlustur) -> Ilan:
        ilan = Ilan(id=self._sonraki_id, **veri.model_dump())
        self._ilanlar[ilan.id] = ilan
        self._sonraki_id += 1
        return ilan

    def listele(self, tur: IlanTuru | None = None) -> list[Ilan]:
        ilanlar = list(self._ilanlar.values())
        if tur is not None:
            ilanlar = [ilan for ilan in ilanlar if ilan.tur == tur]
        return ilanlar

    def getir(self, ilan_id: int) -> Ilan | None:
        return self._ilanlar.get(ilan_id)

    def temizle(self) -> None:
        self._ilanlar.clear()
        self._sonraki_id = 1


def ornek_verileri_yukle(depo: "IlanDeposu") -> None:
    """Uygulamayı deneyenlerin eşleştirmeyi hemen görebilmesi için örnek ilanlar ekler.
    Tarihler bugüne göre hesaplanır, böylece hiçbir zaman gelecek tarihli olmaz."""
    bugun = date.today()
    ornekler = [
        ("kayip", "cuzdan", "Kahverengi deri cüzdan, içinde öğrenci kartı var", "Kütüphane", 3),
        ("kayip", "telefon", "Siyah telefon, kırık ekran koruyuculu", "Yemekhane", 2),
        ("bulundu", "cuzdan", "Kahverengi cüzdan bulundu, danışmaya teslim edildi", "Kütüphane", 2),
        ("bulundu", "cuzdan", "Siyah cüzdan, kantinin yanında", "Mühendislik Fakültesi", 1),
        ("bulundu", "anahtar", "Mavi anahtarlıklı ev anahtarı", "Yemekhane", 1),
        ("bulundu", "cuzdan", "Küçük bozuk para cüzdanı", "Kütüphane", 5),
    ]
    for tur, kategori, aciklama, konum, gun_once in ornekler:
        depo.ekle(
            IlanOlustur(
                tur=tur,
                kategori=kategori,
                aciklama=aciklama,
                konum=konum,
                tarih=bugun - timedelta(days=gun_once),
            )
        )


depo = IlanDeposu()
ornek_verileri_yukle(depo)
