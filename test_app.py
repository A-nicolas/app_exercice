import pytest
from flask import json
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_submit_feedback(client):
    data = {
        'bootcampname': 'Test Bootcamp',
        'prioriteRetour': 'Haute',
        'typeRetour': 'Contenu du cours',
        'date_feedback': '2024-03-20 15:30:00',
        'rating': 5,
        'comments': 'Test comment',
        'attachedfiles': 'test_file.txt',
        'consentement': True
    }

    response = client.post('/api/feedback', json=data)
    assert response.status_code == 200
    assert response.json == {'message': 'Données envoyées avec succès'}

def test_get_feedbacks(client):
    response = client.get('/api/feedback')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_feedback_by_id(client):
    response = client.get('/api/feedback/ff80cb97-fe16-4de9-b3df-95d56f0f132b')
    assert response.status_code == 200
    assert isinstance(response.json, dict)

def test_update_feedback(client):
    feedback_id = 'ff80cb97-fe16-4de9-b3df-95d56f0f132b'
    data = {
        'bootcampname': 'Updated Bootcamp',
        'prioriteRetour': 'Moyenne',
        'typeRetour': 'Formateur',
        'date_feedback': '2024-03-21 10:30:00',
        'rating': 4,
        'comments': 'Updated comment',
        'attachedfiles': 'updated_file.txt'
    }

    response = client.put(f'/api/feedback/{feedback_id}', json=data)
    assert response.status_code == 200
    assert response.json == {'message': 'Feedback mis à jour avec succès'}

def test_delete_feedback(client):
    feedback_id = 'ff80cb97-fe16-4de9-b3df-95d56f0f132b'
    response = client.delete(f'/api/feedback/{feedback_id}')
    assert response.status_code == 200
    assert response.json == {'message': 'Feedback supprimé avec succès'}
