# App.py

# Instructions to install required packages:
# To install the required packages, use the following command:
#
# pip install Flask Flask-SQLAlchemy
#
# Alternatively, if you have a requirements.txt file, you can install all dependencies with:
#
# pip install -r requirements.txt

from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

import os

app = Flask(__name__)
# Create the instance directory if it doesn't exist
os.makedirs(app.instance_path, exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'contacts.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    url = db.Column(db.String(200), nullable=True)
    notes = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Contact {self.name}>'

# Move database creation after all models are defined
with app.app_context():
    db.create_all()
    if Contact.query.count() == 0:
        sample_contacts = [
            Contact(name='John Doe', phone='123-456-7890', email='john.doe@example.com', url='http://www.johndoe.com', notes='Sample note for John'),
            Contact(name='Jane Smith', phone='987-654-3210', email='jane.smith@example.com', url='http://www.janesmith.com', notes='Sample note for Jane'),
            Contact(name='Alice Johnson', phone='555-123-4567', email='alice.johnson@example.com', url='http://www.alicejohnson.com', notes='Sample note for Alice'),
            Contact(name='Bob Williams', phone='111-222-3333', email='bob.williams@example.com', url='http://www.bobwilliams.com', notes='Sample note for Bob'),
            Contact(name='Charlie Brown', phone='444-555-6666', email='charlie.brown@example.com', url='http://www.charliebrown.com', notes='Sample note for Charlie'),
            Contact(name='Diana Miller', phone='777-888-9999', email='diana.miller@example.com', url='http://www.dianamiller.com', notes='Sample note for Diana'),
            Contact(name='Ethan Davis', phone='333-444-5555', email='ethan.davis@example.com', url='http://www.ethandavis.com', notes='Sample note for Ethan'),
            Contact(name='Fiona Wilson', phone='666-777-8888', email='fiona.wilson@example.com', url='http://www.fionawilson.com', notes='Sample note for Fiona'),
            Contact(name='George Garcia', phone='888-999-0000', email='george.garcia@example.com', url='http://www.georgegarcia.com', notes='Sample note for George'),
            Contact(name='Hannah Rodriguez', phone='222-333-4444', email='hannah.rodriguez@example.com', url='http://www.hannahrodriguez.com', notes='Sample note for Hannah')
        ]
        db.session.add_all(sample_contacts)
        db.session.commit()

@app.route('/')
def index():
    contacts = Contact.query.all()
    return render_template('index.html', contacts=contacts)

@app.route('/add', methods=['POST'])
def add_contact():
    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    url = request.form.get('url')
    notes = request.form.get('notes')
    new_contact = Contact(name=name, phone=phone, email=email, url=url, notes=notes)
    db.session.add(new_contact)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_contact(id):
    contact = Contact.query.get(id)
    if request.method == 'POST':
        contact.name = request.form.get('name')
        contact.phone = request.form.get('phone')
        contact.email = request.form.get('email')
        contact.url = request.form.get('url')
        contact.notes = request.form.get('notes')
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', contact=contact)

@app.route('/delete/<int:id>')
def delete_contact(id):
    contact = Contact.query.get(id)
    db.session.delete(contact)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
