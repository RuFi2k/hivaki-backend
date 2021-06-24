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

@app.route('/bookings', methods=['GET', 'POST'])
def getBookings():
  conn = psycopg2.connect(utils.cfgstring)
  if(request.method == 'GET'):
    cur = conn.cursor()
    [limit, offset] = [request.args.get('limit'), request.args.get('offset')]
    return bookings.api.getBookings(cur, limit, offset)
  if(request.method == 'POST'):
    payload = request.json
    return bookings.api.createBooking(conn, payload['name'], payload['phone'], payload['timeslotid'])

@app.route('/bookings/<string:id>', methods=['GET'])
def getBooking(id):
  if(request.method == 'GET'):
    conn = psycopg2.connect(utils.cfgstring)
    cur = conn.cursor()
    return bookings.api.getBooking(cur, id)

@app.route('/timeslots', methods=['GET', 'POST', 'DELETE'])
def createTimeslot():
  conn = psycopg2.connect(utils.cfgstring)
  if(request.method == 'GET'):
    status = request.args.get('status')
    cur = conn.cursor()
    if(status == 'active'):
      return timeslots.api.getActiveTimeslots(cur)
    if(status == 'all'):
      [limit, offset] = [request.args.get('limit'), request.args.get('offset')]
      if(limit is None or offset is None):
        abort(400, '{ "error": "limit and offset required"}')
      return timeslots.api.getAllTimeslots(cur, limit, offset)
    abort(400, '{ "error": "status query parameter required. Should be one of ["all", "active"]"}')
  if(request.method == 'POST'):
    token = request.headers.get('authToken')
    try:
      auth.service.jwt_decode(token)
    except:
      abort(403)
    payload = request.get_json()
    return timeslots.api.createTimeslot(conn, payload['slots'])

@app.route('/timeslots/<string:id>', methods=['DELETE'])
def deleteTimeslot(id):
  conn = psycopg2.connect(utils.cfgstring)
  if(request.method == 'DELETE'):
    return timeslots.api.deleteTimeslot(conn, id)

@app.route('/auth', methods=['GET', 'POST'])
def authenticate():
  conn = psycopg2.connect(utils.cfgstring)
  if(request.method == 'POST'):
    payload = request.get_json()
    return auth.api.authorize(conn, payload['login'], payload['password'])
  if(request.method == 'GET'):
    return auth.api.jwtauthorize(conn, request.args.get('token'))

@app.route('/edit', methods=['PUT'])
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

@app.route('/bookings/update/<string:id>', methods=['PUT'])
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



if __name__ == '__main__':
  app.run(debug=False)