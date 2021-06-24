class models:
  def getModel(row):
    return {
      'id': row[0],
      'name': row[1],
      'phone': row[2],
      'timestart': row[3],
      'timeend': row[4],
      'status': row[5],
    }