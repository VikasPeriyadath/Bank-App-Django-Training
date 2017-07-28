from django.test import TestCase

from .views import *


class SetupClass(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='Jithu')
        self.user.set_password('monachavikas')
        self.user.save()
        self.bank = Bank.objects.create(
            branch_name='koramangala',
            ifsc_code='FEDKOR66565562',
            branch_address='1st Main, 3rd cross , Jakkasandra',
            branch_contact=22036984
        )


class LoginTest(SetupClass):
    csrf_checks = False

    def test_valid_login(self):
        user_login = self.client.login(
            username="Jithu",
            password="monachavikas",
        )
        print(user_login)
        self.assertTrue(user_login)
        response = self.client.post('/Bankpro/')
        self.assertEqual(response.status_code, 302)

    def test_invalid_login(self):
        user_login = self.client.login(username="J", password="monachavikas")
        print(user_login)
        self.assertFalse(user_login)
        response = self.client.post("/Bankpro/")
        self.assertEqual(response.status_code, 200)


class AddBankTest(SetupClass):
    def invalid_bank(self):
        f = BankForm(data={
            'branch_name': 'koramangala',
            'ifsc_code': 'FEDKOR66565562',
            'branch_address': '1st Main, 3rd cross , Jakkasandra',
            'branch_contact': 22036984
        })
        self.failIf(f.is_valid())
        print(f.errors)

    def valid_bank(self):
        f = BankForm(data={
            'branch_name': 'kasaba',
            'ifsc_code': 'FEDKOR6656558988',
            'branch_address': 'Jakkasandra',
            'branch_contact': 22036984
        })
        self.assertTrue(f.is_valid())

    def valid_bank_submission(self):
        self.client.login(
            username="Jithu",
            password="monachavikas",
        )
        response = self.client.post(reverse('addBank'), data={
            'branch_name': 'kasaba',
            'ifsc_code': 'FEDKOR6656558988',
            'branch_address': 'Jakkasandra',
            'branch_contact': 22036984
        })
        self.assertTrue(response)
        self.assertEqual(Bank.objects.count(), 2)
        self.assertTemplateUsed(response, 'success.html')