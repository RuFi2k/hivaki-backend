from flask import jsonify
from datetime import datetime
from .strings import strings
from .model import models

class api:
  def getAllTimeslots(conn, limit, offset):
    cur = conn.cursor()
    result = []
    cur.execute(strings.getAllTimeslots(limit, offset))
    row = cur.fetchone()
    while row is not None:
      result.append(models.getActive(row))
      row = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify({ 'data': result })

  def getActiveTimeslots(conn):
    cur = conn.cursor()
    result = []
    cur.execute(strings.getActiveTimeslots())
    row = cur.fetchone()
    while row is not None:
      result.append(models.getActive(row))
      row = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify({ 'data': result })

  def createTimeslot(conn, slots):
    try:
      result = []
      cur = conn.cursor()
      cur.execute(strings.createTimeslot(slots))
      row = cur.fetchone()
      while row is not None:
        result.append(models.getModel(row))
        row = cur.fetchone()
      conn.commit()
      return jsonify({ 'data': result })
    except Exception as e:
      return jsonify({ 'error': str(e) })
    finally:
      cur.close()
      conn.close()

  def deleteTimeslot(conn, id):
    try:
      cur = conn.cursor()
      cur.execute(strings.deleteTimeslot(id))
      conn.commit()
      return jsonify({ 'success': True, 'data': { 'id': id } })
    except Exception as e:
      return jsonify({ 'success': False, 'error': str(e) })
    finally:
      cur.close()
      conn.close()