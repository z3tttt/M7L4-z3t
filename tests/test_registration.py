import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users

@pytest.fixture(scope="module")
def setup_database():
    create_db()
    yield
    try:
        os.remove('users.db')
    except PermissionError:
        pass

@pytest.fixture
def connection():
    conn = sqlite3.connect('users.db')
    yield conn
    conn.close()

def test_create_db(setup_database, connection):
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists

def test_add_new_user(setup_database, connection):
    add_user('testuser', 'testuser@example.com', 'password123')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user

def test_add_user_with_existing_username(setup_database, connection):
    add_user('testuser', 'testuser@example.com', 'password123')
    result = add_user('testuser', 'another@example.com', 'newpassword')
    assert not result

def test_authenticate_user_success(setup_database, connection):
    add_user('testuser', 'testuser@example.com', 'password123')
    result = authenticate_user('testuser', 'password123')
    assert result

def test_authenticate_user_fail_wrong_password(setup_database, connection):
    add_user('testuser', 'testuser@example.com', 'password123')
    result = authenticate_user('testuser', 'wrongpassword')
    assert not result

def test_authenticate_user_fail_non_existent_user(setup_database, connection):
    result = authenticate_user('nonexistentuser', 'password123')
    assert not result

def test_display_users_empty(setup_database, connection):
    users = display_users()
    assert len(users) == 0

def test_display_users_with_data(setup_database, connection):
    add_user('user1', 'user1@example.com', 'password1')
    add_user('user2', 'user2@example.com', 'password2')
    users = display_users()
    assert len(users) == 2
    assert 'user1' in [user[0] for user in users]
    assert 'user2' in [user[0] for user in users]

def test_add_user_with_empty_password(setup_database, connection):
    result = add_user('userempty', 'userempty@example.com', '')
    assert not result

def test_add_user_with_invalid_email(setup_database, connection):
    result = add_user('userinvalid', 'invalidemail', 'password123')
    assert not result

def test_add_user_with_special_characters(setup_database, connection):
    result = add_user('user@123', 'user@123@example.com', 'password123')
    assert result

def test_user_creation_without_email(setup_database, connection):
    result = add_user('userwithoutemail', '', 'password123')
    assert not result

def test_create_db_twice(setup_database, connection):
    create_db()
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists






