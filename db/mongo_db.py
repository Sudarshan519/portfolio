import motor.motor_asyncio
from core.config import settings
client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URI)#os.environ["MONGODB_URI"])
db_mongo = client.college