import pytest
import json
import sys
from pathlib import Path

# Add the src directory to the path so we can import main
src_path = str(Path(__file__).parent.parent / 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test the /health endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'

def test_process_data(client):
    """Test the /data endpoint"""
    test_payload = {"name": "test", "value": 123}
    response = client.post(
        '/data',
        data=json.dumps(test_payload),
        content_type='application/json'
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['result'] == 'Data processed successfully'
    assert data['input'] == test_payload