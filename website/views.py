from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__) # this passes the string 'views' and the file name '__name__' which will be equal to website.views, 
# it is recommended that you set blueprint to the file name

print('views' , __name__ , "This is what is being passed when we enter the string view and __name__") # This is to see what is happening when name is called

# To define a view or a route type "@", then your blueprint variable "views" name, and then ".route()", then in the parentheses pass what you would 
@views.route('/', methods=['GET', 'POST']) # like the end of the url to be for this route.
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
