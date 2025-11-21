import pytest
from app import create_app
from app.models import db, User, Department
from werkzeug.security import generate_password_hash
from flask_login import login_user
from flask import template_rendered
from contextlib import contextmanager

@pytest.fixture(scope='module')
def test_app():
    """Create and configure a new app instance for each test module."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing

    # Create all tables
    with app.app_context():
        db.create_all()
        
        # Create a test department
        department = Department(department_name='Test Department')
        db.session.add(department)
        db.session.commit()
        
        # Create a test user
        user = User(username='testuser', real_name='Test User', department_id=department.department_id, role='admin')
        user.password = generate_password_hash('testpass')
        db.session.add(user)
        db.session.commit()

        yield app

        # Teardown
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='module')
def client(test_app):
    """Create a test client for the app."""
    return test_app.test_client()

@contextmanager
def captured_templates(app):
    """Context manager to capture rendered templates."""
    recorded = []
    def record_template_rendered(sender, template, context, **extra):
        recorded.append(template)
    template_rendered.connect(record_template_rendered, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record_template_rendered, app)

@pytest.fixture(scope='function')
def logged_in_client(client, test_app):
    """Create a test client with a logged-in user."""
    with test_app.app_context():
        # Get the test user
        user = User.query.first()
        # Log in the user by setting session variables
        with client.session_transaction() as sess:
            sess['_user_id'] = str(user.user_id)
            sess['_fresh'] = True
    
    yield client

# Test inventory templates
def test_inventory_list_template(logged_in_client, test_app):
    with captured_templates(test_app) as templates:
        response = logged_in_client.get('/inventory/')
        assert response.status_code == 200
        assert any('inventory/item_list.html' in template.name for template in templates)

def test_inventory_stock_template(logged_in_client, test_app):
    with captured_templates(test_app) as templates:
        response = logged_in_client.get('/inventory/stock/query')
        assert response.status_code == 200
        assert any('inventory/stock_query.html' in template.name for template in templates)

# Test after_sales templates
def test_complaint_list_template(logged_in_client, test_app):
    with captured_templates(test_app) as templates:
        response = logged_in_client.get('/after_sales/complaints/')
        assert response.status_code == 200
        assert any('after_sales/complaint_list.html' in template.name for template in templates)

def test_complaint_add_template(logged_in_client, test_app):
    with captured_templates(test_app) as templates:
        response = logged_in_client.get('/after_sales/complaints/add/')
        assert response.status_code == 200
        assert any('after_sales/add_complaint.html' in template.name for template in templates)

def test_feedback_list_template(logged_in_client, test_app):
    with captured_templates(test_app) as templates:
        response = logged_in_client.get('/after_sales/feedbacks/')
        assert response.status_code == 200
        assert any('after_sales/feedback_list.html' in template.name for template in templates)

def test_feedback_add_template(logged_in_client, test_app):
    with captured_templates(test_app) as templates:
        response = logged_in_client.get('/after_sales/feedbacks/add/')
        assert response.status_code == 200
        assert any('after_sales/add_feedback.html' in template.name for template in templates)

# Test seed_batch templates
def test_batch_list_template(logged_in_client, test_app):
    with captured_templates(test_app) as templates:
        response = logged_in_client.get('/seed_batch/')
        assert response.status_code == 200
        assert any('seed_batch/batch_list.html' in template.name for template in templates)

def test_batch_create_template(logged_in_client, test_app):
    with captured_templates(test_app) as templates:
        response = logged_in_client.get('/seed_batch/add')
        assert response.status_code == 200
        assert any('seed_batch/add_batch.html' in template.name for template in templates)