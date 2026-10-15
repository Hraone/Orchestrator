import pytest
import database
import app as app_module

@pytest.fixture()
def client(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setattr(database, "DATABASE_PATH", str(db_path))
    database.init_db()
    app_module.app.config.update(TESTING=True, SECRET_KEY="test-secret")
    with app_module.app.test_client() as client:
        yield client

def test_health_endpoint(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"

def test_create_and_list_project(client):
    response = client.post("/api/projects", json={"name": "Demo", "repository_url": "https://github.com/acme/demo", "jira_project_key": "DEMO"})
    assert response.status_code == 201
    project_id = response.get_json()["id"]
    listed = client.get("/api/projects").get_json()
    assert any(project["id"] == project_id and project["name"] == "Demo" for project in listed)

def test_project_requires_name_and_repository(client):
    response = client.post("/api/projects", json={"name": "", "repository_url": ""})
    assert response.status_code == 400

def test_delete_project(client):
    project = database.create_project("Demo", "https://github.com/acme/demo")
    response = client.delete(f"/api/projects/{project['id']}")
    assert response.status_code == 204
    assert client.delete(f"/api/projects/{project['id']}").status_code == 404
