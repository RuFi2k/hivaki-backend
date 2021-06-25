import jwt
from .strings import strings
from .service import service
from flask import jsonify, abort, make_response

class api:
  def authorize(conn, login, password):
    cur = conn.cursor()
    try:
      cur.execute(strings.authorize(login, password))
      row = cur.fetchone()
      if(row is None):
        raise Exception('INVALID_CREDENTIALS')
      id = row[0]
      # return '''{}'''.format(service.jwt_encode(id).replace('b\'', '').replace('\'', ''))
      return jsonify({ 'success': True, 'data': { 'id': id, 'token': service.jwt_encode(id).decode("utf-8") } })
    except Exception as e:
      return abort(make_response(jsonify(message=str(e)), 400))
    finally:
      cur.close()
      conn.close()

  def jwtauthorize(conn, token):
    cur = conn.cursor()
    try:
      id = service.jwt_decode(token)
      cur.execute(strings.jwtauthorize(id))
      row = cur.fetchone()
      if(row is None):
        raise Exception('INVALID_CREDENTIALS')
      id = row[0]
      return jsonify({ 'success': True, 'data': { 'token': token, 'id': id } })
    except Exception as e:
      return abort(make_response(jsonify(message=str(e)), 400))
    finally:
      cur.close()
      conn.close()

  def changePassword(conn, id, password):
    cur = conn.cursor()
    try:
      cur.execute(strings.changePassword(id, password))
      conn.commit()
      return jsonify({ 'success': True, 'data': { 'token': service.jwt_encode(id) } })
    except Exception as e:
      return abort(make_response(jsonify(message=str(e)), 400))
    finally:
      cur.close()
      conn.close()

  def changeData(conn, token, fields):
    cur = conn.cursor()
    try:
      fieldsStr = ', '.join(map(lambda x: '''{} = \'{}\''''.format(x, fields[x]), fields.keys()))
      id = service.jwt_decode(token)
      cur.execute(strings.changeData(id, fieldsStr))
      row = cur.fetchone()
      if(row is None):
        raise Exception('UNEXPECTED_ERROR')
      conn.commit()
      return jsonify({ 'success': True, 'data': { 'token': service.jwt_encode(id) } })
    except Exception as e:
      print(str(e))
      if(str(e) == 'INVALID_TOKEN' or str(e) == 'TOKEN_EXPIRED'):
        return abort(make_response(jsonify(message=str(e)), 403))
      return abort(make_response(jsonify(message=str(e)), 400))
    finally:
      cur.close()
      conn.close()