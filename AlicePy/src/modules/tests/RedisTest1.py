import redis
r = redis.Redis(
    host='local',
    port=6379)
# r = redis.StrictRedis(host='mohu.local', port=6379).keys()
r.set('name', 'mohu')
val = r.get('name')
print(val)

# users = [{"Name":"Pradeep", "Company":"SCTL", "Address":"Mumbai", "Location":"RCP"}, {"Name":"Pradeep1", "Company":"SCTL", "Address":"Mumbai", "Location":"RCP"}]
# for user in users:
# 	r.lpush("pythonDict", user)

r.hset("pythonDict", "Name","Pradeep")
r.hset("pythonDict", "Company","SCTL")
r.hset("pythonDict", "Address","Mumbai")
r.hset("pythonDict", "Location","RCP")

vals = r.hgetall('pythonDict')
print(vals)