import json
import logging
import os

import requests

USER = "user"
METHOD = "method"
URL = "url"
ROLE = "role"

DEFAULT_OPA_URL = "http://localhost:8181"


def check_opa_allowed(body: dict) -> bool:
    """
    This function checks if data body in body are granted by OPA service.

    :param body: Body we want to validate in OPA
    :type body: dict
    :rtype: bool
    """
    response = None

    try:
        inp = json.dumps(body, indent=2)
        url = os.environ.get("OPA_URL", DEFAULT_OPA_URL)
        logging.debug("OPA query: %s. Body: %s", url, inp)
        response = requests.post(url, data=inp)
    except requests.exceptions.HTTPError as e:
        logging.exception("Got HTTP error querying OPA: {}".format(e))
        return False
    except requests.exceptions.ReadTimeout as e:
        logging.exception("Got HTTP timeout querying OPA: {}".format(e))
    except Exception as e:
        logging.exception("Unexpected error querying OPA: {}".format(e))
        return False

    if response.status_code != 200:
        return False

    allowed = response.json()
    logging.debug("OPA result: %s", allowed)
    if not allowed:
        return False

    return True


if __name__ == '__main__':
    pass
