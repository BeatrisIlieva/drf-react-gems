from unittest.mock import patch
from django.test import TestCase

from src.common.tasks import _send_email


class TestSendEmailTask(TestCase):
    @patch('src.common.tasks.send_mail')
    def test_send_mail_calls_django_send_mail_func(
        self, mock_django_send_mail
    ):
        _send_email(
            subject="Subject",
            message="Message",
            html_message="HTML message",
            from_email='test@mail.com',
            recipient_list=['test@mail.com'],
        )

        mock_django_send_mail.assert_called_once_with(
            subject="Subject",
            message="Message",
            html_message="HTML message",
            from_email='test@mail.com',
            recipient_list=['test@mail.com'],
        )
