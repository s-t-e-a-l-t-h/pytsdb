import unittest
from unittest import mock

from pyopentsdb import tsdb
from tests.testutils import get_mock_requests_get
from tests.testutils import GeneralUrlTestCase


class TsdbConfigTestCase(unittest.TestCase):
    __TEST_CONFIG__ = {
        "Ansible": "managed",
        "tsd.core.authentication.enable": "false",
        "tsd.core.authentication.plugin": "",
        "tsd.core.auto_create_metrics": "true",
        "tsd.core.auto_create_tagks": "true",
        "tsd.core.auto_create_tagvs": "true"
    }

    __TEST_FILTERS__ = {
        "regexp": {
            "examples": "host=regexp(.*)  {\"type\":\"regexp\",\"tagk\":\"host\",\"filter\":\".*\",\"groupBy\":false}",
            "description": "Provides full, POSIX compliant regular expression using the built in Java"
        },
        "iwildcard": {
            "examples": "host=iwildcard(web*),  host=iwildcard(web*.tsdb.net)  "
                        "{\"type\":\"iwildcard\",\"tagk\":\"host\",\"filter\":\"web*.tsdb.net\",\"groupBy\":false}",
            "description": "Performs pre, post and in-fix glob matching of values. The globs are case"
        }
    }

    __TETS_DROPCACHES__ = {
        "message": "Caches dropped",
        "status": "200"
    }

    def setUp(self):
        self._host = 'mockhttp://localhost:5896/'

        self._c = tsdb.tsdb_connection(self._host)

    @mock.patch('requests.Session.get', side_effect=get_mock_requests_get(None))
    def test_url_config(self, _):
        GeneralUrlTestCase.test_url(self, "/api/config/", "config")

    @mock.patch('requests.Session.get', side_effect=get_mock_requests_get(None))
    def test_url_filters(self, _):
        GeneralUrlTestCase.test_url(self, "/api/config/filters/", "filters")

    @mock.patch('requests.Session.get', side_effect=get_mock_requests_get(__TEST_CONFIG__))
    def test_config(self, _):
        response = self._c.config()
        self.assertEqual(sorted(response), sorted(TsdbConfigTestCase.__TEST_CONFIG__))

    @mock.patch('requests.Session.get', side_effect=get_mock_requests_get(__TEST_FILTERS__))
    def test_filters(self, _):
        response = self._c.filters()
        self.assertEqual(sorted(response), sorted(TsdbConfigTestCase.__TEST_FILTERS__))
