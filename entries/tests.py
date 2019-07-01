#!/usr/bin/env/ python
# Tests for Entries App

from django.test import TestCase, SimpleTestCase
from django.utils import timezone
from entries.models import Entry
from django.urls import reverse
from entries.forms import EntryForm


def setUp(self):
    self.user = get_user_model().objects.create(username='my_username')

# Tests for Templates


class HomePageTest(SimpleTestCase):
    """ Tests for home page"""

    def test_index_page_status_code(self):
        # Test for home page
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)

    def test_index_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_home_page_contains_correct_title(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, '<title>My Diary</title>')

    def test_home_page_does_not_contain_incorrect_html(self):
        response = self.client.get(reverse('home'))
        self.assertNotContains(
            response, 'This is no not supposed to be here, man!!!')

    def test_create_entry_status_code(self):
        # Test for create entry form/page
        response = self.client.get(reverse('create'))
        self.assertEqual(response.status_code, 302)

    def test_create_view_uses_correct_template(self):
        response = self.client.get(reverse('create'))
        self.assertEquals(response.status_code, 302)
        self.assertTemplateUsed(response, 'create_entry.html')

    def test_create_entry_page_contains_correct_title(self):
        response = self.client.get(reverse('create'))
        self.assertContains(response, '<h1>New Record</h1>')

    def test_create_entry_page_does_not_contain_incorrect_html(self):
        response = self.client.get(reverse('create'))
        self.assertNotContains(
            response, 'This is no not supposed to be here, man!!!')

    def test_entries(self):
        # Test for entries page
        response = self.client.get(reverse('entries'))
        self.assertEqual(response.status_code, 302)

    def test_entry_details(self):
        # Tes for entry details page
        response = self.client.get(reverse('details'))
        self.assertEqual(response.status_code, 200)

    def test_update_entry(self):
        # Test for entry update page
        response = self.client.get(reverse('update'))
        self.assertEqual(response.status_code, 201)

# Tests for model


class EntryModelTest(TestCase):
    """ Test model class"""

    # Create the test model
    def create_entry(self, title='Teremi', event='I love my home'):
        return Entry.objects.create(title=title, event=event, date_posted=timezone.now())

    def test_entry_creation(self):
        # Test the creation of the Entry model
        entry = self.create_entry()
        self.assertTrue(isinstance(entry, Entry))

    def test_string_representation(self):
        entry = Entry(title="My entry title")
        self.assertEqual(str(entry), entry.title)

    def test_verbose_name_plural(self):
        self.assertEqual(str(Entry._meta.verbose_name_plural), "entries")

# Tests for Views


class EntryViewTest(TestCase):
	""" Tests for views """
	def setUp(self):
		Entry.objects.create(author='Joe', title='Test Title', event='I like it!!!', date_posted='01/07/2019, 10:54:30')

	def test_text_content(self):
		entry = Entry.objects.get(id=1)
		expected_object_name = f'{entry.title}'
		self.assertEquals(expected_object_name, 'Test Title')

	def test_get_entries(self):
		response = self.client.get(reverse('entries'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Joe', 'Test Title', 'I like it!!!', '01/07/2019, 10:54:30')
		self.assertTemplateUsed(response, 'entries.html')
"""
	def test_create_entry(self):
		# Test for create view
		self.client.post('/create', {'author':"Joe", 'title':"Teremi", 'event':"I like it.", 'date_posted': timezone.now()})
		self.assertEqual(Entry.objects.last().title, "Teremi")
"""

# Form tests


def test_valid_data(self):
    # Test for valid data
    form = EntryForm({
        'title': "Entry Test Title",
        'event': "Entry Test Event"
    }, entry=self.entry)

    self.assertTrue(form.is_valid())
    my_entry = form.save()
    self.assertEqual(my_entry.title, "Entry Test Title")
    self.assertEqual(my_entry.event, "Entry Test Event")
    self.assertEqual(my_entry.entry, self.entry)


def test_blank_data(self):
    # Test for blank data fields errors
    form = EntryForm({}, entry=self.entry)
    self.assertFalse(form.is_valid())
    self.assertEqual(form.errors, {
        'title': ['required'],
        'event': ['required'],
    })


if __name__ == '__main__':
    unittest.main()
