'''This is the unit test file for the google_api.py file.'''

import unittest
import google_api
from apiclient import errors

class Request():
    def __init__(self):
        self.count = 0

    def execute(self):
        self.count += 1
        return {}

    def get_count(self):
        return self.count

class RequestHTTP(Request):
    def execute(self):
        self.count += 1
        raise errors.HttpError('Test error', b'HTTP/1.1 404 Not Found.')

class RequestApps(Request):
    def execute(self):
        self.count += 1
        return {'error': {'details': ['Test error']}}

class TestGeneralMethods(unittest.TestCase):
    def test_try_request_n_retries(self):
        req = Request()
        res = google_api.try_request_n_retries(req, 5)
        self.assertEqual(res, {})
        self.assertEqual(req.get_count(), 1)

    def test_try_request_n_retries_http_error(self):
        req = RequestHTTP()
        self.assertRaises(errors.HttpError, google_api.try_request_n_retries, req, 5, retry_time=0)
        self.assertEqual(req.get_count(), 5)

    def test_try_request_n_retries_appsscript_error(self):
        req = RequestApps()
        self.assertRaises(google_api.AppsScriptError, google_api.try_request_n_retries, req, 5, retry_time=0)
        self.assertEqual(req.get_count(), 5)

    def test_column_number_to_letter(self):
        tests = [(1,'A'),(2,'B'),(3,'C'),(27,'AA'),(28,'AB'),(703,'AAA')]
        for test in tests:
            self.assertEqual(google_api.column_number_to_letter(test[0]), test[1])

    def test_get_a1_notation(self):
        a1_t = google_api.get_a1_notation('sheet_name', 1, 1, 2, 2)
        a1 = "'sheet_name'!A1:B2"
        self.assertEqual(a1, a1_t)

class TestServicesMethods(unittest.TestCase):
    def setUp(self):
        self.drive = 'drive_service'
        self.sheets = 'sheets_service'
        self.appsscript = 'appsscript_service'
        self.service = google_api.Services(self.drive, self.sheets, self.appsscript)

    def tearDown(self):
        del self.drive
        del self.sheets
        del self.appsscript
        del self.service

    def test_drive(self): #Vrrrooooomm!
        self.assertEqual(self.drive, self.service.drive())

    def test_sheets(self):
        self.assertEqual(self.sheets, self.service.sheets())

    def test_appsscript(self):
        self.assertEqual(self.appsscript, self.service.appsscript())

class TestCacheMethods(unittest.TestCase):
    def setUp(self):
        self.name = 'name'
        self.value = 'value'

        self.empty_cache = google_api.Cache()

        self.valid_cache = google_api.Cache()
        self.valid_cache.set_value(self.name, self.value)

        self.invalid_cache = google_api.Cache()
        self.invalid_cache.set_value(self.name, self.value)
        self.invalid_cache.timeout_var(self.name)

    def tearDown(self):
        del self.name
        del self.value

        del self.empty_cache

        del self.valid_cache

        del self.invalid_cache

    def test_is_fresh(self):
        self.assertFalse(self.empty_cache.is_fresh(self.name))
        self.assertTrue(self.valid_cache.is_fresh(self.name))
        self.assertFalse(self.invalid_cache.is_fresh(self.name))

    def test_set_value(self):
        self.empty_cache.set_value(self.name, self.value)
        self.assertIn(self.name, self.empty_cache.cache)
        self.assertEqual(self.empty_cache.cache[self.name], (True, self.value))

        self.valid_cache.set_value(self.name, self.value)
        self.assertIn(self.name, self.valid_cache.cache)
        self.assertEqual(self.valid_cache.cache[self.name], (True, self.value))

        self.invalid_cache.set_value(self.name, self.value)
        self.assertIn(self.name, self.invalid_cache.cache)
        self.assertEqual(self.invalid_cache.cache[self.name], (True, self.value))

    def test_get_value(self):
        value = self.empty_cache.get_value(self.name)
        self.assertIsNone(value)

        value = self.valid_cache.get_value(self.name)
        self.assertEqual(value, self.value)

        value = self.invalid_cache.get_value(self.name)
        self.assertIsNone(value)

    def test_timeout_var(self):
        self.empty_cache.timeout_var(self.name)
        self.assertNotIn(self.name, self.empty_cache.cache)

        self.valid_cache.timeout_var(self.name)
        self.assertIn(self.name, self.valid_cache.cache)
        self.assertEqual(self.valid_cache.cache[self.name], (False, self.value))

        self.invalid_cache.timeout_var(self.name)
        self.assertIn(self.name, self.invalid_cache.cache)
        self.assertEqual(self.invalid_cache.cache[self.name], (False, self.value))

class TestFormLocationMethods(unittest.TestCase):
    def setUp(self):
        self.form_id_1 = 'form id # 1'
        self.form_id_2 = 'form id # 2'
        self.response_id_1 = 'response id # 1'
        self.response_id_2 = 'response id # 2'

        self.loc_1_1 = google_api.FormLocation(self.form_id_1, self.response_id_1)
        self.loc_1_2 = google_api.FormLocation(self.form_id_1, self.response_id_2)
        self.loc_2_1 = google_api.FormLocation(self.form_id_2, self.response_id_1)
        self.loc_2_2 = google_api.FormLocation(self.form_id_2, self.response_id_2)

    def tearDown(self):
        del self.form_id_1
        del self.form_id_2
        del self.response_id_1
        del self.response_id_2

        del self.loc_1_1
        del self.loc_1_2
        del self.loc_2_1
        del self.loc_2_2

    def test_init(self):
        maybe_loc = google_api.FormLocation(self.form_id_1, self.response_id_1)
        self.assertTrue(isinstance(maybe_loc, google_api.FormLocation))

    def test_init_fail_no_form_id(self):
        with self.assertRaises(TypeError):
            maybe_loc = google_api.FormLocation(None, self.response_id_1)

    def test_init_fail_no_response_id(self):
        with self.assertRaises(TypeError):
            maybe_loc = google_api.FormLocation(self.form_id_1, None)

    def test_get_form_id(self):
        self.assertEqual(self.loc_1_1.get_form_id(), self.form_id_1)
        self.assertEqual(self.loc_1_2.get_form_id(), self.form_id_1)
        self.assertEqual(self.loc_2_1.get_form_id(), self.form_id_2)
        self.assertEqual(self.loc_2_2.get_form_id(), self.form_id_2)

    def test_get_response_id(self):
        self.assertEqual(self.loc_1_1.get_response_id(), self.response_id_1)
        self.assertEqual(self.loc_1_2.get_response_id(), self.response_id_2)
        self.assertEqual(self.loc_2_1.get_response_id(), self.response_id_1)
        self.assertEqual(self.loc_2_2.get_response_id(), self.response_id_2)

    def test_compare(self):
        self.assertTrue(self.loc_1_1.compare(self.loc_1_1))
        self.assertFalse(self.loc_1_1.compare(self.loc_1_2))
        self.assertFalse(self.loc_1_1.compare(self.loc_2_1))
        self.assertFalse(self.loc_1_1.compare(self.loc_2_2))

        self.assertTrue(self.loc_1_2.compare(self.loc_1_2))
        self.assertFalse(self.loc_1_2.compare(self.loc_2_1))
        self.assertFalse(self.loc_1_2.compare(self.loc_2_2))

        self.assertTrue(self.loc_2_1.compare(self.loc_2_1))
        self.assertFalse(self.loc_2_1.compare(self.loc_2_2))

        self.assertTrue(self.loc_2_2.compare(self.loc_2_2))

# Not sure how to write unit tests for the GoogleDocsBot class...

if __name__ == '__main__':
    unittest.main()
