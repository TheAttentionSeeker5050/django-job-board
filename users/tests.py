from django.test import TestCase
# import model
from .models import CustomUser

# use django test client
from django.test import Client

# import auth hasher
from django.contrib.auth.hashers import check_password




# Create your tests here.
class UserModelTests(TestCase):
    # set up the database for testing
    def setUp(self):
        # create a user
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='testpassword'
        )

    # after each test, delete the database
    def tearDown(self):
        self.user.delete()


    # the tests -------------------------------------------

    # test create user and retrieve email
    def test_create_user(self):
        # create a user
        user = CustomUser.objects.create_user(
            username='testuser2',
            email='testtestuser2@email.com',
            password='testpassword2'
        )

        # get the user email and assert exist and correct email
        user_email = user.email
        self.assertIsNotNone(user_email)
        self.assertEqual(user_email, 'testtestuser2@email.com')

    # create another complete profile and assert added data
    def test_create_complete_user(self):

        # variables to compare
        compare_username = 'testuser2'
        compare_email = 'testtestuser2@email.com'
        compare_password = 'testpassword2'
        compare_first_name = 'test'
        compare_last_name = 'user2'

        # create a user
        user = CustomUser.objects.create_user(
            username='testuser2',
            email='testtestuser2@email.com',
            password='testpassword2',
            first_name='test',
            last_name='user2',
        )

        # retrieve user object
        retrieved_user = CustomUser.objects.get(username='testuser2')

        # check password comparing retrieved user hash and the compare password
        passwordIsSame = check_password(compare_password, retrieved_user.password)

        # assert password is same
        self.assertTrue(passwordIsSame)

        # assert user data
        self.assertEqual(retrieved_user.username, compare_username)
        self.assertEqual(retrieved_user.email, compare_email)
        
        self.assertEqual(retrieved_user.first_name, compare_first_name)
        self.assertEqual(retrieved_user.last_name, compare_last_name)


class UserViewTests(TestCase):
    # set up the database for testing
    def setUp(self):
        # create a user
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='testpassword'
        )

    # after each test, delete the database
    def tearDown(self):
        self.user.delete()

    def test_register_view(self):
        # create a test client
        client = Client()

        # create a post request
        response = client.post('/register/', {
            'username': 'testuser2',
            'email': 'testuser2@email.com',
            'password1': 'testpassword2',
            'password2': 'testpassword2',
        })

        # test response created
        self.assertEqual(response.status_code, 302)

        # test user created
        user = CustomUser.objects.get(username='testuser2')

        # test user email
        self.assertEqual(user.email, 'testuser2@email.com')

        # test login with new email
        client.post('/login/', {
            'username': 'testuser2',
            'password': 'testpassword2',
        })

        # test response ok
        self.assertEqual(response.status_code, 302)

    def test_invalid_data_register_view(self):
        # create a test client
        client = Client()

        # create a post request
        response = client.post('/register/', {
            'username': 'testuser2',
            'email': 'testuser2email.com',
            'password1': 'testpassword2',
            'password2': 'testpassword2',
        })

        # test user created does not exist in the database
        with self.assertRaises(CustomUser.DoesNotExist):
            CustomUser.objects.get(username='testuser2')

        # create a login request response
        response2 = client.post('/login/', {
            'username': 'testuser2',
            'password': 'testpassword2',
        })

        # test if form error, invalid credentials
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')

    def test_user_already_exists_register_view(self):
        # create a test client
        client = Client()

        # create a post request
        response = client.post('/register/', {
            'username': 'testuser2',
            'email': 'testuser@email.com',
            'password1': 'testpassword2',
            'password2': 'testpassword2',
        })

        
        response2 = client.post('/register/', {
            'username': 'testuser2',
            'email': 'testuser2@email.com',
            'password1': 'testpassword2',
            'password2': 'testpassword2',
        })

        # check if response was redirected back to register page
        self.assertEqual(response2.status_code, 200)
        self.assertFormError(response2, 'form', 'username', 'A user with that username already exists.')

