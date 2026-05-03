import sys
import os

# PYTHONPATH problemini hell etmek ucun:
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Verilenler bazasi faylini (hbnb.db) yaradir
    print("Database hazirdir. Server http://127.0.0.1:5000 unvaninda isleyir.")
    app.run(debug=True)
