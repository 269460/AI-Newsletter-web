# import os
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from email.mime.application import MIMEApplication
# from dotenv import load_dotenv
# from flask import render_template
# from app import app
#
# # Wczytaj zmienne środowiskowe
# load_dotenv()
#
# def send_email(to_email, subject, template, template_context, attachments=None):
#     # Konfiguracja serwera SMTP
#     smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
#     port = int(os.getenv("SMTP_PORT", 587))
#     sender_email = os.getenv("EMAIL_USER")
#     password = os.getenv("EMAIL_PASSWORD")
#
#     if not sender_email or not password:
#         raise ValueError("Brak danych logowania do konta e-mail. Sprawdź plik .env")
#
#     # Tworzenie wiadomości
#     message = MIMEMultipart("alternative")
#     message["Subject"] = subject
#     message["From"] = sender_email
#     message["To"] = to_email
#
#     # Renderowanie treści z szablonów
#     with app.app_context():
#         text_content = render_template(f"{template}.txt", **template_context)
#         html_content = render_template(f"{template}.html", **template_context)
#
#     # Dodawanie treści tekstowej i HTML
#     part1 = MIMEText(text_content, "plain")
#     part2 = MIMEText(html_content, "html")
#     message.attach(part1)
#     message.attach(part2)
#
#     # Dodawanie załączników, jeśli zostały podane
#     if attachments:
#         for attachment in attachments:
#             with open(attachment, "rb") as file:
#                 part = MIMEApplication(file.read(), Name=os.path.basename(attachment))
#             part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment)}"'
#             message.attach(part)
#
#     # Wysyłanie e-maila
#     try:
#         with smtplib.SMTP(smtp_server, port) as server:
#             server.starttls()
#             server.login(sender_email, password)
#             server.send_message(message)
#         print(f"Email wysłany pomyślnie do {to_email}")
#     except Exception as e:
#         print(f"Błąd podczas wysyłania e-maila do {to_email}: {e}")
#
# def send_newsletter(user, articles):
#     send_email(
#         to_email=user.email,
#         subject='Your AI Newsletter',
#         template='email/newsletter',
#         template_context={'user': user, 'articles': articles}
#     )
