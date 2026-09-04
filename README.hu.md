# HomePantry

A HomePantry egy saját szerveren futtatható háztartási kamra-, készlet- és
receptkezelő alkalmazás magyar és angol felülettel.

Asztali gépen és mobilon is használható, és a hétköznapi otthoni
készletkezelésre készült.

> **Állapot:** `0.1.0-alpha.1`
>
> Ez az első nyilvános alpha kiadás.

## Főbb funkciók

- Háztartás alapú többfelhasználós működés
- Magyar és angol felület
- Alapanyag-törzs
- Kategóriák, aliasok, mértékegységek és helyettesítések
- Terméktörzs több vonalkóddal
- Böngészőből működő vonalkódolvasás
- Open Food Facts termékadat-lekérdezés
- Termék- és tárolóhely-képek
- Hierarchikus tárolóhelyek
- Készlettételek és készletmozgások
- Minimumkészlet-szabályok
- Receptkezelés
- Receptcímkék és képek
- Recept elkészíthetőségének vizsgálata az aktuális készlet alapján
- Online receptkeresés és import TheMealDB-ről
- Importált mértékegységek normalizálása
- Opcionális helyi receptfordítás LibreTranslate használatával
- PostgreSQL adatbázis
- Alembic migrációk
- Gunicorn és systemd
- Reverse proxy és application prefix támogatás
- Health-check végpont
- Automatikus Ubuntu telepítő

## Képernyőképek

Az első nyilvános kiadáshoz képernyőképek is kerülnek a repóba.

## Rendszerigény

Ajánlott környezet:

- Ubuntu 24.04 LTS
- PostgreSQL
- Python 3.12
- systemd
- modern webböngésző

Docker csak az opcionális LibreTranslate telepítéshez szükséges.

## Telepítés

Lásd:

- [English installation guide](docs/INSTALL.md)
- [Magyar telepítési útmutató](docs/INSTALL.hu.md)

Normál Ubuntu telepítéshez:

```bash
sudo ./install.sh
```

A telepítő előkészíti:

- PostgreSQL-t
- alkalmazásfelhasználót
- Python virtual environmentet
- függőségeket
- környezeti konfigurációt
- adatbázis-migrációkat
- referenciaadatokat
- systemd service-t
- health checket

## Első használat

Telepítés után:

```text
http://SERVER_IP:8084/
```

Az első felhasználó a regisztrációs oldalon hozható létre.

Az első regisztrált felhasználó létrehozza a háztartást és annak
tulajdonosa lesz.

## Reverse proxy és Tailscale

A HomePantry application prefix alatt is használható, például:

```text
/homepantry
```

Beállítás:

```env
APPLICATION_PREFIX=/homepantry
```

Ezzel párhuzamosan a közvetlen LAN-elérés továbbra is működhet a `/`
útvonalon.

## Opcionális receptfordítás

Az importált angol receptek magyarításához külön LibreTranslate service
használható.

Telepítés:

```bash
sudo ./deploy/install-libretranslate.sh
```

Ha a LibreTranslate nem érhető el, a receptimport továbbra is működik,
és az eredeti angol szöveg kerül mentésre.

## Külső szolgáltatások

A HomePantry opcionálisan használja:

- Open Food Facts
- TheMealDB
- LibreTranslate

A böngészős vonalkódolvasást a Quagga2 biztosítja.

Licenc- és forrásinformációk:

[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)

## Adatok és mentés

Az alkalmazás adatai PostgreSQL-ben, a feltöltött képek pedig a HomePantry
feltöltési könyvtáraiban találhatók.

Az adatbázist és a feltöltött médiát rendszeresen mentsd.

Alpha verziók közötti frissítés előtt mindig készíts friss biztonsági
mentést.

## Fejlesztési állapot

A HomePantry már valódi háztartási használatban működik, de a nyilvános
kiadás jelenleg alpha állapotú.

A telepítés, konfiguráció, migrációk és dokumentáció az alpha verziók
során még változhatnak.

## Licenc

A HomePantry MIT licenc alatt érhető el.

Lásd: [LICENSE](LICENSE)

## Támogatás

Ha hasznosnak találod a HomePantry-t és támogatnád a fejlesztését:

https://www.patreon.com/c/ZoltanRigo
