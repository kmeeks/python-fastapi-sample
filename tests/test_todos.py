def test_create_todo(client):
    response = client.post(
        "/todos/",
        json={"title": "Buy milk", "description": "2%", "status": "pending"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] is not None
    assert data["title"] == "Buy milk"
    assert data["description"] == "2%"
    assert data["status"] == "pending"


def test_create_todo_default_status(client):
    response = client.post(
        "/todos/",
        json={"title": "No status provided"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "No status provided"
    assert data["status"] == "pending"
    assert data["description"] is None


def test_list_todos(client, sample_todo):
    response = client.get("/todos/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(todo["id"] == sample_todo["id"] for todo in data)


def test_list_todos_skip_limit(client):
    created_ids = []
    for i in range(3):
        response = client.post(
            "/todos/",
            json={"title": f"Todo {i}", "description": f"desc {i}"},
        )
        assert response.status_code == 200
        created_ids.append(response.json()["id"])

    response = client.get("/todos/", params={"skip": 1, "limit": 1})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == created_ids[1]


def test_list_todos_by_status_defaults(client):
    done_ids = []
    pending_id = None

    for i in range(3):
        response = client.post(
            "/todos/",
            json={"title": f"Done {i}", "status": "done"},
        )
        assert response.status_code == 200
        done_ids.append(response.json()["id"])

    response = client.post(
        "/todos/",
        json={"title": "Pending item", "status": "pending"},
    )
    assert response.status_code == 200
    pending_id = response.json()["id"]

    response = client.get("/todos/by-status/done")
    assert response.status_code == 200
    data = response.json()

    assert set(data.keys()) == {"items", "page", "size", "total"}
    assert data["page"] == 0
    assert data["size"] == 20
    assert data["total"] == 3
    assert [todo["id"] for todo in data["items"]] == done_ids
    assert all(todo["status"] == "done" for todo in data["items"])
    assert all(todo["id"] != pending_id for todo in data["items"])


def test_list_todos_by_status_page_size(client):
    for i in range(5):
        response = client.post(
            "/todos/",
            json={"title": f"In progress {i}", "status": "in_progress"},
        )
        assert response.status_code == 200

    response = client.get(
        "/todos/by-status/in_progress",
        params={"page": 1, "size": 2},
    )
    assert response.status_code == 200
    data = response.json()

    assert data["page"] == 1
    assert data["size"] == 2
    assert data["total"] == 5
    assert len(data["items"]) == 2
    assert [todo["title"] for todo in data["items"]] == ["In progress 2", "In progress 3"]
    assert all(todo["status"] == "in_progress" for todo in data["items"])


def test_list_todos_by_status_size_max_validation(client):
    response = client.get("/todos/by-status/pending", params={"size": 101})
    assert response.status_code == 422


def test_get_todo(client, sample_todo):
    response = client.get(f"/todos/{sample_todo['id']}")
    assert response.status_code == 200
    assert response.json() == sample_todo


def test_get_todo_not_found(client):
    response = client.get("/todos/99999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_update_todo_partial(client, sample_todo):
    response = client.put(
        f"/todos/{sample_todo['id']}",
        json={"status": "done"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_todo["id"]
    assert data["title"] == sample_todo["title"]
    assert data["description"] == sample_todo["description"]
    assert data["status"] == "done"


def test_update_todo_full(client, sample_todo):
    response = client.put(
        f"/todos/{sample_todo['id']}",
        json={
            "title": "Updated title",
            "description": "Updated description",
            "status": "in_progress",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": sample_todo["id"],
        "title": "Updated title",
        "description": "Updated description",
        "status": "in_progress",
    }


def test_update_todo_not_found(client):
    response = client.put("/todos/99999", json={"title": "Nope"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_delete_todo(client, sample_todo):
    response = client.delete(f"/todos/{sample_todo['id']}")
    assert response.status_code == 200
    assert response.json() == {"detail": "Todo deleted"}

    follow_up = client.get(f"/todos/{sample_todo['id']}")
    assert follow_up.status_code == 404


def test_delete_todo_not_found(client):
    response = client.delete("/todos/99999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}
