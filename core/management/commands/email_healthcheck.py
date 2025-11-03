from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMessage, get_connection
from django.conf import settings


class Command(BaseCommand):
    help = "Verifies email connectivity by opening an SMTP connection and (optionally) sending a test email."

    def add_arguments(self, parser):
        parser.add_argument(
            "--to",
            dest="to_email",
            help="Recipient email (defaults to EMAIL_HOST_USER or DEFAULT_FROM_EMAIL)",
            default=None,
        )
        parser.add_argument(
            "--subject",
            dest="subject",
            default="Email health check",
            help="Subject for the test email",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Only open and close SMTP connection without sending an email",
        )
        parser.add_argument(
            "--timeout",
            type=int,
            default=15,
            help="SMTP connection timeout in seconds (default: 15)",
        )

    def handle(self, *args, **options):
        to_email = options["to_email"] or settings.EMAIL_HOST_USER or settings.DEFAULT_FROM_EMAIL
        subject = options["subject"]
        dry_run = options["dry_run"]
        timeout = options["timeout"]

        try:
            conn = get_connection(timeout=timeout)
            conn.open()
        except Exception as e:
            raise CommandError(f"SMTP connection failed: {e}")

        if dry_run:
            self.stdout.write(self.style.SUCCESS("SMTP connection established successfully (dry run)"))
            try:
                conn.close()
            except Exception:
                pass
            return

        if not to_email:
            try:
                conn.close()
            except Exception:
                pass
            raise CommandError(
                "No recipient available. Provide --to or set EMAIL_HOST_USER/DEFAULT_FROM_EMAIL."
            )

        sender = settings.DEFAULT_FROM_EMAIL or settings.EMAIL_HOST_USER
        if not sender:
            try:
                conn.close()
            except Exception:
                pass
            raise CommandError(
                "No sender available. Set DEFAULT_FROM_EMAIL or EMAIL_HOST_USER in environment."
            )

        try:
            msg = EmailMessage(
                subject,
                "This is an automated email connectivity check from the LMS portal.",
                sender,
                [to_email],
                connection=conn,
            )
            sent = msg.send()
            conn.close()
            if sent:
                self.stdout.write(self.style.SUCCESS(f"Email sent successfully to {to_email}"))
            else:
                raise CommandError("send() returned 0; email not sent")
        except Exception as e:
            raise CommandError(f"Email health check failed while sending: {e}")
