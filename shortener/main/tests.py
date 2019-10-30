from django.test import TestCase
from main.models import URL, Visit
from django.db import IntegrityError
from django.utils import timezone

class URLTestCase(TestCase):
    def setUp(self):
        random = URL.objects.create(
            short_url="iBgE",
            long_url="http://reddit.com",
            create_time = timezone.now(),
            custom=False
        )
        custom = URL.objects.create(
            short_url="abcd",
            long_url="http://reddit.com",
            create_time = timezone.now(),
            custom=True
        )

    def test_allows_multiple_custom(self):
        customURL = URL.objects.get(long_url="http://reddit.com", custom=True)
        new = URL.objects.create(
            short_url="rdt",
            long_url=customURL.long_url,
            create_time=timezone.now(),
            custom=customURL.custom
        )
        self.assertEqual(new.id, new.id)

    def test_rejects_duplicate_short(self):
        try:
            URL.objects.create(
                short_url="abcd",
                long_url="http://wikipedia.com",
                create_time = timezone.now(),
                custom=True
            )
            self.fail("Should prohibit creation due to non-unique short_url")
        except IntegrityError:
            pass
    
    def test_allows_only_one_random_per_long(self):
        try:
            URL.objects.create(
                short_url="xyza",
                long_url="http://reddit.com",
                create_time = timezone.now(),
                custom=False
            )
            self.fail("Should prohibit creation because a randomly generated short_url already exists for that long_url")
        except IntegrityError:
            pass
