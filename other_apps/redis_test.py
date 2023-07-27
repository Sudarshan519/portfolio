# import redis

# # Replace these values with your actual Redis server configuration
# REDIS_HOST = 'localhost'
# REDIS_PORT = 6379
# REDIS_PASSWORD = None  # Set to the password if your Redis server requires authentication

# # Create a Redis client
# redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)

# # Test the connection
# try:
#     pong_response = redis_client.ping()
#     if pong_response == True:
#         print("Connected to Redis successfully!")
#     else:
#         print("Failed to connect to Redis.")
# except redis.exceptions.ConnectionError as e:
#     print(f"Connection error: {e}")
