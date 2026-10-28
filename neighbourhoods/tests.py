from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase

from neighbourhoods.models import Business, Contact, Neighbourhood, Post


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

    def test_anonymous_visitor_reads_the_sample(self):
        response = self.client.get('/')
        self.assertContains(response, 'Kileleshwa')
        self.assertContains(response, 'Water interruption on Thursday')
        self.assertContains(response, 'Sign in')
        self.assertNotContains(response, 'Post notice')

    def test_a_member_can_post_a_notice(self):
        user = User.objects.create_user('kamau', 'kamau@example.com', 'pass-word-123')
        area = Neighbourhood.objects.create(owner=user, name='Umoja', location='Nairobi')
        user.profile.neighbourhood = area
        user.profile.save()
        self.client.login(username='kamau', password='pass-word-123')

        response = self.client.post('/', {
            'post_type': 'news',
            'title': 'Market day',
            'description': 'Saturday market opens at eight.',
        })

        self.assertRedirects(response, '/')
        self.assertEqual(Post.objects.get(title='Market day').neighbourhood, area)

    def test_only_the_author_can_change_a_notice(self):
        author = User.objects.create_user('kamau', 'kamau@example.com', 'pass-word-123')
        other = User.objects.create_user('asha', 'asha@example.com', 'pass-word-123')
        area = Neighbourhood.objects.create(owner=author, name='Umoja', location='Nairobi')
        post = Post.objects.create(
            owner=author,
            title='Market day',
            description='Saturday market opens at eight.',
            neighbourhood=area,
            post_type='news',
        )
        self.client.login(username='asha', password='pass-word-123')
        denied = self.client.post(f'/neighbourhood/notices/{post.id}/edit/', {
            'post_type': 'news',
            'title': 'Changed',
            'description': 'Nope.',
        })
        self.assertEqual(denied.status_code, 403)
        self.client.login(username='kamau', password='pass-word-123')
        updated = self.client.post(f'/neighbourhood/notices/{post.id}/edit/', {
            'post_type': 'news',
            'title': 'Market day moved',
            'description': 'It opens at nine.',
        })
        self.assertRedirects(updated, '/')
        post.refresh_from_db()
        self.assertEqual(post.title, 'Market day moved')

    def test_a_resident_can_remove_a_contact(self):
        user = User.objects.create_user('kamau', 'kamau@example.com', 'pass-word-123')
        outsider = User.objects.create_user('asha', 'asha@example.com', 'pass-word-123')
        area = Neighbourhood.objects.create(owner=user, name='Umoja', location='Nairobi')
        elsewhere = Neighbourhood.objects.create(owner=outsider, name='South B', location='Nairobi')
        user.profile.neighbourhood = area
        user.profile.save()
        outsider.profile.neighbourhood = elsewhere
        outsider.profile.save()
        contact = Contact.objects.create(
            neighbourhood=area,
            name='Clinic',
            phone_number='0700',
            category='health',
        )
        self.client.login(username='asha', password='pass-word-123')
        denied = self.client.post(f'/neighbourhood/contacts/{contact.id}/delete/')
        self.assertEqual(denied.status_code, 403)
        self.client.login(username='kamau', password='pass-word-123')
        removed = self.client.post(f'/neighbourhood/contacts/{contact.id}/delete/')
        self.assertRedirects(removed, '/')
        self.assertFalse(Contact.objects.filter(pk=contact.id).exists())

    def test_a_new_neighbourhood_becomes_yours(self):
        user = User.objects.create_user('kamau', 'kamau@example.com', 'pass-word-123')
        self.client.login(username='kamau', password='pass-word-123')
        response = self.client.post('/neighbourhood/neighbourhood-list/', {
            'action': 'neighbourhood',
            'area-name': 'South B',
            'area-location': 'Nairobi',
        })
        self.assertRedirects(response, '/')
        user.profile.refresh_from_db()
        self.assertEqual(user.profile.neighbourhood.name, 'South B')

    def test_residents_are_limited_to_your_neighbourhood(self):
        user = User.objects.create_user('kamau', 'kamau@example.com', 'pass-word-123')
        other = User.objects.create_user('asha', 'asha@example.com', 'pass-word-123')
        area = Neighbourhood.objects.create(owner=user, name='Umoja', location='Nairobi')
        elsewhere = Neighbourhood.objects.create(owner=other, name='South B', location='Nairobi')
        user.profile.neighbourhood = area
        user.profile.first_name = 'Kamau'
        user.profile.save()
        other.profile.neighbourhood = elsewhere
        other.profile.first_name = 'Asha'
        other.profile.save()
        self.client.login(username='kamau', password='pass-word-123')
        response = self.client.get('/users/')
        self.assertContains(response, 'Kamau')
        self.assertNotContains(response, 'Asha')

    def test_a_business_keeps_a_phone_and_description(self):
        user = User.objects.create_user('kamau', 'kamau@example.com', 'pass-word-123')
        area = Neighbourhood.objects.create(owner=user, name='Umoja', location='Nairobi')
        user.profile.neighbourhood = area
        user.profile.save()
        self.client.login(username='kamau', password='pass-word-123')
        response = self.client.post('/neighbourhood/business-list/', {
            'name': 'Corner shop',
            'description': 'Bread and milk until eight.',
            'phone_number': '0711000111',
            'email': 'shop@example.com',
        })
        self.assertRedirects(response, '/neighbourhood/business-list/')
        business = Business.objects.get(name='Corner shop')
        self.assertEqual(business.phone_number, '0711000111')
        self.assertEqual(business.description, 'Bread and milk until eight.')

    def test_a_notice_needs_a_neighbourhood(self):
        user = User.objects.create_user('asha', 'asha@example.com', 'pass-word-123')
        self.client.login(username='asha', password='pass-word-123')
        response = self.client.post('/', {
            'post_type': 'news',
            'title': 'Market day',
            'description': 'Saturday market opens at eight.',
        })
        self.assertRedirects(response, '/profile/')
        self.assertEqual(Post.objects.filter(title='Market day').count(), 0)
