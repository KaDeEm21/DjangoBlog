# Django Blog

Polskojęzyczna aplikacja blogowa przygotowana w Django. Projekt zawiera publiczną listę wpisów, szczegóły posta, profile autorów, komentarze, polubienia, wyszukiwarkę oraz panel użytkownika do zarządzania własnymi treściami.

## Funkcje

- rejestracja, logowanie i wylogowanie
- dodawanie, edycja i usuwanie własnych postów
- komentarze moderowane przez autora posta
- polubienia postów
- wyszukiwarka oraz filtrowanie po kategoriach i tagach
- profil użytkownika i publiczne strony autorów

## Uruchomienie

1. Przejdź do katalogu projektu:

```powershell
cd django_blog
```

2. Utwórz i aktywuj środowisko wirtualne:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

3. Zainstaluj zależności:

```powershell
python -m pip install --upgrade pip
python -m pip install -r .\requirements.txt
```

4. Skopiuj plik środowiskowy:

```powershell
Copy-Item .env.example .env
```

5. Uruchom aplikację:

```powershell
python .\manage.py runserver
```

6. Otwórz w przeglądarce:

```text
http://127.0.0.1:8000/
```

## Konta demo

- `demo_author` / `DemoAuthor123`
- `ola_dev` / `OlaDev123`
- `marek_travel` / `MarekTravel123`
- `ania_culture` / `AniaCulture123`

## Stack

- Python
- Django
- SQLite
- Django Templates
- Tailwind CSS przez CDN
