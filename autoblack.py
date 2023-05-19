import time,json,threading,math,rate,random

violation = {"botkick":10800,"adminkick":1800,"memberkick":900,"m_invite":600,"f_invite":1800,"cancel":600,"name":600,"icon":600,"url":600,"allm":600}

readjson = open('./data/autoblack.json')
data = json.load(readjson)

def data_save():
	with open("./data/autoblack.json",'w') as f:
		json.dump(data,f,indent=4)

def check_keys(autoblack_id):
	autoblack_id = int(autoblack_id)
	if str(autoblack_id) not in data["blackid_uid"]:
		return "Error"
	mid = data["blackid_uid"][f"{str(autoblack_id)}"]["mid"]
	gid = data["blackid_uid"][f"{str(autoblack_id)}"]["gid"]
	return {"mid":mid,"gid":gid}

def del_autoblack(autoblack_id):
	autoblack_id = int(autoblack_id)
	if str(autoblack_id) not in data["blackid_uid"]:
		return "Error"
	temp_check_key = check_keys(autoblack_id)
	count = data["autoblack"][temp_check_key["gid"]][temp_check_key["mid"]]["time"]
	for i in range(count):
		time.sleep(1)
		try:
			data["autoblack"][temp_check_key["gid"]][temp_check_key["mid"]]["time"] -= 1
			data_save()
		except:
			return
	del data["autoblack"][temp_check_key["gid"]][temp_check_key["mid"]]
	del data["blackid_uid"][f"{str(autoblack_id)}"]
	data["autoblack_list"][temp_check_key["gid"]].remove(temp_check_key["mid"])
	data_save()

def time_check(gid,mid):
	if gid not in data["autoblack"]:
		return False
	elif mid not in data["autoblack"][gid]:
		return False
	elif mid in data["autoblack"][gid]:
		return data["autoblack"][gid][mid]["time"]

def check(autoblack_id):
	autoblack_id = int(autoblack_id)
	if str(autoblack_id) not in data["blackid_uid"]:
		return None
	mid = data["blackid_uid"][f"{str(autoblack_id)}"]["mid"]
	gid = data["blackid_uid"][f"{str(autoblack_id)}"]["gid"]
	v_type = data["blackid_uid"][f"{str(autoblack_id)}"]["v_type"]
	i_time = data["blackid_uid"][f"{str(autoblack_id)}"]["i_time"]
	try:
		l_time = data["autoblack"][gid][mid]["time"]
	except:
		l_time = None
	return {"mid":mid,"gid":gid,"v_type":v_type,"i_time":i_time,"l_time":l_time}

def check_blacklist(gid,mid):
	if gid not in data["autoblack_list"]:
		data["autoblack_list"][gid]=[]
		data_save()
	return data["autoblack_list"][gid]

def black_del(autoblack_id):
	autoblack_id = int(autoblack_id)
	try:
		temp_check_key = check_keys(autoblack_id)
		gid = temp_check_key["gid"]
		mid = temp_check_key["mid"]
	except:
		return False
	if gid not in data["autoblack"]:
		return False
	elif mid not in data["autoblack"][gid]:
		return False
	elif mid in data["autoblack"][gid]:
		del data["autoblack"][temp_check_key["gid"]][temp_check_key["mid"]]
		del data["blackid_uid"][f"{str(autoblack_id)}"]
		data["autoblack_list"][gid].remove(mid)
		data_save()
		return "success"

def black_del_uid(gid,mid):
	if gid not in data["autoblack"]:
		return "Error"
	elif mid not in data["autoblack"][gid]:
		return "Error"
	elif mid in data["autoblack"][gid]:
		if black_del(data["autoblack"][gid][mid]["ab_id"]) == "success":
			return "success"

def black_check(gid,mid):
	if gid not in data["autoblack"]:
		return False
	elif mid not in data["autoblack"][gid]:
		return False
	elif mid in data["autoblack"][gid]:
		return True

def put(gid,mid,v_type=None,V2_time=600):
	black_time = 0
	if mid not in data["user"]:
		data["user"][mid]={"all_violation":0}
		data_save()
	if gid not in data["user"][mid]:
		data["user"][mid][gid]={"save_data":{"all_v":0},"violation":{"v_all":0,"botkick": 0,"adminkick": 0,"memberkick": 0,"m_invite": 0,"f_invite": 0,"cancel": 0,"name": 0,"icon": 0,"url": 0,"allm": 0,"others": 0}}
		data_save()
	if v_type in violation:
		v_to_count = data["user"][mid][gid]["violation"][v_type]
		v_to_all_count = data["user"][mid][gid]["violation"]["v_all"]
		v_all_count = data["user"][mid]["all_violation"]
		data["user"][mid][gid]["violation"][v_type] += 1
		data["user"][mid][gid]["violation"]["v_all"] += 1
		data["user"][mid]["all_violation"] += 1
		data_save()
	elif v_type not in violation:
		v_to_count = 1
		v_all_count = data["user"][mid]["all_violation"]
		v_to_all_count = data["user"][mid][gid]["violation"]["v_all"]
		data["user"][mid][gid]["violation"]["v_all"] += 1
		data_save()
	if v_to_count == 0:
		v_to_count += 1
		data_save()
	if v_to_all_count == 0:
		v_to_all_count += 1
		data_save()
	if data["user"][mid][gid]["save_data"]["all_v"] == 0:
		data["user"][mid][gid]["save_data"]["all_v"] += 1
		all_v_count = data["user"][mid][gid]["save_data"]["all_v"]
		data_save()
	else:
		all_v_count = data["user"][mid][gid]["save_data"]["all_v"]
		data["user"][mid][gid]["save_data"]["all_v"] += 1
		data_save()
	score = rate.check_rate(mid)
	temp_score = score
	temp_score = 100 - temp_score
	temp_score = math.floor(temp_score) * 600
	score_time = temp_score
	if v_type is not None:
		temp_black_time = violation[v_type]
		temp_black_time = temp_black_time * v_to_count
		temp_black_time = temp_black_time * v_to_all_count
		temp_black_time = temp_black_time + score_time
		black_time = temp_black_time
	else:
		temp_all_count = v_all_count - all_v_count
		if temp_all_count < 1:
			temp_v_all_count = 1
		else:
			temp_v_all_count = temp_all_count
		temp_score_time = score_time * 2
		temp_black_time = V2_time
		temp_black_time = temp_black_time * v_to_all_count
		temp_black_time = temp_black_time * all_v_count
		temp_black_time = temp_black_time * temp_v_all_count
		temp_black_time = temp_black_time + temp_score_time
		black_time = temp_black_time
	autoblack_id = int(random.randint(1000000, 9999999))
	if gid not in data["autoblack"]:
		data["autoblack"][gid]={mid:{"ab_id":autoblack_id,"time":black_time}}
		data_save()
	else:
		data["autoblack"][gid][mid]={"ab_id":autoblack_id,"time":black_time}
		data_save()
	data["blackid_uid"][f"{str(autoblack_id)}"]={"mid":mid,"gid":gid,"v_type":v_type,"i_time":black_time}
	if gid in data["autoblack_list"]:
		data["autoblack_list"][gid].append(mid)
		data_save()
	elif gid not in data["autoblack_list"]:
		data["autoblack_list"][gid]=[]
		data["autoblack_list"][gid].append(mid)
		data_save()
	data_save()
	threading.Thread(target=del_autoblack,args=(autoblack_id,)).start()
	return {"ab_id":autoblack_id,"time":black_time}