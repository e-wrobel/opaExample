import json
from unittest import TestCase, mock
from opa_example import USER, URL, ROLE, METHOD, check_opa_allowed

OPA_REQUIRED_ROLES = ["manager"]
OPA_REQUIRED_URLS = ["allowed_url"]


def mocked_requests_post(*args, **kwargs):
    """
    This is mock for requests.post function. It will return HTTP_CODE 200 for selected data.
    We return 200 HTTP response only for roles in OPA_REQUIRED_ROLES and urls in OPA_REQUIRED_URL.
    """
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data
    body = json.loads(kwargs['data'])

    if body[URL] in OPA_REQUIRED_URLS and (body[ROLE] in OPA_REQUIRED_ROLES):
        return MockResponse("allowed", 200)

    return MockResponse("not allowed", 404)


class Test(TestCase):
    def setUp(self) -> None:
        pass

    # In this scenario, we assume that OPA response is true only for allowed_url url and manager role.
    # Any other requests will be finished with an error code.
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_check_opa_allowed(self, _):
        """
        This is mock test for OPA, containing 3 scenarios. As a second parameter we have added expected result.
        """
        tests = [
            ({
                USER: "admin1",
                METHOD: "GET",
                URL: "allowed_url",
                ROLE: "manager"
            }, "positive_url_and_role_is_allowed", True),
            ({
                 USER: "admin2",
                 METHOD: "GET",
                 URL: "not_allowed_url",
                 ROLE: "deputy"
             }, "negative_url_and_role_not_allowed", False),
            ({
                 USER: "admin2",
                 METHOD: "GET",
                 URL: "allowed_url",
                 ROLE: "deputy"
             }, "negative_url_allowed_role_not_allowed", False),
        ]

        for test in tests:
            body = test[0]
            test_name = test[1]
            expected_result = test[2]
            result = check_opa_allowed(body)
            self.assertTrue(expected_result == result, "Expected: {}, got: {}, test name: {}".
                            format(expected_result, result, test_name))
