from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase

from neighbourhoods.models import Neighbourhood, Post


class NeighbourhoodPostTests(TestCase):
    def test_a_post_is_stored_on_its_neighbourhood(self):
        user = User.objects.create_user('ada', 'ada@example.com', 'pass-word-123')
        area = Neighbourhood.objects.create(owner=user, name='Umoja', location='Nairobi')
        Post.objects.create(
            owner=user,
            title='Water rate',
            description='The quarterly rate is unchanged.',
            neighbourhood=area,
            post_type='announcement',
        )

        stored = Post.objects.get(title='Water rate')
        self.assertEqual(stored.neighbourhood, area)
        self.assertEqual(stored.post_type, 'announcement')
        self.assertEqual(user.profile.email, 'ada@example.com')
        self.assertEqual(len(mail.outbox), 1)
