#tu trzeba bedzie przez azure functions
from mining_summary.spiders.mining_summary import run_spider
from Newsletter_database.news_api import NewsAPI
from newsletter_sender import NewsletterSender


def update_and_send():
    print("Updating articles...")
    run_spider()

    print("Updating summaries...")
    news_api = NewsAPI()
    news_api.update_summaries()

    print("Sending newsletters...")
    sender = NewsletterSender()
    sender.send_newsletters()

    print("Process completed.")


if __name__ == "__main__":
    update_and_send()

# Tak, Microsoft
# Azure
# oferuje
# świetne
# rozwiązania
# do
# automatyzacji
# zadań, takich
# jak
# aktualizacja
# bazy
# danych
# i
# wysyłanie
# newsletterów.Oto
# jak
# możesz
# to
# zrobić
# za
# pomocą
# Azure:
#
# 1.
# Azure
# Functions:
# Azure
# Functions
# to
# usługa
# serverless, która
# pozwala
# na
# uruchamianie
# małych
# fragmentów
# kodu(funkcji)
# bez
# konieczności
# zarządzania
# całym
# serwerem.Możesz
# użyć
# jej
# do
# uruchamiania
# Twojego
# skryptu
# regularnie.
#
# 2.
# Kroki
# implementacji:
#
# a) Przygotowanie
# kodu:
# - Zmodyfikuj
# swój
# skrypt, aby
# działał
# jako
# funkcja
# Azure.
#
# b) Stworzenie
# Azure
# Function
# App:
# - Zaloguj
# się
# do
# Azure
# Portal.
# - Stwórz
# nową
# Function
# App.
#
# c) Wdrożenie
# kodu:
# - Wgraj
# swój
# kod
# do
# Azure
# Function.
#
# d) Konfiguracja
# wyzwalacza
# czasowego:
# - Ustaw
# wyzwalacz
# czasowy(Timer
# trigger) do
# regularnego
# uruchamiania
# funkcji.
#
# 3.
# Przykładowa
# implementacja:
#
# ```python
# import azure.functions as func
# import datetime
# from mining_summary.spiders.mining_summary import run_spider
# from Newsletter_database.news_api import NewsAPI
# from newsletter_sender import NewsletterSender
#
#
# def main(mytimer: func.TimerRequest) -> None:
#     utc_timestamp = datetime.datetime.utcnow().replace(
#         tzinfo=datetime.timezone.utc).isoformat()
#
#     if mytimer.past_due:
#         print('The timer is past due!')
#
#     print('Python timer trigger function ran at %s', utc_timestamp)
#
#     # Uruchomienie spider'a
#     print("Updating articles...")
#     run_spider()
#
#     # Aktualizacja streszczeń
#     print("Updating summaries...")
#     news_api = NewsAPI()
#     news_api.update_summaries()
#
#     # Wysyłanie newsletterów
#     print("Sending newsletters...")
#     sender = NewsletterSender()
#     sender.send_newsletters()
#
#     print("Process completed.")
#
#
# ```
#
# 4.
# Konfiguracja
# wyzwalacza:
# W
# pliku
# `function.json`:
#
# ```json
# {
#     "scriptFile": "__init__.py",
#     "bindings": [
#         {
#             "name": "mytimer",
#             "type": "timerTrigger",
#             "direction": "in",
#             "schedule": "0 0 0 * * *"
#         }
#     ]
# }
#
# ```
#
# Ta
# konfiguracja
# uruchamia
# funkcję
# codziennie
# o
# północy.
#
# 5.
# Zalety
# używania
# Azure:
# - Serverless: Nie
# musisz
# zarządzać
# serwerem.
# - Skalowalność: Azure
# automatycznie
# skaluje
# zasoby
# w
# razie
# potrzeby.
# - Monitorowanie: Łatwe
# śledzenie
# wykonania
# i
# błędów.
# - Integracja: Łatwa
# integracja
# z
# innymi
# usługami
# Azure(np.bazą
# danych).
