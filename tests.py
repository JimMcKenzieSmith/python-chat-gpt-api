from main import app
import json
import pytest

@pytest.fixture()
def client():
    app.config.update({
        "TESTING": True,
    })
    with app.test_client() as client:
        yield client


def test_get_sales(client, mocker):
    mocker.patch(
        'main.get_response_from_chat_gpt',
        return_value={
            "choices": [
            {
                "message": {
                "content": "The status of order 10248 is Cancelled."
                }
            }]
        }
    )
    response = client.post("/api/sales", 
        data=json.dumps(dict(customer_id='778', user_request='What is the status of order 10248?')),
        content_type='application/json')
    assert response.status_code == 200
    assert b"Cancelled" in response.data

def test_get_sales_missing_data(client, mocker):
    response = client.post("/api/sales", 
        data=json.dumps(dict(user_request='What is the status of order 10248?')),
        content_type='application/json')
    assert response.status_code == 400

def test_get_quiz_results(client, mocker):
    mocker.patch(
        'main.get_response_from_chat_gpt',
        return_value={
            "choices": [
            {
                "message": {
                "content": "The question that the highest number of students answered wrong is \"Which two major superpowers were the primary participants in the Cold War?\"."
                }
            }]
        }
    )
    response = client.post("/api/quiz-results", 
        data=json.dumps(dict(file_loc='data/cold_war_classroom_quiz_sample.csv', user_request='Which question did the highest number of students answer wrong?')),
        content_type='application/json')
    assert response.status_code == 200
    assert b"superpowers" in response.data

def test_get_quiz_results_missing_data(client, mocker):
    response = client.post("/api/quiz-results", 
        data=json.dumps(dict(user_request='Which question did the highest number of students answer wrong?')),
        content_type='application/json')
    assert response.status_code == 400