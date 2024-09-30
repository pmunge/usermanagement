import asyncio
from aiosmtpd.controller import Controller
from django.core.management.base import BaseCommand

class DebuggingController:
    async def handle_DATA(self, server, session, envelope):
        print(f"Message from: {envelope.mail_from}")
        print(f"Message to: {envelope.rcpt_tos}")
        print(f"Message data: {envelope.content.decode()}")
        return '250 OK'

class Command(BaseCommand):
    help = 'Start the SMTP debugging server'

    def handle(self, *args, **kwargs):
        controller = Controller(DebuggingController(), hostname='localhost', port=1025)
        controller.start()

        try:
            asyncio.Event().wait()  # Keep the server running
        except KeyboardInterrupt:
            controller.stop()
            self.stdout.write(self.style.SUCCESS('SMTP server stopped.'))
