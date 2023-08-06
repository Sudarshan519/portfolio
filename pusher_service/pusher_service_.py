# First, run 'pip install pusher'

from pydantic import BaseModel
import pusher

pusher_client = pusher.Pusher(
  app_id='1644680',
  key='27748d5ceeba4d889228',
  secret='ddb21ebd3b8c5e0b262e',
  cluster='mt1',
  ssl=True
)
MY_CHANNEL="my-channel"
MY_EVENT="my-event"
# curl -H 'Content-Type: application/json' -d '{"data":"{\"message\":\"hello world\"}","name":"my-event","channel":"my-channel"}' \
# "https://api-mt1.pusher.com/apps/1644680/events?"\
# "body_md5=2c99321eeba901356c4c7998da9be9e0&"\
# "auth_version=1.0&"\
# "auth_key=27748d5ceeba4d889228&"\
# "auth_timestamp=1690908953&"\
# "auth_signature=9adbb5902b7ca9cf9323ce90a507c2f4dc886a06e5415286ea82a66203958c3c&"


class EventModel(BaseModel):
    channelName:str
    event:str
    data:dict
class PusherService:
    @staticmethod
    def triggerEvent(event:EventModel):
        pusher_client.trigger('my-channel', 'my-event', {'message': 'hello world'})

