# Lullaby - System Monitorowania Dostępności Biletów

Nowoczesna aplikacja webowa do monitorowania dostępności biletów na koncerty Lullaby. System automatycznie sprawdza liczbę wolnych i zajętych miejsc, wyświetlając dane w przejrzystym interfejsie z mechanizmem cache'owania.

## 📋 Funkcjonalności

- ✅ **Automatyczne scrapowanie** - Pobiera dane o dostępności miejsc z bilety24.pl
- ✅ **15-minutowy cache** - Ogranicza liczbę zapytań do serwisu zewnętrznego
- ✅ **Nowoczesny interfejs** - Minimalistyczny, responsywny design
- ✅ **Podsumowania** - Wyświetla statystyki dla wszystkich koncertów
- ✅ **Status w czasie rzeczywistym** - Informacje o stanie cache i następnej aktualizacji
- ✅ **Obsługa błędów** - Graceful error handling z możliwością ponawiania

## 🚀 Uruchamianie lokalnie

### Wymagania
- Python 3.7+
- pip

### Krok po kroku

1. **Sklonuj/pobierz projekt**
```bash
git clone <repository-url>
cd PythonProject1
```

2. **Zainstaluj zależności**
```bash
pip install -r requirements.txt
```

3. **Uruchom aplikację**
```bash
python app.py
```

4. **Otwórz w przeglądarce**
```
http://localhost:5000
```

## 🌐 Deployment na Replit

### Metoda 1: Import z GitHub
1. Wejdź na [replit.com](https://replit.com)
2. Kliknij "Create Repl"
3. Wybierz "Import from GitHub"
4. Podaj URL swojego repozytorium
5. Kliknij "Import from GitHub"
6. Kliknij przycisk "Run"

### Metoda 2: Upload plików
1. Utwórz nowy Repl (Python)
2. Usuń domyślny `main.py`
3. Prześlij wszystkie pliki projektu:
   - `app.py`
   - `scraper.py` 
   - `requirements.txt`
   - `.replit`
   - katalog `templates/`
   - katalog `static/`
4. Kliknij "Run"

### Konfiguracja Replit
Plik `.replit` już zawiera odpowiednią konfigurację:
```toml
run = "python app.py"
language = "python3"

[deployment]
run = ["sh", "-c", "python app.py"]
```

## 📁 Struktura projektu

```
PythonProject1/
├── app.py                 # Główna aplikacja Flask
├── scraper.py            # Moduł scrapowania danych
├── requirements.txt      # Zależności Python
├── .replit              # Konfiguracja Replit
├── main.py              # Oryginalny skrypt (do usunięcia)
├── templates/
│   └── index.html       # Szablon HTML
└── static/
    ├── css/
    │   └── style.css    # Style CSS
    └── js/
        └── app.js       # JavaScript aplikacji
```

## 🔧 API Endpoints

### `GET /`
Główna strona aplikacji

### `GET /api/seats`
Pobiera dane o dostępności miejsc
```json
{
  "data": {
    "events": [...],
    "summary": {
      "free_total": 120,
      "taken_total": 80,
      "all_total": 200,
      "total_percent": 60.0
    }
  },
  "cached_at": "2024-01-01T12:00:00",
  "cache_expires_at": "2024-01-01T12:15:00"
}
```

### `GET /api/status`
Status cache'a
```json
{
  "cache_valid": true,
  "cached_at": "2024-01-01T12:00:00",
  "cache_expires_at": "2024-01-01T12:15:00"
}
```

## ⚙️ Konfiguracja

### Zmiana URLi koncertów
W pliku `scraper.py`, zaktualizuj słownik `urls`:
```python
self.urls = {
    "2025-09-28": "https://www.bilety24.pl/...",
    "2025-10-04": "https://www.bilety24.pl/...",
    # dodaj nowe daty
}
```

### Zmiana czasu cache'a
W pliku `app.py`, zmień wartość `CACHE_DURATION`:
```python
CACHE_DURATION = 15 * 60  # 15 minut w sekundach
```

## 🐛 Rozwiązywanie problemów

### Problem: "Module not found"
```bash
pip install -r requirements.txt
```

### Problem: Port już zajęty
Zmień port w `app.py`:
```python
app.run(host='0.0.0.0', port=8080, debug=True)
```

### Problem: Błędy scrapowania
1. Sprawdź czy URLe są aktualne
2. Sprawdź połączenie internetowe
3. Sprawdź logi w konsoli dla szczegółów błędów

## 📊 Monitorowanie

Aplikacja automatycznie:
- Odświeża dane co 15 minut
- Wyświetla status cache na stronie głównej  
- Loguje błędy w konsoli
- Pokazuje czas następnej aktualizacji

## 🔒 Bezpieczeństwo

- Aplikacja używa tylko publicznych API
- Nie przechowuje żadnych danych osobowych
- Cache ogranicza częstotliwość zapytań
- CORS skonfigurowany dla bezpieczeństwa

## 📝 Licencja

Projekt stworzony do celów edukacyjnych i monitorowania dostępności biletów.