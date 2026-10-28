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

    def test_feed_asks_for_sign_in(self):
        response = self.client.get('/neighbourhood/')
        self.assertRedirects(response, '/?next=/neighbourhood/')

    def test_a_member_can_post_a_notice(self):
        user = User.objects.create_user('kamau', 'kamau@example.com', 'pass-word-123')
        area = Neighbourhood.objects.create(owner=user, name='Umoja', location='Nairobi')
        user.profile.neighbourhood = area
        user.profile.save()
        self.client.login(username='kamau', password='pass-word-123')

        response = self.client.post('/neighbourhood/', {
            'post_type': 'news',
            'title': 'Market day',
            'description': 'Saturday market opens at eight.',
        })

        self.assertRedirects(response, '/neighbourhood/')
        self.assertEqual(Post.objects.get(title='Market day').neighbourhood, area)

    def test_a_notice_needs_a_neighbourhood(self):
        user = User.objects.create_user('asha', 'asha@example.com', 'pass-word-123')
        self.client.login(username='asha', password='pass-word-123')
        response = self.client.post('/neighbourhood/', {
            'post_type': 'news',
            'title': 'Market day',
            'description': 'Saturday market opens at eight.',
        })
        self.assertRedirects(response, '/profile/')
        self.assertEqual(Post.objects.filter(title='Market day').count(), 0)
