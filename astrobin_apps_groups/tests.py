# Django
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

# This app
from astrobin_apps_groups.models import Group

# Other AstroBin apps
from astrobin_apps_notifications.utils import get_unseen_notifications


class GroupsTest(TestCase):
    def _assertMessage(self, response, tags, content):
        messages = response.context[0]['messages']

        if len(messages) == 0:
            self.assertEqual(False, True)

        for message in messages:
            self.assertEqual(message.tags, tags)
            self.assertTrue(content in message.message)

    def setUp(self):
        self.user1 = User.objects.create_user('user1', 'user1@test.com', 'password')
        self.user2 = User.objects.create_user('user2', 'user2@test.com', 'password')
        self.group = Group.objects.create(
            creator = self.user1,
            owner = self.user1,
            name = 'Test group',
            category = 101,
            public = True,
        )

    def tearDown(self):
        self.user1.delete()
        self.user2.delete()
        self.group.delete()

    def test_public_group_list_view(self):
        response = self.client.get(reverse('public_group_list'))
        self.assertEqual(response.status_code, 200)

    def test_group_detail_view(self):
        response = self.client.get(reverse('group_detail', kwargs = {'pk': self.group.pk}))
        self.assertEqual(response.status_code, 200)

        self.group.public = False
        self.group.save()
        response = self.client.get(reverse('group_detail', kwargs = {'pk': self.group.pk}))
        self.assertEqual(response.status_code, 403)

        # Restore previous state
        self.group.public = True
        self.group.save()

    def test_group_create_view(self):
        url = reverse('group_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.client.login(username = 'user1', password = 'password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(url, {
            'name': 'Test create group',
            'description': 'Description',
            'category': 101,
            'public': True,
            'moderated': True,
        }, follow = True)
        self.assertEqual(response.status_code, 200)
        self._assertMessage(response, "success unread", "Your new group was created successfully")
        group = Group.objects.all().order_by('pk')[1]
        self.assertEqual(group.creator, self.user1)
        self.assertEqual(group.owner, self.user1)
        self.assertEqual(group.name, 'Test create group')
        self.assertEqual(group.description, 'Description')
        self.assertEqual(group.category, 101)
        self.assertEqual(group.public, True)
        self.assertEqual(group.moderated, True)

        group.delete()
        self.client.logout()

    def test_group_update_view(self):
        url = reverse('group_update', kwargs = {'pk': self.group.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.client.login(username = 'user2', password = 'password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.client.logout()

        self.client.login(username = 'user1', password = 'password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(url, {
            'name': 'Updated group name',
            'description': 'Updated group description',
            'category': 1,
            'public': False,
            'moderated': True,
        }, follow = True)
        self._assertMessage(response, "success unread", "Form saved")
        self.group = Group.objects.get(pk = self.group.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.group.name, 'Updated group name')
        self.assertEqual(self.group.description, 'Updated group description')
        self.assertEqual(self.group.category, 1)
        self.assertEqual(self.group.public, False)
        self.assertEqual(self.group.moderated, True)

        # Restore previous group data
        self.group.name = 'Test group'
        self.group.description = None
        self.group.category = 101
        self.group.public = True
        self.group.moderated = False
        self.group.save()

        self.client.logout()

    def test_group_join_view(self):
        url = reverse('group_join', kwargs = {'pk': self.group.pk})

        # Login required
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

        self.client.login(username = 'user1', password = 'password')

        # GET not allowed
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)

        # Group does not exist
        response = self.client.post(reverse('group_join', kwargs = {'pk': 999}), follow = True)
        self.assertEqual(response.status_code, 404)

        # Private group, uninvited user
        self.group.public = False; self.group.save()
        response = self.client.post(url, follow = True)
        self.assertEqual(response.status_code, 403)
        self.group.public = True; self.group.save()

        # Join successful
        response = self.client.post(url, follow = True)
        self.assertEqual(response.status_code, 200)
        self._assertMessage(response, "success unread", "You have joined the group")
        self.assertTrue(self.user1 in self.group.members.all())

        # Second attempt results in error "already joined"
        response = self.client.post(url, follow = True)
        self.assertEqual(response.status_code, 200)
        self._assertMessage(response, "error unread", "You already were a member of this group")
        self.group.members.remove(self.user1)

        # If the group is not public, only invited members can join
        self.group.public = False; self.group.save()

        response = self.client.post(url, follow = True)
        self.assertEqual(response.status_code, 403)

        self.group.invited_users.add(self.user1)

        response = self.client.post(url, follow = True)
        self.assertEqual(response.status_code, 200)
        self._assertMessage(response, "success unread", "You have joined the group")
        self.assertTrue(self.user1 in self.group.members.all())

        # Restore group state
        self.group.invited_users.remove(self.user1)
        self.group.members.remove(self.user1)
        self.group.public = True
        self.group.save()

        self.client.logout()