def test_root_redirect(client):
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities(client):
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "michael@mergington.edu" in data["Chess Club"]["participants"]


def test_signup_success(client):
    email = "newstudent@mergington.edu"
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"

    # Verify participant was added
    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]
    assert email in participants


def test_signup_duplicate_email(client):
    email = "michael@mergington.edu"
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_activity_not_found(client):
    response = client.post("/activities/Unknown Activity/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_success(client):
    email = "michael@mergington.edu"
    response = client.delete(f"/activities/Chess Club/unregister?email={email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from Chess Club"

    # Verify participant was removed
    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]
    assert email not in participants


def test_unregister_not_registered(client):
    email = "notregistered@mergington.edu"
    response = client.delete(f"/activities/Chess Club/unregister?email={email}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not registered for this activity"


def test_unregister_activity_not_found(client):
    response = client.delete("/activities/Unknown Activity/unregister?email=michael@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
