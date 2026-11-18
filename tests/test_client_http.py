import json
import random
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

import factories
from helpers import fresh_state
from l_toolkit import upstream as U
from l_toolkit.client import UpstreamClient
from l_toolkit.errors import ApiError


class Script:
    def __init__(self):
        self.account = []
        self.config = []
        self.seen = []


@pytest.fixture
def server():
    script = Script()

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            length = int(self.headers.get("Content-Length") or 0)
            body = self.rfile.read(length) if length else b""
            queue = script.account if self.path == U.ACCOUNT_PATH else script.config
            script.seen.append({"path": self.path, "headers": dict(self.headers), "body": body})
            status, payload, headers = queue.pop(0) if queue else (500, b"{}", {})
            self.send_response(status)
            for key, value in headers.items():
                self.send_header(key, value)
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def log_message(self, *args):
            pass

    httpd = HTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=lambda: httpd.serve_forever(poll_interval=0.02), daemon=True)
    thread.start()
    script.url = "http://127.0.0.1:%d" % httpd.server_address[1]
    yield script
    httpd.shutdown()


@pytest.fixture
def client(server):
    sleeps = []
    instance = UpstreamClient(
        account_url=server.url,
        config_url=server.url,
        sleep=sleeps.append,
        rng=random.Random(3),
    )
    instance.sleeps = sleeps
    return instance


def ok(payload):
    return 200, json.dumps(payload).encode("utf-8"), {"Content-Type": "application/json"}


def state():
    return fresh_state().with_user(77, "http-token-value")


def test_an_account_is_created_over_real_http_with_the_documented_headers(server, client):
    server.account.append(ok({"userId": 5, "token": "t0k3n-value"}))
    device = fresh_state().device_id
    assert client.create_account(device) == (5, "t0k3n-value")
    request = server.seen[0]
    assert request["path"] == U.ACCOUNT_PATH and request["body"] == b""
    assert request["headers"][U.HEADER_DEVICE_ID] == device
    assert request["headers"][U.HEADER_APP_NAME] == U.APP_NAME
    assert U.HEADER_USER_ID not in request["headers"]


def test_a_configuration_is_fetched_over_real_http_with_the_documented_body(server, client):
    server.config.append(ok(factories.response()))
    account = state()
    assert client.fetch_config(account)["country"] == "IR"
    request = server.seen[0]
    assert request["path"] == U.CONFIG_PATH
    assert request["headers"][U.HEADER_USER_ID] == "77"
    assert request["headers"]["Content-Type"] == "application/json"
    body = json.loads(request["body"])
    assert body["device_id"] == account.device_id and body["pro_token"] == "http-token-value"
    assert body["protocols"] == list(U.ADVERTISED_PROTOCOLS)


def test_the_token_is_only_sent_in_the_body_never_in_a_header(server, client):
    server.config.append(ok(factories.response()))
    client.fetch_config(state())
    for key, value in server.seen[0]["headers"].items():
        assert "http-token-value" not in value, key


def test_a_503_is_retried_and_then_succeeds(server, client):
    server.config.append((503, b"{}", {}))
    server.config.append(ok(factories.response()))
    assert client.fetch_config(state())["country"] == "IR"
    assert [r["path"] for r in server.seen] == [U.CONFIG_PATH, U.CONFIG_PATH]
    assert len(client.sleeps) == 1


def test_a_429_with_retry_after_waits_for_that_long(server, client):
    server.config.append((429, b"{}", {"Retry-After": "11"}))
    server.config.append(ok(factories.response()))
    client.fetch_config(state())
    assert 11 <= client.sleeps[0] <= 12


def test_a_huge_retry_after_stops_after_one_request(server, client):
    server.config.append((429, b"{}", {"Retry-After": "900"}))
    with pytest.raises(ApiError):
        client.fetch_config(state())
    assert len(server.seen) == 1 and client.sleeps == []


@pytest.mark.parametrize("status", [429, 500, 502, 503, 504])
def test_account_creation_is_never_repeated_by_the_http_layer(server, client, status):
    server.account.append((status, b"{}", {}))
    server.account.append(ok({"userId": 1, "token": "second-account"}))
    with pytest.raises(ApiError):
        client.create_account(fresh_state().device_id)
    assert len(server.seen) == 1 and client.sleeps == []


def test_three_failures_in_a_row_give_up_after_exactly_three_requests(server, client):
    for _ in range(5):
        server.config.append((500, b"{}", {}))
    with pytest.raises(ApiError):
        client.fetch_config(state())
    assert len(server.seen) == 3 and len(client.sleeps) == 2


def test_an_unreachable_host_fails_cleanly_without_leaking_details():
    unreachable = UpstreamClient(account_url="http://127.0.0.1:9", config_url="http://127.0.0.1:9", sleep=lambda s: None)
    with pytest.raises(ApiError) as info:
        unreachable.fetch_config(state())
    assert "127.0.0.1" not in str(info.value)
