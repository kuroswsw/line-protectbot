import json
import threading
import time

rate_list = ["botkick","adminkick","memberkick","minvite","finvite","cancel","name","icon","url","allm","others"]

readjson = open('./data/rate.json')
rate = json.load(readjson)

def rate_save():
	with open("./data/rate.json",'w') as f:
		json.dump(rate,f,indent=4)

def comp_data():
	for mid in rate["rate"]:
		rate["rate"][mid]["others"]=0
	rate_save()

def create_rate(mid):
	rate["rate"][mid]={"score":100,"botkick":0,"adminkick":0,"memberkick":0,"minvite":0,"finvite":0,"cancel":0,"name":0,"icon":0,"url":0,"allm":0,"others":0}
	rate_save()

def down_rate(mid,r_type,num=0):
	if mid not in rate["rate"]:
		create_rate(mid)
	if r_type not in rate_list:
		return
	if r_type == "botkick":
		if rate["rate"][mid]["botkick"] != 0:
			n_score = rate["rate"][mid]["botkick"] * 7
			rate["rate"][mid]["score"] -= int(n_score)
			rate["rate"][mid]["botkick"] += 1
			rate_save()
		else:
			rate["rate"][mid]["score"] -= 7
			rate["rate"][mid]["botkick"] += 1
			rate_save()
	if r_type == "adminkick":
		if rate["rate"][mid]["adminkick"] != 0:
			n_score = rate["rate"][mid]["adminkick"] * 3
			rate["rate"][mid]["score"] -= int(n_score)
			rate["rate"][mid]["adminkick"] += 1
			rate_save()
		else:
			rate["rate"][mid]["score"] -= 3
			rate["rate"][mid]["adminkick"] += 1
			rate_save()
	if r_type == "memberkick":
		if rate["rate"][mid]["memberkick"] != 0:
			n_score = rate["rate"][mid]["memberkick"] * 3
			rate["rate"][mid]["score"] -= int(n_score)
			rate["rate"][mid]["memberkick"] += 1
			rate_save()
		else:
			rate["rate"][mid]["score"] -= 3
			rate["rate"][mid]["memberkick"] += 1
			rate_save()
	if r_type == "minvite":
		if rate["rate"][mid]["minvite"] != 0:
			n_score = rate["rate"][mid]["minvite"] * 2
			rate["rate"][mid]["score"] -= int(n_score)
			rate["rate"][mid]["minvite"] += 1
			rate_save()
		else:
			rate["rate"][mid]["score"] -= 2
			rate["rate"][mid]["minvite"] += 1
			rate_save()
	if r_type == "finvite":
		if rate["rate"][mid]["finvite"] != 0:
			n_score = rate["rate"][mid]["finvite"] * 3
			rate["rate"][mid]["score"] -= int(n_score)
			rate["rate"][mid]["finvite"] += 1
			rate_save()
		else:
			rate["rate"][mid]["score"] -= 3
			rate["rate"][mid]["finvite"] += 1
			rate_save()
	if r_type == "cancel":
		if rate["rate"][mid]["cancel"] != 0:
			n_score = rate["rate"][mid]["cancel"] * 2
			rate["rate"][mid]["score"] -= int(n_score)
			rate["rate"][mid]["cancel"] += 1
			rate_save()
		else:
			rate["rate"][mid]["score"] -= 2
			rate["rate"][mid]["cancel"] += 1
			rate_save()
	if r_type == "name":
		if rate["rate"][mid]["name"] != 0:
			n_score = rate["rate"][mid]["name"] * 2
			rate["rate"][mid]["score"] -= int(n_score)
			rate["rate"][mid]["name"] += 1
			rate_save()
		else:
			rate["rate"][mid]["score"] -= 2
			rate["rate"][mid]["name"] += 1
			rate_save()
	if r_type == "icon":
		if rate["rate"][mid]["icon"] != 0:
			n_score = rate["rate"][mid]["icon"] * 2
			rate["rate"][mid]["score"] -= int(n_score)
			rate["rate"][mid]["icon"] += 1
			rate_save()
		else:
			rate["rate"][mid]["score"] -= 2
			rate["rate"][mid]["icon"] += 1
			rate_save()
	if r_type == "url":
		if rate["rate"][mid]["url"] != 0:
			n_score = rate["rate"][mid]["url"] * 3
			rate["rate"][mid]["score"] -= int(n_score)
			rate["rate"][mid]["url"] += 1
			rate_save()
		else:
			rate["rate"][mid]["score"] -= 3
			rate["rate"][mid]["url"] += 1
			rate_save()
	if r_type == "allm":
		if rate["rate"][mid]["allm"] != 0:
			n_score = rate["rate"][mid]["allm"] * 3
			rate["rate"][mid]["score"] -= int(n_score)
			rate["rate"][mid]["allm"] += 1
			rate_save()
		else:
			rate["rate"][mid]["score"] -= 3
			rate["rate"][mid]["allm"] += 1
			rate_save()
	if r_type == "others":
		if rate["rate"][mid]["others"] != 0:
			#n_score = rate["rate"][mid]["others"] * 0
			rate["rate"][mid]["score"] -= int(num)
			rate["rate"][mid]["others"] += 1
			rate_save()
		else:
			rate["rate"][mid]["score"] -= int(num)
			rate["rate"][mid]["others"] += 1
			rate_save()

def check_rate(mid):
	if mid not in rate["rate"]:
		create_rate(mid)
	return rate["rate"][mid]["score"]

def change_rate(num,c_type,mid,r_type=None):
	if mid not in rate["rate"]:
		create_rate(mid)
	old_rate = rate["rate"][mid]["score"]
	if c_type == "+":
		rate["rate"][mid]["score"] += num
	elif c_type == "-":
		rate["rate"][mid]["score"] -= num
	else:
		pass
	if r_type is not None:
		if r_type in rate_list:
			rate["rate"][mid][r_type] += 1
	rate_save()
	return {"old_rate":old_rate,"new_rate":rate["rate"][mid]["score"],"r_type":r_type}

def recovery_rate():
	for mid in rate["rate"]:
		if rate["rate"][mid]["score"] < 100:
			all_violation_count = 0
			for r_type in rate_list:
				try:
					all_violation_count += rate["rate"][mid][r_type]
				except:
					pass
			if all_violation_count > 1:
				recovery_num = round(round(0.25 / all_violation_count, 5) * 2, 5)
				rate["rate"][mid]["score"] += recovery_num
			else:
				rate["rate"][mid]["score"] += 0.25
	rate_save()