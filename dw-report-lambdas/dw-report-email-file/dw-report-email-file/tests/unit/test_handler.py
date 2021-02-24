import json

import pytest

from src.app import app


@pytest.fixture()
def s3_event():

    return {
        "Records": [
            {
                "s3": {
                    "bucket": {
                        "name": "k12-dev-dw-report-email"
                    },
                    "object": {
                        "key": "data/TEST_01/send.txt"
                    }
                }
            }
        ]
    }


def test_lambda_handler(s3_event):

    ret = app.lambda_handler(s3_event, "")
    assert ret["statusCode"] == 200