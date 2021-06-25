from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import psycopg2
import utils
import bookings
import timeslots
import auth
import os

app = Flask(__name__)
CORS(app)

@app.route('/api/bookings', methods=['GET', 'POST'])
def getBookings():
  conn = psycopg2.connect(utils.cfgstring)
  if(request.method == 'GET'):
    [limit, offset] = [request.args.get('limit'), request.args.get('offset')]
    return bookings.api.getBookings(conn, limit, offset)
  if(request.method == 'POST'):
    payload = request.json
    return bookings.api.createBooking(conn, payload['name'], payload['phone'], payload['timeslotid'])

@app.route('/api/bookings/<string:id>', methods=['GET'])
def getBooking(id):
  if(request.method == 'GET'):
    conn = psycopg2.connect(utils.cfgstring)
    return bookings.api.getBooking(conn, id)

@app.route('/api/timeslots', methods=['GET', 'POST', 'DELETE'])
def createTimeslot():
  conn = psycopg2.connect(utils.cfgstring)
  if(request.method == 'GET'):
    status = request.args.get('status')
    if(status == 'active'):
      return timeslots.api.getActiveTimeslots(conn)
    if(status == 'all'):
      [limit, offset] = [request.args.get('limit'), request.args.get('offset')]
      if(limit is None or offset is None):
        abort(400, '{ "error": "limit and offset required"}')
      return timeslots.api.getAllTimeslots(conn, limit, offset)
    abort(400, '{ "error": "status query parameter required. Should be one of ["all", "active"]"}')
  if(request.method == 'POST'):
    token = request.headers.get('authToken')
    try:
      auth.service.jwt_decode(token)
    except:
      abort(403)
    payload = request.get_json()
    return timeslots.api.createTimeslot(conn, payload['slots'])

@app.route('/api/timeslots/<string:id>', methods=['DELETE'])
def deleteTimeslot(id):
  conn = psycopg2.connect(utils.cfgstring)
  if(request.method == 'DELETE'):
    return timeslots.api.deleteTimeslot(conn, id)

@app.route('/api/auth', methods=['GET', 'POST'])
def authenticate():
  conn = psycopg2.connect(utils.cfgstring)
  if(request.method == 'POST'):
    payload = request.get_json()
    return auth.api.authorize(conn, payload['login'], payload['password'])
  if(request.method == 'GET'):
    return auth.api.jwtauthorize(conn, request.args.get('token'))

@app.route('/api/edit', methods=['PUT'])
def changePassword():
  conn = psycopg2.connect(utils.cfgstring)
  if(request.method == 'PUT'):
    fields = request.get_json()
    token = request.headers.get('authToken')
    try:
      auth.service.jwt_decode(token)
    except:
      abort(403)
    payload = request.get_json()
    return auth.api.changeData(conn, token, fields)

@app.route('/api/bookings/update/<string:id>', methods=['PUT'])
def updateBooking(id):
  conn = psycopg2.connect(utils.cfgstring)
  if(request.method == 'PUT'):
    token = request.headers.get('authToken')
    try:
      auth.service.jwt_decode(token)
    except:
      abort(403)
    payload = request.get_json()
    return bookings.api.changeStatus(conn, id, payload['status'])

@app.route('/api/hello')
def tmp():
  conn = psycopg2.connect(utils.cfgstring)
  cur = conn.cursor()
  cur.execute('''CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
  
  CREATE TABLE IF NOT EXISTS users
(
    id uuid PRIMARY KEY NOT NULL DEFAULT uuid_generate_v4(),
    login text NOT NULL,
    password text NOT NULL
);

CREATE TABLE IF NOT EXISTS timeslots
(
    id uuid PRIMARY KEY NOT NULL DEFAULT uuid_generate_v4(),
    timestart timestamp without time zone NOT NULL,
    timeend timestamp without time zone NOT NULL,
    status boolean NOT NULL
);

CREATE TABLE IF NOT EXISTS bookings
(
    id uuid PRIMARY KEY NOT NULL DEFAULT uuid_generate_v4(),
    name text NOT NULL,
    phone text NOT NULL,
    timeslotid uuid NOT NULL,
    status text NOT NULL,
    CONSTRAINT fk_timeslot FOREIGN KEY (timeslotid)
        REFERENCES timeslots (id)
);

INSERT INTO users (login, password)
SELECT \'admin\', \'admin\'
WHERE NOT EXISTS (SELECT * FROM users);

SELECT * FROM USERS''')
  row = cur.fetchone()
  conn.commit()
  cur.close()
  conn.close()
  return jsonify(row)


if __name__ == '__main__':
  app.run(debug=False)