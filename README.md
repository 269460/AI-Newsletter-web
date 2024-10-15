# AI-Newsletter

Ogolna idea

1. Rejestracja i logowanie:
   - Użytkownik wchodzi na stronę główną i widzi opcje logowania lub rejestracji.
   - Przy rejestracji użytkownik podaje:
     - Adres e-mail
     - Hasło
     - Preferowane kategorie technologiczne (wybór wielokrotny)
     - Subskrypcja dla uzytkownikow, ktore wola otrzymywac newsletter mailem 
    
2. Strona główna (po zalogowaniu):
   - Użytkownik widzi spersonalizowany dashboard z:
     - Najnowszymi artykułami z wybranych kategorii
     - Opcją zmiany preferencji
   
     
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

8. Panel ustawień użytkownika:
   - Użytkownik może w każdej chwili zmienić swoje preferencje:
     - Dodać lub usunąć kategorie
   

9. Funkcje dodatkowe:
   - Wyszukiwarka artykułów na stronie
  
Implementacja:

1. Frontend (strona internetowa):
   - Używamy Flask do stworzenia strony internetowej.
   - Tworzymy szablony HTML dla każdej z wymienionych stron (strona główna, kategorie, artykuły, ustawienia).
   - Używamy Bootstrap lub innego frameworka CSS do stylizacji.

2. Backend:
   - `MiningSpider` regularnie scrapuje nowe artykuły i zapisuje je w bazie danych.
   - `NewsAPI` obsługuje wszystkie interakcje z bazą danych.
   - `NewsletterSender` generuje i wysyła spersonalizowane newslettery.

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



Główne zmiany i ich wpływ:

Kategoria jest teraz bezpośrednio powiązana z artykułem, co upraszcza zapytania i strukturę danych.

Użytkownicy mogą przeglądać artykuły i kategorie.
Zalogowani użytkownicy mogą aktualizować swoje preferencje dotyczące kategorii.
Subskrypcja newslettera jest zarządzana przez news_api, a nie bezpośrednio przez model User.
Użytkownicy mogą generować PDF-y z artykułami dla wybranych kategorii.
Istnieje możliwość wyszukiwania artykułów.