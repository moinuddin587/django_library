import datetime
from django.test import TestCase
from catalog.forms import BookRenewForm
from django.utils import timezone


class BookRenewFormTest(TestCase):
    def test_date_field_lebel(self):
        form = BookRenewForm()
        field_label = form.fields['renewal_date'].label
        self.assertTrue(field_label is None or field_label == 'renewal_date')
    
    def test_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = BookRenewForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())

    def test_date_in_too_far(self):
        date = datetime.date.today() +datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
        form = BookRenewForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())
    
    def test_date_today(self):
        date = datetime.date.today()
        form = BookRenewForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())

    def test_date_max(self):
        date = timezone.localtime() + datetime.timedelta(weeks=4)
        form = BookRenewForm(data={'renewal_data': date})
        self.assertTrue(form.is_valid())

    def test_help_text(self):
        form = BookRenewForm()
        field_label_text = form.fields['renewal_date'].help_text
        self.assertEqual(field_label_text, "Enter a date between now and 4 weeks (default 3).")