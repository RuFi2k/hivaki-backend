class strings:
  def getAllTimeslots(limit, offset):
    return '''SELECT
      EXTRACT(YEAR from timestart) AS year,
      EXTRACT(MONTH from timestart) AS month,
      EXTRACT(DAY from timestart) AS day,
      json_agg(
        json_build_object(
            'id', id,
            'status', status,
            'start', json_build_object('hour', EXTRACT(HOUR from timestart), 'minute', EXTRACT(MINUTE from timestart)),
            'end', json_build_object('hour', EXTRACT(HOUR from t.timeend), 'minute', EXTRACT(MINUTE from t.timeend))
        )) as slots
      FROM (
        SELECT id, timestart, timeend, status
        FROM timeslots
        WHERE timestart > CURRENT_TIMESTAMP
      ) t
      GROUP BY 1,2,3
      ORDER BY year, month, day
      LIMIT {} OFFSET {}'''.format(limit, offset)

  def getActiveTimeslots():
    return '''SELECT
      EXTRACT(YEAR from timestart) AS year,
      EXTRACT(MONTH from timestart) AS month,
      EXTRACT(DAY from timestart) AS day,
      json_agg(
        json_build_object(
            'id', id,
            'start', json_build_object('hour', EXTRACT(HOUR from timestart), 'minute', EXTRACT(MINUTE from timestart)),
            'end', json_build_object('hour', EXTRACT(HOUR from t.timeend), 'minute', EXTRACT(MINUTE from t.timeend))
        )) as slots
      FROM (
        SELECT id, timestart, timeend, status
        FROM timeslots
        WHERE timestart > CURRENT_TIMESTAMP
        AND status = false
      ) t
      GROUP BY 1,2,3
      ORDER BY year, month, day'''

  def createTimeslot(slots):
    return '''INSERT INTO timeslots
    (timestart, timeend, status)
    VALUES {}
    RETURNING id, timestart, timeend, status'''.format(
      ", ".join(map(lambda x: '''(\'{}\', \'{}\', false)'''.format(x['start'], x['end']), slots))
    )

  def deleteTimeslot(id):
    return '''DELETE FROM timeslots
    WHERE id = \'{}\''''.format(id)