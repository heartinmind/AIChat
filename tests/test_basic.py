from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_send_message():
    resp = client.post('/message', json={'user_id': '123', 'text': 'hello'})
    assert resp.status_code == 200
    assert 'reply' in resp.json()
