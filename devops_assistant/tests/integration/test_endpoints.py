import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_generate_terraform_endpoint():
    resp = client.post(
        "/generate/terraform", json={"provider":"aws","resources":[{"type":"ec2","size":"t3.micro"}]}
    )
    assert resp.status_code == 200
    assert "provider \"aws\"" in resp.json()['code']


def test_generate_cicd_endpoint():
    resp = client.post(
        "/generate/cicd", json={"platform":"github","steps":[{"name":"Build","run":"make"}]}
    )
    assert resp.status_code == 200
    assert "jobs:" in resp.json()['code']