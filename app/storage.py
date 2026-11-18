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


depo = IlanDeposu()
