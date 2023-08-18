from tests.utils import send_websocket_message

def test_point_deleted(client):

    # send websocket message
    res = send_websocket_message({
        "text": "Hello Mad Hatter"
    }, client)

    # get point back
    params = {
        "text": "Mad Hatter"
    }
    response = client.get(f"/memory/recall/", params=params)
    json = response.json()
    assert response.status_code == 200
    assert len(json["vectors"]["collections"]["episodic"]) == 1
    memory = json["vectors"]["collections"]["episodic"][0]
    assert memory["page_content"] == "Hello Mad Hatter"

    # delete point (wrong collection)
    res = client.delete(f"/memory/collections/wrongcollection/points/{memory['id']}/")
    assert res.status_code == 400
    assert res.json()["detail"]["error"] == "Collection does not exist."

    # delete point (wrong id)
    res = client.delete(f"/memory/collections/episodic/points/wrong_id/")
    assert res.status_code == 400
    assert res.json()["detail"]["error"] == "Point does not exist."

    # delete point (all right)
    res = client.delete(f"/memory/collections/episodic/points/{memory['id']}/")
    assert res.status_code == 200
    assert res.json()["deleted"] == memory['id']

    # there is no point now
    params = {
        "text": "Mad Hatter"
    }
    response = client.get(f"/memory/recall/", params=params)
    json = response.json()
    assert response.status_code == 200
    assert len(json["vectors"]["collections"]["episodic"]) == 0

    # delete again the same point (Qdrant in :memory: bug!)
    #res = client.delete(f"/memory/episodic/point/{memory['id']}/")
    #assert res.status_code == 422
    #assert res.json()["detail"]["error"] == "Point does not exist."
