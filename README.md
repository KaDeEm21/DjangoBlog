# Django Blog

Polskojęzyczna aplikacja blogowa zbudowana w Django. Projekt obejmuje publiczny katalog wpisów, profile autorów, komentarze, polubienia, wyszukiwarkę, filtrowanie po kategoriach i tagach oraz panel użytkownika do zarządzania własną treścią.

## Stack technologiczny

- Python 3.12+
- Django 6
- SQLite 3
- Django ORM
- Django Templates
- Tailwind CSS przez CDN w [`blog/templates/blog/base.html`](blog/templates/blog/base.html)

## Najważniejsze funkcje

- rejestracja, logowanie i wylogowanie użytkownika
- automatyczne tworzenie profilu użytkownika przez sygnał `post_save`
- tworzenie, edycja i usuwanie własnych wpisów
- komentarze zapisywane jako oczekujące i moderowane po stronie autora wpisu
- polubienia oparte o adres IP
- wyszukiwarka i filtrowanie po kategorii, tagu i popularności
- publiczne strony autorów z podstawowymi statystykami
- seed danych demo z gotowymi użytkownikami, wpisami, komentarzami i polubieniami
- gotowa baza `db.sqlite3` z załadowanymi danymi demonstracyjnymi do szybkiego pokazu projektu

## Architektura projektu

Projekt ma prostą architekturę monolitu Django z jedną główną aplikacją `blog`.

- [`settings.py`](settings.py) ładuje konfigurację projektu, w tym SQLite oraz zmienne środowiskowe z `.env`
- [`urls.py`](urls.py) mapuje główne trasy i panel admina
- [`blog/models.py`](blog/models.py) definiuje modele `Post`, `Category`, `Tag`, `Comment`, `Like` i `Profile`
- [`blog/views.py`](blog/views.py) trzyma logikę widoków funkcyjnych
- [`blog/forms.py`](blog/forms.py) odpowiada za walidację formularzy
- [`blog/templates/blog`](blog/templates/blog) zawiera warstwę prezentacji
- [`blog/management/commands/seed_data.py`](blog/management/commands/seed_data.py) buduje przykładowe dane do demo

Relacje domenowe:

- `Post` należy do autora i kategorii, a tagi obsługuje przez relację wiele-do-wielu
- `Comment` i `Like` są przypięte do wpisu
- `Profile` jest relacją jeden-do-jednego z użytkownikiem Django

## Jak uruchomić

1. Przejdź do katalogu projektu:

```bash
cd django_blog
```

2. Utwórz wirtualne środowisko:

```bash
python -m venv .venv
```

3. Aktywuj środowisko:

```bash
.venv\Scripts\activate
```

4. Zaktualizuj pip oraz zainstaluj zależności:

```bash
python -m pip install --upgrade pip
python -m pip install -r .\requirements.txt
```

5. Skopiuj przykładową konfigurację środowiskową:

```bash
cp .env.example .env
```

W PowerShell możesz użyć:

```powershell
Copy-Item .env.example .env
```

6. Uruchom migracje:

```bash
python manage.py migrate
```

7. Repo zawiera już gotową bazę `db.sqlite3` z danymi demo, więc po migracjach możesz od razu uruchomić aplikację.

8. Jeśli chcesz odtworzyć dane demo od zera:

```bash
python manage.py seed_data
```

9. Uruchom serwer developerski:

```bash
python manage.py runserver
```

10. Otwórz przeglądarkę i wejdź na:

```text
http://127.0.0.1:8000/
```

Zmienne środowiskowe używane przez projekt:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`

## Dane logowania do użytkowników demo

- `admin` / lokalne hasło zapisane wyłącznie w dołączonej bazie `db.sqlite3`
- `demo_author` / `DemoAuthor123`
- `ola_dev` / `OlaDev123`
- `marek_travel` / `MarekTravel123`
- `ania_culture` / `AniaCulture123`

## O mnie

```md
Nazywam się Karol Michalak. Rozwijam projekty webowe w Pythonie i Django, skupiając się na czytelnej architekturze, prostych interfejsach i sensownym DX.

- GitHub: https://github.com/KaDeEm21
- LinkedIn: https://www.linkedin.com/in/karol-michalak-045803354/
```

## Grafiki i licencje

### Avatary

Seed danych nie używa już zewnętrznych zdjęć ludzi. Profile demo korzystają z fallbacku w interfejsie, który renderuje inicjał użytkownika, więc nie dochodzi tu zewnętrzna licencja obrazów ani ryzyko związane z prawem do wizerunku.

### Miniatury postów

Miniatury wpisów w seedzie nadal wskazują na obrazy z CDN Unsplash:

- [`blog/management/commands/seed_data.py`](blog/management/commands/seed_data.py)

Przydatne źródła licencyjne:

- Unsplash License: https://unsplash.com/license
- Unsplash Terms, sekcja "License to Images": https://unsplash.com/terms
- Releases and Trademarks: https://help.unsplash.com/en/articles/2612329-releases-and-trademarks
- Identifiable person / brand FAQ: https://help.unsplash.com/en/articles/2646379-what-if-there-s-a-brand-or-identifiable-person-depicted-in-an-image-that-i-download

Krótki cytat z warunków Unsplash:

> "for free, including for commercial purposes, without permission"

To nie zwalnia jednak z oceny praw do tego, co zdjęcie przedstawia. Unsplash wyraźnie wskazuje, że sama licencja autorska nie daje automatycznie prawa do wykorzystania rozpoznawalnych osób, znaków towarowych ani niektórych obiektów. Dlatego w tym projekcie avatary zostały zastąpione bezpiecznym fallbackiem, a miniatury warto traktować jako materiały demonstracyjne.

Jeżeli repo ma być publicznie prezentowane albo używane komercyjnie, rozsądnym kolejnym krokiem jest zamiana miniatur na własne grafiki, lokalne placeholdery albo obrazy z pełną ścieżką atrybucji i weryfikowalnym źródłem.

## Struktura katalogów

```text
django_blog/
├── blog/
│   ├── management/commands/
│   │   └── seed_data.py
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── settings.py
├── urls.py
└── README.md
```
