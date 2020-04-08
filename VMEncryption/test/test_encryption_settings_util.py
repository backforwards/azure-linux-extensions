import unittest
import mock
from main import EncryptionSettingsUtil
from main import Common
from StringIO import StringIO
import console_logger

class TestEncryptionSettingsUtil(unittest.TestCase):
    """ unit tests for functions in the check_util module """
    def setUp(self):
        self.logger = console_logger.ConsoleLogger()
        self.es_util = EncryptionSettingsUtil.EncryptionSettingsUtil(self.logger)

    @mock.patch('time.sleep') # To speed up this test.
    @mock.patch('os.path.isfile', return_value=True)
    @mock.patch('main.EncryptionSettingsUtil.EncryptionSettingsUtil.get_http_util')
    def test_post_to_wire_server(self, get_http_util, os_path_isfile,  time_sleep):
        get_http_util.return_value = mock.MagicMock() # Return a mock object
        data = {"Protectors" : "mock data"}

        get_http_util.return_value.Call.return_value.status = 500 # make it so that the http call returns a 500
        self.assertRaises(Exception, self.es_util.post_to_wireserver, data)
        self.assertEqual(get_http_util.return_value.Call.call_count, 3)

        get_http_util.return_value.Call.reset_mock()

        get_http_util.return_value.Call.return_value.status = 400 # make it so that the http call returns a 400
        self.assertRaises(Exception, self.es_util.post_to_wireserver, data)
        self.assertEqual(get_http_util.return_value.Call.call_count, 3)

        get_http_util.return_value.Call.reset_mock()

        get_http_util.return_value.Call.return_value.status = 200 # make it so that the http call returns a 200
        self.es_util.post_to_wireserver(data)
        self.assertEqual(get_http_util.return_value.Call.call_count, 1)

        get_http_util.return_value.Call.reset_mock()

        get_http_util.return_value.Call.return_value = None # Make it so that the HTTP call returns nothing
        self.assertRaises(Exception, self.es_util.post_to_wireserver, data)
        self.assertEqual(get_http_util.return_value.Call.call_count, 3)