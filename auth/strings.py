class strings:
  def authorize(login, password):
    return '''SELECT id
      FROM booking.users
      WHERE login = \'{}\' AND password = \'{}\''''.format(login, password)

  def jwtauthorize(id):
    return '''SELECT id
    FROM booking.users
    WHERE id = \'{}\''''.format(id)

  def changeData(id, fieldsStr):
    return '''UPDATE booking.users
    SET {}
    WHERE id = \'{}\'
    RETURNING id'''.format(fieldsStr, id)