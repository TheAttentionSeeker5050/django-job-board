from django.test import TestCase

# import model
from users.models import CustomUser
from resumes.models import JobApplicant

# use django test client
from django.test import Client

from .permissions import isOwnerOfObject

# test cases for permissions method
class PermissionsTests(TestCase):
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
    def test_user_of_resume_is_logged_in_and_owner(self):
        # create a user
        user = self.user

        # create a resume
        resume = JobApplicant.objects.create(
            title='test resume',
            resume_file='testfile.pdf',
            user_owner=user
        )

        # get the resume from database
        retrieved_resume = JobApplicant.objects.get(title='test resume')

        # assert not empty retrieved resume
        self.assertIsNotNone(retrieved_resume)

        # get the resume user owner
        resume_user_owner = retrieved_resume.user_owner

        client = Client()

        response = client.post("/login/", {
            "username": "testuser",
            "password": "testpassword"
        })

        # create the self request object, so it emulates the self.request object in a view
        new_self = type('obj', (object,), {
            'request': type('obj', (object,), {
                'user': user
            })
        })


        # now use the permissions method and save response to var
        permission_return_val = isOwnerOfObject(new_self, resume_user_owner)

        # assert the permission return value is true
        self.assertTrue(permission_return_val)
