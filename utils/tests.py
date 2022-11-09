from time import sleep

from django.test import TestCase


class SleepyTestCase(TestCase):
    def tearDown(self):
        # to comply with locationiq free tier rate limits
        sleep(1)
