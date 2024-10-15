from tasks import update_articles, update_summaries, send_newsletters


def manual_update_and_send():
    print("Rozpoczęcie ręcznego procesu aktualizacji i wysyłania...")

    print("Aktualizacja artykułów...")
    update_articles()

    print("Aktualizacja streszczeń...")
    update_summaries()

    print("Wysyłanie newsletterów...")
    send_newsletters()

    print("Proces zakończony.")


if __name__ == "__main__":
    manual_update_and_send()