import redis

try:
	redis_client = redis.Redis(host='localhosst', port=5000, db=0)
	
	#check if connected, remove later
	redis_client.ping()
	print("Connected successfuly!")
except redis.exception.ConnectionError as e: #Told by AI to implement this as a placeholder
	print("Could not connect, error: " + str(e)) 
	redis_client = None
