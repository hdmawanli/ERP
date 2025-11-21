#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import create_app, db
from sqlalchemy import text

app = create_app()
with app.app_context():
    import app.models
    db.session.execute(text('DROP TABLE IF EXISTS opening_balance_inventory CASCADE'))
    db.session.commit()
    db.create_all()
    print('All database tables created successfully!')
