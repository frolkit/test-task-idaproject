from django.test import Client, TestCase
from django.core.files.uploadedfile import SimpleUploadedFile


class TestData(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        image = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.image_file = SimpleUploadedFile(name='img.jpeg',
                                            content=image,
                                            content_type='image/jpeg')
        cls.image_link = 'https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png' # noqa
        cls.invalid_image_link = 'https://www.google.com/'


class ImageCreateErrors(TestData):

    def test_upload_with_invalid_link(self):
        response = self.client.post('/image_create/',
                                    {'image_link': self.invalid_image_link})
        self.assertContains(response, "не получилось найти изображение")

    def test_upload_with_no_input(self):
        response = self.client.post('/image_create/', {'image_link': ''})
        self.assertContains(response, 'Не указан вариант загрузки.')

    def test_upload_with_two_input(self):
        response = self.client.post('/image_create/',
                                    {'image_link': self.image_link,
                                     'image_file': self.image_file})
        self.assertContains(response, 'Укажите только один вариант загрузки.')


class ImageCreate(TestData):

    def test_upload_image_from_link(self):
        response = self.client.post('/image_create/',
                                    {'image_link': self.image_link})
        self.assertEqual(response.status_code, 302)

    def test_upload_image_from_file(self):
        response = self.client.post('/image_create/',
                                    {'image_file': self.image_file})
        self.assertEqual(response.status_code, 302)


class ImageEdit(TestData):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client.post('/image_create/',
                        {'image_file': cls.image_file},
                        follow=True)

    def test_edit_width(self):
        response = self.client.post('/image_edit/1/',
                                    {'width': 1920},
                                    follow=True)
        edited_image = response.context['image']
        width, height = edited_image.size
        self.assertEqual(width, 1920)

    def test_edit_height(self):
        response = self.client.post('/image_edit/1/',
                                    {'height': 1080},
                                    follow=True)
        edited_image = response.context['image']
        width, height = edited_image.size
        self.assertEqual(height, 1080)

    def test_edit_width_and_height(self):
        response = self.client.post('/image_edit/1/',
                                    {'width': 1920,
                                     'height': 1080},
                                    follow=True)
        edited_image = response.context['image']
        width, height = edited_image.size
        self.assertEqual(width, 1920)
        self.assertEqual(height, 1080)
