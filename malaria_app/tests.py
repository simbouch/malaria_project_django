from django.test import TestCase

from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
import os

class MalariaAppTests(TestCase):
    def setUp(self):
        """
        Set up a test client to make requests to the application.
        """
        self.client = Client()

    def test_index_view(self):
        """
        Test the index view to ensure it returns a 200 status code.
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Malaria Prediction")  # Check if the title is rendered

    def test_upload_view_get(self):
        """
        Test the upload view for GET requests to ensure it returns a 200 status code.
        """
        response = self.client.get(reverse('upload'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Upload an Image")  # Check if the form is rendered

    def test_upload_view_post(self):
        """
        Test the upload view for POST requests with an image.
        """
        # Simulate an uploaded image
        test_image_path = os.path.join(os.path.dirname(__file__), 'test_image.png')
        with open(test_image_path, 'wb') as f:  # Create a small dummy image
            f.write(b'\x89PNG\r\n\x1a\n')

        with open(test_image_path, 'rb') as img:
            image_file = SimpleUploadedFile("test_image.png", img.read(), content_type="image/png")
            response = self.client.post(reverse('upload'), {'image': image_file})

        # Clean up the dummy image
        os.remove(test_image_path)

        self.assertEqual(response.status_code, 302)  # Should redirect to result
        self.assertIn(reverse('result'), response.url)  # Check if it redirects to result

    def test_result_view(self):
        """
        Test the result view to ensure it displays the prediction result.
        """
        response = self.client.get(reverse('result'), {'prediction': 'Saine'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The uploaded image is:")
        self.assertContains(response, "Saine")
