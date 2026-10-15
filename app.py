import os
from flask import Flask, jsonify, redirect, render_template, request, url_for
from dotenv import load_dotenv

load_dotenv()

import database
from integrations import github_snapshot, jira_snapshot
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "dev-only-change-me")
database.init_db()

@app.get("/")
def dashboard():
    projects = database.list_projects()
    for project in projects:
        project["github"] = github_snapshot(project["repository_url"])
        project["jira"] = jira_snapshot(project["jira_project_key"])
    return render_template("dashboard.html", projects=projects, error=None)

@app.post("/projects")
def add_project():
    try:
        database.create_project(request.form.get("name"), request.form.get("repository_url"), request.form.get("jira_project_key", ""))
    except ValueError as exc:
        projects = database.list_projects()
        for project in projects:
            project["github"] = github_snapshot(project["repository_url"])
            project["jira"] = jira_snapshot(project["jira_project_key"])
        return render_template("dashboard.html", projects=projects, error=str(exc)), 400
    return redirect(url_for("dashboard"))

@app.post("/projects/<int:project_id>/delete")
def remove_project(project_id):
    database.delete_project(project_id)
    return redirect(url_for("dashboard"))

@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "service": "development-orchestrator"})

@app.get("/api/projects")
def api_projects():
    return jsonify(database.list_projects())

@app.post("/api/projects")
def api_create_project():
    payload = request.get_json(silent=True) or {}
    try:
        project = database.create_project(payload.get("name"), payload.get("repository_url"), payload.get("jira_project_key", ""))
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    return jsonify(project), 201

@app.delete("/api/projects/<int:project_id>")
def api_delete_project(project_id):
    if not database.delete_project(project_id):
        return jsonify({"error": "Project not found"}), 404
    return "", 204

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
