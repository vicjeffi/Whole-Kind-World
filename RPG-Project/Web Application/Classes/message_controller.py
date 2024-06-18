from flask import render_template, session, redirect, url_for, request
from Classes.auth_controller import login_check
from Models.message import Message
from flask.json import jsonify
from db_extension import db

def get_messages():
    if login_check():
        LoginedUser = session['LoginedUser']
        messages = Message.query.filter(Message.ReceiverID == LoginedUser['ID']).order_by(Message.timestamp.asc()).all()
        if messages:
            return jsonify([{'text': msg.text, 'timestamp': msg.timestamp} for msg in messages])
        else:
            return None
        
def send_message():
    if login_check():
        LoginedUser = session['LoginedUser']
        data = request.get_json()
        new_message = Message(
            text=data['text'],
            ReceiverID=LoginedUser['ID']
        )
        db.session.add(new_message)
        db.session.commit()
        return jsonify({'message': 'Message sent successfully'})
    else:
        return jsonify({'error': 'User not logged in'}), 401