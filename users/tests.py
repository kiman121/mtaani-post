from django.test import TestCase


class LoginPageTests(TestCase):
    def test_sign_in_page_names_the_product(self):
        response = self.client.get("/")
        self.assertContains(response, "Mtaani")
        self.assertContains(response, "Sign in")

    def test_unknown_account_gets_one_message(self):
        response = self.client.post("/", {"username": "missing", "password": "nope-nope"})
        self.assertContains(response, "Username or password is incorrect.")
        self.assertNotContains(response, "Wrong username")
