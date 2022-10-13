import pytest
from rest_framework.test import APIClient

from students.models import Course, Student
from model_bakery import baker


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_get_course(client):
    Course.objects.create(name='Python')

    response = client.get('/api/v1/courses/')

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['name'] == 'Python'


@pytest.mark.django_db
def test_get_1_course(client, course_factory):
    courses = course_factory(_quantity=1)

    response = client.get(f'/api/v1/courses/{courses[0].id}/')

    assert response.status_code == 200
    data = response.json()

    assert data['name'] == courses[0].name
    assert data['id'] == courses[0].id


@pytest.mark.django_db
def test_get_list_course(client, course_factory):
    courses = course_factory(_quantity=15)

    response = client.get('/api/v1/courses/')

    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)
    for i, m in enumerate(data):
        assert m['name'] == courses[i].name


@pytest.mark.django_db
def test_create_course(client):
    count = Course.objects.count()

    response = client.post('/api/v1/courses/', data={'name': 'Java'})

    assert response.status_code == 201
    assert Course.objects.count() == count + 1


@pytest.mark.django_db
def test_update_course(client, course_factory):
    course = course_factory(_quantity=1)

    response = client.patch(f'/api/v1/courses/{course[0].id}/', data={'name': 'Java'})

    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    course = course_factory(_quantity=1)

    response = client.delete(f'/api/v1/courses/{course[0].id}/')

    assert response.status_code == 204


@pytest.mark.django_db
def test_filter_id(client, course_factory):
    courses = course_factory(_quantity=10)

    response = client.get(f'/api/v1/courses/{courses[5].id}/')

    assert response.status_code == 200
    data = response.json()
    assert data['id'] == courses[5].id
    assert data['name'] == courses[5].name


@pytest.mark.django_db
def test_filter_name(client, course_factory):
    courses = course_factory(_quantity=10)

    response = client.get(f'/api/v1/courses/', {'name': courses[5].name})

    assert response.status_code == 200
    data = response.json()
    assert data[0]['id'] == courses[5].id
    assert data[0]['name'] == courses[5].name
