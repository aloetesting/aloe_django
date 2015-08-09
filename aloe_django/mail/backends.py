#

"""
Email backend that sends mails to a multiprocessing queue
"""
from aloe_django import mail
from django.core.mail.backends.base import BaseEmailBackend


class QueueEmailBackend(BaseEmailBackend):
    """
    Email backend that allows mail to be captured by tests run between
    separate processes via :mod:`multiprocessing`.
    """

    def send_messages(self, messages):
        for message in messages:
            mail.queue.put(message)  # pylint:disable=no-member

        return len(messages)
