from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)

class UserClosestAirports(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    closest_airport_id = db.Column(db.Integer, nullable=False)

class Airports(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ident = db.Column(db.String, unique=True, nullable=False)
    wikipedia_link = db.Column(db.String, nullable=True)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/nearest_airports/<int:user_id>', methods=['GET'])
def get_nearest_airport(user_id):
    user_airport = UserClosestAirports.query.filter_by(user_id=user_id).first()
    if user_airport is None:
        return jsonify(error='User not found or has no closest airport'), 404

    airport = Airports.query.filter_by(id=user_airport.closest_airport_id).first()
    if airport is None:
        return jsonify(error='Airport not found'), 404

    return jsonify(airport_id=airport.id)

@app.route('/nearest_airports_wikipedia/<int:user_id>', methods=['GET'])
def get_nearest_airport_wikipedia(user_id):
    user_airport = UserClosestAirports.query.filter_by(user_id=user_id).first()
    if user_airport is None:
        return jsonify(error='User not found or has no closest airport'), 404

    airport = Airports.query.filter_by(id=user_airport.closest_airport_id).first()
    if airport is None:
        return jsonify(error='Airport not found'), 404

    return jsonify(wikipedia_link=airport.wikipedia_link)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
