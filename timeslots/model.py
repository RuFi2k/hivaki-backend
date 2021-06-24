class models:
  def getModel(row):
    return {
      'id': row[0],
      'timestart': row[1],
      'timeend': row[2],
      'status': row[3],
    }
  
  def getActive(row):
    return {
      'year': row[0],
      'month': row[1],
      'day': row[2],
      'slots': row[3],
    }