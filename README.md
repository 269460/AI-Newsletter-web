# AI-Newsletter

Ogolna idea

1. Rejestracja i logowanie:
   - Użytkownik wchodzi na stronę główną i widzi opcje logowania lub rejestracji.
   - Przy rejestracji użytkownik podaje:
     - Adres e-mail
     - Hasło
     - Preferowane kategorie technologiczne (wybór wielokrotny)

   - Subskrypcja dla uzytkownikow poprzez formularz, ktore wola otrzymywac newsletter mailem 
    
2. Strona główna (po zalogowaniu):
   - Użytkownik widzi spersonalizowany dashboard z:
     - Najnowszymi artykułami z wybranych kategorii
     
3. Przeglądanie kategorii:
   - Użytkownik może kliknąć na daną kategorię, aby zobaczyć więcej artykułów z tej dziedziny.
   - Na stronie kategorii wyświetlane są tytuły, krótkie streszczenia i linki do pełnych artykułów.

4. Czytanie artykułów:
   - Kliknięcie w tytuł artykułu przenosi użytkownika do strony z pełnym streszczeniem.
   - Na tej stronie jest też link do oryginalnego artykułu.

5. Generowanie i wysyłanie newslettera dla subskrebentow:
   - System automatycznie generuje newslettery zgodnie z preferencjami użytkowników.
   - Newsletter zawiera:
     - Personalizowane powitanie
     - Lista 5-10 najnowszych artykułów z wybranych kategorii (tytuł, krótkie streszczenie, link)
     - Opcję przejścia do pełnej wersji na stronie

6. Otrzymywanie newslettera:
   - Użytkownik otrzymuje e-mail z newsletterem zgodnie z informacja z formularza.
   - E-mail zawiera krótkie streszczenia i linki do pełnych artykułów na stronie.

7. Interakcja z newsletterem:
   - Użytkownik może kliknąć w link w e-mailu, który przeniesie go do pełnej wersji artykułu na stronie.
   - Na stronie artykułu użytkownik ma opcję udostępnienia go w mediach społecznościowych.

  
Implementacja:

1. Frontend (strona internetowa):
   - Używamy Flask do stworzenia strony internetowej.
   - Tworzymy szablony HTML dla każdej z wymienionych stron (strona główna, kategorie, artykuły, ustawienia).
   - Używamy Bootstrap lub innego frameworka CSS do stylizacji.

2. Dokumentacja techniczna systemu Mining Summary
==============================================

1. Ogólny opis systemu
----------------------
Mining Summary to system służący do automatycznego zbierania, kategoryzowania i streszczania artykułów technologicznych. System wykorzystuje techniki web scrapingu, przetwarzania tekstu i sztucznej inteligencji do tworzenia spersonalizowanych streszczeń dla różnych grup odbiorców.

2. Główne komponenty systemu
----------------------------
### 2.1. MiningSpider
- Główny komponent odpowiedzialny za crawling stron
- Bazuje na frameworku Scrapy
- Zarządza procesem pobierania i wstępnego przetwarzania artykułów
- Implementuje logikę kategoryzacji treści
- Obsługuje różne źródła poprzez dedykowane parsery

### 2.2. ArticleFinder
- Komponent odpowiedzialny za wykrywanie nowych artykułów
- Obsługuje dwa typy źródeł:
  * Kanały RSS
  * Bezpośrednie scrapowanie stron WWW
- Implementuje mechanizmy filtrowania duplikatów
- Zarządza listą monitorowanych źródeł

### 2.3. NewsAPI
- Interfejs bazy danych
- Przechowuje informacje o artykułach
- Zarządza metadanymi i treścią
- Implementuje mechanizmy sprawdzania duplikatów

### 2.4. Model streszczający
- Wykorzystuje Azure OpenAI API
- Generuje spersonalizowane streszczenia
- Adaptuje treść do różnych grup odbiorców

3. Wykorzystywane technologie i biblioteki
-----------------------------------------
### 3.1. Podstawowe biblioteki Python:
- Scrapy: Framework do web scrapingu
- BeautifulSoup4: Parsowanie HTML
- Feedparser: Obsługa kanałów RSS
- Requests: Obsługa żądań HTTP
- Logging: System logowania

### 3.2. Przetwarzanie tekstu:
- Azure OpenAI API: Generowanie streszczeń
- Własne narzędzia do czyszczenia tekstu

### 3.3. Przechowywanie danych:
- System bazodanowy (przez NewsAPI)
- Mechanizmy cache'owania

4. Funkcjonalności systemu
-------------------------
### 4.1. Zbieranie artykułów:
- Monitorowanie kanałów RSS
- Scrapowanie wybranych stron WWW
- Wykrywanie duplikatów
- Obsługa błędów i retry

### 4.2. Przetwarzanie treści:
- Ekstrakcja tekstu z HTML
- Czyszczenie i normalizacja tekstu
- Kategoryzacja tematyczna
- Generowanie streszczeń

### 4.3. Kategoryzacja:
System rozpoznaje następujące kategorie:
- AI: Sztuczna Inteligencja
- IoT: Internet Rzeczy
- CS: Cyberbezpieczeństwo
- RA: Robotyka i Automatyzacja
- TC: Technologie Chmurowe
- TM: Technologie Mobilne
- BT: Biotechnologia
- NT: Nanotechnologia
- EO: Energetyka Odnawialna
- TK: Technologie Kwantowe

5. Konfiguracja i deployment
---------------------------
### 5.1. Wymagane komponenty:
- Python 3.8+
- Dostęp do Azure OpenAI API
- System bazodanowy
- Dostęp do internetu

### 5.2. Konfiguracja:
- Ustawienia w pliku config
- Konfiguracja logowania
- Parametry scrapingu
- Klucze API

6. Obsługa błędów i monitoring
-----------------------------
### 6.1. System logowania:
- Osobne logi dla różnych komponentów
- Różne poziomy logowania
- Rotacja logów

### 6.2. Obsługa błędów:
- Automatyczne retry
- Graceful degradation
- Powiadomienia o błędach krytycznych

7. Wydajność i optymalizacja
---------------------------
### 7.1. Mechanizmy optymalizacyjne:
- Limitowanie requestów
- Respektowanie robots.txt
- Inteligentne opóźnienia między requestami
- Wykrywanie duplikatów

### 7.2. Skalowanie:
- Możliwość równoległego przetwarzania
- Konfigurowalny poziom współbieżności
- Zarządzanie zasobami

8. Bezpieczeństwo
----------------
### 8.1. Zabezpieczenia:
- Bezpieczne przechowywanie kluczy API
- Przestrzeganie polityk ROBOTS.txt
- Limitowanie dostępu do API
- Walidacja danych wejściowych

9. Przyszłe rozszerzenia
------------------------
### 9.1. Planowane funkcjonalności:
- Mechanizm cache'owania
- Asynchroniczne przetwarzanie
- System kolejkowania zadań
- Rozszerzona analiza sentymentu
- Wielojęzyczność

10. Utrzymanie i rozwój
----------------------
### 10.1. Aktualizacje:
- Regularne aktualizacje selektorów
- Dostosowywanie do zmian w API
- Optymalizacja wydajności
- Rozszerzanie bazy źródeł

3. Baza danych:
   - Przechowuje informacje o użytkownikach, ich preferencjach, artykułach i streszczeniach.

4. System wysyłki e-maili:
   - Używamy biblioteki do wysyłania e-maili (np. Flask-Mail) do dystrybucji newsletterów.


działania bazy danych 

Kategorie (Categories):

Każda kategoria ma unikalną nazwę i opis.
Kategorie są teraz bezpośrednio powiązane z artykułami.


Artykuły (Article):

Każdy artykuł jest przypisany do jednej kategorii poprzez category_id.
Artykuły mają link, tytuł, treść, źródło i datę utworzenia.
Każdy artykuł może mieć jedno powiązane podsumowanie.


Podsumowania (Summary):

Każde podsumowanie jest powiązane z jednym artykułem.
Zawiera tylko tekst podsumowania, bez osobnej kategorii.


Użytkownicy (User):

Przechowują email, zahaszowane hasło i preferencje (jako JSON).
Nie ma już pola is_admin.


Subskrypcje (Subscription):

Łączą użytkowników z kategoriami, określając częstotliwość otrzymywania newslettera.
