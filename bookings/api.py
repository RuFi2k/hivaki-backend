from flask import jsonify, abort, make_response
from .strings import strings
from .model import models

class api:
  def getBookings(conn, limit, offset):
    cur = conn.cursor()
    result = []
    cur.execute(strings.getBookingsString(limit, offset))
    row = cur.fetchone()
    while row is not None:
      result.append(models.getModel(row))
      row = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify({ 'data': result })

  def getBooking(conn, id):
    cur = conn.cursor()
    try:
      cur.execute(strings.getBooking(id))
      result = []
      row = cur.fetchone()
      while row is not None:
        result.append(models.getModel(row))
        row = cur.fetchone()
      if( not len(result) ):
        abort(make_response(jsonify(message='Запись не найдена'), 404))
      return jsonify({ 'data': result })
    except Exception as e:
      return abort(make_response(jsonify(message=str(e)), 400))
    finally:
      cur.close()
      conn.close()


  def createBooking(conn, name, phone, timeslotid):
    cur = conn.cursor()
    try:
      cur.execute(strings.createBooking(name, phone, timeslotid))
      row = cur.fetchone()
      if(row == None):
        raise Exception('Не удалось создать запись. Повторите попытку позже')
      id = row[0]
      cur.execute(strings.updateTimeslotStatus(timeslotid, True))
      conn.commit()
      return jsonify({ 'data': {
        'id': id,
        'name': name,
        'phone': phone,
        'timeslotid': timeslotid
      } })
    except Exception as e:
      return abort(make_response(jsonify(message=str(e)), 400))
    finally:
      cur.close()
      conn.close()

  def changeStatus(conn, id, status):
    cur = conn.cursor()
    try:
      cur.execute(strings.setBookingStatus(id, status))
      row = cur.fetchone()
      if(row == None):
        raise Exception('Не удалось найти указанную запись')
      conn.commit()
      return jsonify({ 'success': True, 'data': models.getModel(row) })
    except Exception as e:
      return abort(make_response(jsonify(message=str(e)), 400))
    finally:
      cur.close()
      conn.close()