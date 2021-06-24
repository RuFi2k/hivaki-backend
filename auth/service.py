import datetime
import jwt
import utils

class service:
  def jwt_decode(token):
    try:
      payload = jwt.decode(token, utils.SECRET_KEY, algorithms='HS256')
      return payload['sub']
    except jwt.ExpiredSignatureError:
      raise Exception('TOKEN_EXPIRED')
    except jwt.InvalidTokenError:
      raise Exception('INVALID_TOKEN')

  def jwt_encode(user_id):
    try:
      payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=3),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
      }
      return jwt.encode(
        payload,
        utils.SECRET_KEY,
        algorithm='HS256'
      )
    except Exception as e:
        return e