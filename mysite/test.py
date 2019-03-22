import unittest
from django.test import Client
from PIL import ImageFile

class SimpleTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

        # As we are dealing with images responses
        self.parser = ImageFile.Parser()

    def test_home(self):
        # Issue a GET request to the home page.
        response = self.client.get('')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    """ Testing the url with only the width provided
        Must be in the range 1 to 1920
        Must be PNG
        Must be sized 200 x 200
        Must be RGB format """
    def test_placeholder_width_only(self):
        # Supply a width only in allowed range.
        response = self.client.get('/200/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check the response is a png
        self.assertEqual("image/png", response['Content-Type'])

        # Feed the image Parser and check the width, height and mode.
        self.parser.feed(response.content)
        self.assertEqual(self.parser.image.size[0], 200)
        self.assertEqual(self.parser.image.size[1], 200)
        self.assertEqual(self.parser.image.mode, 'RGB')

    """ Testing width only incorrect values return a 404 """
    def test_fail_placeholder_width_only(self):
        # Supply a rubbish width and response is 404, not found
        response = self.client.get('/ffffff/')
        self.assertEqual(response.status_code, 404)

        # Supply 0px width and response is 404, not found
        response = self.client.get('/0/')
        self.assertEqual(response.status_code, 404)

        # Supply 1921 width and response is 404, not found
        response = self.client.get('/1921/')
        self.assertEqual(response.status_code, 404)

    """ Testing the url with the width and height provided
        Width must be in the range 1 to 1920
        Height must be in the range 1 to 1080
        Must be PNG
        Must be sized 600 x 400
        Must be RGB format """
    def test_placeholder_width_height(self):
        # Supply a width only in allowed range.
        response = self.client.get('/600/400/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check the response is a png
        self.assertEqual("image/png", response['Content-Type'])

        # Feed the image Parser and check the width, height and mode.
        self.parser.feed(response.content)
        self.assertEqual(self.parser.image.size[0], 600)
        self.assertEqual(self.parser.image.size[1], 400)
        self.assertEqual(self.parser.image.mode, 'RGB')

    """ Testing width and height incorrect values return a 404 """
    def test_fail_placeholder_width_height(self):
        # Supply a rubbish width and height and response is 404, not found
        response = self.client.get('/rubbish/rubbish/')
        self.assertEqual(response.status_code, 404)

        # Supply a rubbish width and good height and response is 404, not found
        response = self.client.get('/rubbish/600/')
        self.assertEqual(response.status_code, 404)

        # Supply a good width and rubbish height and response is 404, not found
        response = self.client.get('/400/rubbish/')
        self.assertEqual(response.status_code, 404)

        # Supply 0px width and 0px height response is 404, not found
        response = self.client.get('/0/0/')
        self.assertEqual(response.status_code, 404)

        # Supply 0px width and good height response is 404, not found
        response = self.client.get('/0/400/')
        self.assertEqual(response.status_code, 404)

        # Supply good width and 0px height response is 404, not found
        response = self.client.get('/400/0/')
        self.assertEqual(response.status_code, 404)

        # Supply 1921 width and 1081 height and response is 404, not found
        response = self.client.get('/1921/1081/')
        self.assertEqual(response.status_code, 404)

        # Supply good width and 1081 height and response is 404, not found
        response = self.client.get('/400/1081/')
        self.assertEqual(response.status_code, 404)

        # Supply 1921 width and good height and response is 404, not found
        response = self.client.get('/1921/400/')
        self.assertEqual(response.status_code, 404)

    """ Testing the url with the background color provided
        Must be PNG
        Must be RGB format """
    def test_placeholder_background(self):
        # Supply a width only in allowed range and color in allowed range
        response = self.client.get('/200/aabbcc/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check the response is a png
        self.assertEqual("image/png", response['Content-Type'])

        # Feed the image Parser and check the mode.
        self.parser.feed(response.content)
        self.assertEqual(self.parser.image.mode, 'RGB')

        # Supply a width and height in allowed range and color in allowed range
        response = self.client.get('/200/400/11ffaa/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check the response is a png
        self.assertEqual("image/png", response['Content-Type'])

        # Feed the image Parser and check the mode.
        self.parser.feed(response.content)
        self.assertEqual(self.parser.image.mode, 'RGB')

    """ Testing background incorrect values return a 404 """
    def test_fail_placeholder_background(self):
        # Supply good width and good height and short color, response is 404, not found
        response = self.client.get('/200/400/fff/')
        self.assertEqual(response.status_code, 404)

        # Supply good width and good height and rubish color, response is 404, not found
        response = self.client.get('/200/400/rubish/')
        self.assertEqual(response.status_code, 404)

        # Supply good dimensions and long color hex, response is 404, not found
        response = self.client.get('/200/400/aabbccd/')
        self.assertEqual(response.status_code, 404)

        # Supply good dimensions and long color over hex values, response is 404, not found
        response = self.client.get('/200/400/gggggg/')
        self.assertEqual(response.status_code, 404)

    """ Testing the url with the background and foreground colors provided
        Must be PNG
        Must be RGB format """
    def test_placeholder_background_foreground(self):
        # Supply a width only in allowed range and color in allowed range
        response = self.client.get('/200/123456/789abc/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check the response is a png
        self.assertEqual("image/png", response['Content-Type'])

        # Feed the image Parser and check the mode.
        self.parser.feed(response.content)
        self.assertEqual(self.parser.image.mode, 'RGB')

        # Supply a width and height in allowed range and colors in allowed range
        response = self.client.get('/200/400/11ffaa/0055cc/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check the response is a png
        self.assertEqual("image/png", response['Content-Type'])

        # Feed the image Parser and check the mode.
        self.parser.feed(response.content)
        self.assertEqual(self.parser.image.mode, 'RGB')

    """ Testing background incorrect values return a 404 """
    def test_fail_placeholder_background_foreground(self):
        # Supply good dimensions and short colors response is 404, not found
        response = self.client.get('/200/400/fff/fff/')
        self.assertEqual(response.status_code, 404)

        # Supply good dimensions and good background and short foreground response is 404, not found
        response = self.client.get('/200/400/112233/fff/')
        self.assertEqual(response.status_code, 404)

        # Supply good dimensions and rubish colors response is 404, not found
        response = self.client.get('/200/400/rubish/rubish/')
        self.assertEqual(response.status_code, 404)

        # Supply good dimensions and foreground and rubish background colors response is 404, not found
        response = self.client.get('/200/400/acacac/rubish/')
        self.assertEqual(response.status_code, 404)

    """ Testing the url with the format provided
        Must match format
        Must be RGB format """
    def test_placeholder_format(self):
        # Supply a width only and format in allowed formats
        response = self.client.get('/200/png/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check the response is a png
        self.assertEqual("image/png", response['Content-Type'].lower())

        # Feed the image Parser and check the mode.
        self.parser.feed(response.content)
        self.assertEqual(self.parser.image.mode, 'RGB')

        # Supply with dimension and format in allowed
        response = self.client.get('/200/400/jpg/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check the response is a JPEG
        self.assertEqual("image/jpeg", response['Content-Type'].lower())

        # Feed the image Parser and check the mode.
        self.parser.feed(response.content)
        self.assertEqual(self.parser.image.mode, 'RGB')

        # Supply with dimension and background color and format in allowed
        response = self.client.get('/200/400/ffffff/jpeg/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check the response is a JPEG
        self.assertEqual("image/jpeg", response['Content-Type'].lower())

        # Feed the image Parser and check the mode.
        self.parser.feed(response.content)
        self.assertEqual(self.parser.image.mode, 'RGB')

        # Supply with dimension and colors and format in allowed
        response = self.client.get('/200/400/ffffff/000000/pcx/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check the response is a JPEG
        self.assertEqual("image/pcx", response['Content-Type'].lower())

        # Feed the image Parser and check the mode.
        self.parser.feed(response.content)
        self.assertEqual(self.parser.image.mode, 'RGB')

        # Supply with width and colors and format in allowed
        response = self.client.get('/200/ffffff/000000/gif/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check the response is a JPEG
        self.assertEqual("image/gif", response['Content-Type'].lower())

        # Feed the image Parser and check the mode.
        self.parser.feed(response.content)
        self.assertEqual(self.parser.image.mode, 'RGB')

        # Supply with width and background color and format in allowed
        response = self.client.get('/200/ffffff/bmp/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check the response is a JPEG
        self.assertEqual("image/bmp", response['Content-Type'].lower())

        # Feed the image Parser and check the mode.
        self.parser.feed(response.content)
        self.assertEqual(self.parser.image.mode, 'RGB')

    """ Testing format incorrect values return a 404 """
    def test_fail_placeholder_format(self):
        # Supply good dimensions and good colors with rubbish format, response is 404, not found
        response = self.client.get('/200/400/ffffff/000000/rubbish/')
        self.assertEqual(response.status_code, 404)

        # Supply good dimensions and good colors with unsuported format, response is 404, not found
        response = self.client.get('/200/400/ffffff/000000/tiff/')
        self.assertEqual(response.status_code, 404)

    """ To improve coverage, test cases that are not normall """
    def test_unusual_dimensions(self):
        # Supply very small dimensions, stops text from appearing.
        response = self.client.get('/10/15/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check the response is a png
        self.assertEqual("image/png", response['Content-Type'])

        # Feed the image Parser and check the width, height and mode.
        self.parser.feed(response.content)
        self.assertEqual(self.parser.image.size[0], 10)
        self.assertEqual(self.parser.image.size[1], 15)
        self.assertEqual(self.parser.image.mode, 'RGB')
