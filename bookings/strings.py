class strings:  
  def getBookingsString(limit, offset):
    return '''SELECT
      B.id,
      name,
      phone,
      timestart,
      timeend,
      B.status
      FROM bookings B
      JOIN timeslots T
      ON B.timeslotid = T.id
      ORDER BY timestart DESC LIMIT {} OFFSET {}'''.format(limit, offset)

  def getBooking(id):
    return '''SELECT
      B.id,
      name,
      phone,
      timestart,
      timeend,
      B.status
      FROM bookings B
      JOIN timeslots T
      ON B.timeslotid = T.id
      WHERE B.id = \'{}\''''.format(id)

  def createBooking(name, phone, timeslotid):
    # return '''INSERT INTO booking.bookings
    # (name, phone, timeslotid)
    # VALUES (\'{}\', \'{}\', \'{}\')
    # RETURNING id'''.format(name, phone, timeslotid)
    return '''INSERT INTO bookings (name, phone, timeslotid, status)
    SELECT \'{}\', \'{}\', \'{}\', \'ACTIVE\'
    WHERE EXISTS (SELECT * FROM timeslots T WHERE T.id = \'{}\' AND T.status = false)
    RETURNING id'''.format(name.replace('\'', '\'\''), phone.replace('\'', '\'\''), timeslotid, timeslotid)

  def updateTimeslotStatus(id, status):
    return '''UPDATE timeslots
    SET status = {}
    WHERE id = \'{}\''''.format(status, id)

  def setBookingStatus(id, status):
    return '''update bookings B
      set status = \'{}\'
      from (
        select timestart, timeend
        from bookings B join timeslots T on B.timeslotid = T.id
      ) sub
      where B.id = \'{}\'
      returning B.id, B.name, phone, sub.timestart, sub.timeend, B.status'''.format(status, id)
