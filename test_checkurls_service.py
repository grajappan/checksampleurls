import webtest
import unittest
from webtest import TestApp
import checkurls_service

class TestCheckrls_service(unittest.TestCase):
    def test_my_app_metrics(self):
        app = TestApp(checkurls_service.my_app)
        res = app.get(url='/metrics',expect_errors=True,status='*')
        self.assertEqual(res.status_int, 200)

    def test_my_app(self):
        app = TestApp(checkurls_service.my_app)
        res = app.get(url='/',expect_errors=True,status='*')
        self.assertEqual(res.body, b'Sample urls are accessible')
if __name__ == '__main__':
    unittest.main()
