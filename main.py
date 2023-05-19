import sys
from CHRLINE import *
import threading
from KuroUtil import Kurosawa
import time, os, concurrent, asyncio, random, json, requests, datetime, copy, string, base64, concurrent, timeit, re, wait, rate, autoblack

#-----------#
allbot = [] #
kbot   = [] #
allmid = [] #
kmid   = [] #
#-----------#

setlist = ["kick","inv","url","cancel","name","pic","allm","ng","joinms"]

"""setting"""
ver = "v3.0.3"
test_message_mid = "u1efb5e6be2aeef645991031d5b515da5"
admin_group = ""
kuroswsw = "u3629e2dc9c1abb89d6defe27f779aa35"
wait_data = {}
"""-------"""

helpmessage_old=f"""-lv0 or invitee
test
help
check1
check2
check3

set:on/off:[key] #設定
#key:{setlist}

add/del:[key] @
#key:gwlist,gblist
#メンションなしで連絡先から登録,finで登録終了

joinms:[message]
#空白でメッセージ削除
#@kurosawaでメンション

join #足りないbot参加

un:[num]

-invitee
add/del:lv0 @ #グル別権限
invitee @ #招待者変更
leave

-lv2
add/del:lv1

-lv3
add/del:lv[1,2,3]

-all
add/del:[key] @
#key:black,white
#メンションなしで連絡先から登録,finで登録終了

mc

-dev
.ver
mk @
noop"""

helpmessage = """dhelpを使用してください"""

lines = [line.strip('\n') for line in open('./data/token.txt', 'r')]

botlen = 0
for i in lines:
	mp = i.split(',')
	mail = mp[0]
	password = mp[1]
	iclient = 0
	try:
		ilogin = CHRLINE(mail,password,device='DESKTOPWIN')
		if botlen == 0:
			cl = ilogin
			botlen + 1
			iclient + 1
		allbot.append(ilogin)
		allmid.append(ilogin.mid)
		if iclient == 0:
			kbot.append(ilogin)
			kmid.append(ilogin.mid)
	except Exception as e:
		print(e)
		print(mail)

swsw = Kurosawa(cl,allbot,allmid,kbot,kmid)

#bot追加
for i in allbot:
	clist = allmid.copy()
	clist.remove(i.mid)
	fmid = i.getAllContactIds()
	for m in clist:
		if m not in fmid:
			try:
				i.findAndAddContactsByMid(m)
			except:
				print("add error")

readjson = open('./data/data.json')
data = json.load(readjson)

mention_data_json = open('./data/mention_data.json')
mention_data = json.load(mention_data_json)

commands_data_json = open('./data/commands.json')
commands = json.load(commands_data_json)

def data_save():
	with open("./data/data.json",'w') as f:
		json.dump(data,f,indent=4)

def mention_data_save():
	with open("./data/mention_data.json",'w') as f:
		json.dump(mention_data,f,indent=4)

def joinBots(gid,cl=cl):
	a=cl.getChatJoinMids(gid)
	li=[]
	for i in allbot:
		if i.mid in a:
			li.append(i)
	return li

def join(gid,cl=cl):
	try:
		random.choice(joinBots(gid,cl)).inviteIntoChat(gid,[c for c in allmid if c not in cl.getChatAllMids(gid)])
	except Exception as e:
		cl.sendCompactMessage(gid,e)
		return
	for i in allbot:
		a=i.getAllChatMids()
		if gid not in a[1]:
			i.acceptChatInvitation(gid)
	cl.sendCompactMessage(gid,"fin")

def gen_metadata(ms,m_mid):
	li=[i.start() for i in re.finditer("@kurosawa", ms)]
	m=[]
	for i in li:
		m.append({'S': i, 'L': 9, 'M': f"{m_mid}"})
	m=random.choice(allbot).genMentionData(m)
	return m

def asyncio_message(to,ms,cl=random.choice(allbot)):
	asyncio.new_event_loop().run_in_executor(None, cl.sendMessage, to, ms)

"""
def del_autoblack(to,mid,autoblack_id,sec=600):
	try:
		count = int(sec)
		count -= 1
		for i in range(int(sec)):
			wait_data[autoblack_id] = count
			count -= 1
			time.sleep(1)
		del data["autoblack"][to][mid]
		del wait_data[autoblack_id]
		data_save()
		#random.choice(allbot).sendMessage(to,f"<{random.choice(allbot).getContact(mid)[22]}>\nブラックリストから削除されました")
	except Exception as e:
		print(e)

def autoblack(to,mid,autoblack_id,sec=600):
	threading.Thread(target=del_autoblack,args=(to,mid,autoblack_id,sec,)).start()

def check_autoblack_time(autoblack_id):
	try:
		wait_data[autoblack_id]
	except:
		return "Error"
	return wait_data[autoblack_id]
"""

def recovery_rate_a():
	while True:
		time.sleep(3600)
		rate.recovery_rate()

def jl_log(gid,mid):
	time.sleep(0.3)
	g_g = random.choice(allbot).getChats([gid])
	ra = random.choice(allbot)
	ra.sendMessage("",f"name：{g_g[1][0][6]}\njoin：{str(len(list(g_g[1][0][8][1][4].keys())))}\ninvitation：{str(len(list(g_g[1][0][8][1][5].keys())))}")
	ra.sendContact("",mid)

def bot(op,cl):
	if op[3] == 124 and cl.mid in op[12]:
		gid=op[10]
		if op[11] in data["dev"] or op[11] in data["lv1"] or op[11] in data["lv2"] or op[11] in data["lv3"] or op[11] in data["lv4"]:
			chatallmids = cl.getChatAllMids(op[10])
			invitemid = cl.getChatInviteMids(op[10])
			if all(i in chatallmids for i in allmid):
				if wait.check(f"join:{op[11]}") is None:
					wait.wait(180,f"join:{op[11]}")
					for i in allbot:
						if i.mid in invitemid:
							i.acceptChatInvitation(op[10])
					if "kurosawa" == "kurosawa":
						data["invadmin"][op[10]]=op[11]
						data["kick"][op[10]]=False
						data["inv"][op[10]]=False
						data["url"][op[10]]=False
						data["cancel"][op[10]]=False
						data["name"][op[10]]=False
						data["pic"][op[10]]=False
						data["allm"][op[10]]=False
						data["ng"][op[10]]=False
						data["lv0"][op[10]]=[]
						data["gwlist"][op[10]]=[]
						data["gblist"][op[10]]=[]
						data["lflag"][op[10]]=False
						data["joinklist"][op[10]]=[]
						data["joinms"][op[10]]={
							"send_TF":False,
							"message":None
						}
						data_save()
						random.choice(allbot).sendMessage(op[10],"保護bot無料配布中です\n質問や悪用報告はこちら↓")
						random.choice(allbot).sendContact(op[10],"u3629e2dc9c1abb89d6defe27f779aa35")
						try:
							swsw.log(f"joined\n\n{op[10]}\n{op[11]}")
							asyncio.new_event_loop().run_in_executor(None, jl_log, op[10], op[11])
						except Exception as e:
							print(e)
					else:
						data["invadmin"][op[10]]=op[11]
						data_save()
						random.choice(allbot).sendMessage(op[10],"保護bot無料配布中です\n質問や悪用報告はこちら↓")
						random.choice(allbot).sendContact(op[10],"u3629e2dc9c1abb89d6defe27f779aa35")
						try:
							swsw.log(f"joined\n\n{op[10]}\n{op[11]}")
							asyncio.new_event_loop().run_in_executor(None, jl_log, op[10], op[11])
						except Exception as e:
							print(e)
				else:
					random.choice(allbot).sendMessage(op[11],"前回の招待から3分以上経過していないため参加しません")
		
		else:
			allg=cl.getAllChatMids()
			if op[10] in allg[1]:
				if op[10] not in data["invadmin"]:
					cl.deleteSelfFromChat(op[10])
					swsw.log(f"{op[10]}\n{op[11]}")

	if op[3] == 124 and cl.mid not in op[12]:
		gid = op[10]
		if op[11] in data["dev"] or op[11] in data["lv0"][gid] or op[11] in data["invadmin"][gid] or op[11] in data["gwlist"][gid] or op[11] in data["swlist"]:
			return
		try:
			if op[11] in data["wlist"][data["invadmin"][op[10]]]:
				return
		except:
			pass

		try:
			autoblack_list = autoblack.check_blacklist(op[10])
			if len(autoblack_list) >= 1:
				black_mid = list(set(autoblack_list) & set(op[12].split("\x1e")))
				if len(black_mid) >= 1:
					random.choice(kbot).deleteOtherFromChat(op[10],op[11])
					if len(black_mid) <= 7:
						for i in black_mid:
							random.choice(kbot).cancelChatInvitation(op[10],i)

		except Exception as e:
			print(e)

		all_black_list = []
		try:
			all_black_list += data["gblist"][op[10]]
		except:
			pass

		try:
			all_black_list += data["sblist"]
		except:
			pass

		try:
			mid=data["invadmin"][op[10]]
			all_black_list += data["blist"][mid]
		except:
			pass
		all_black_list = list(set(all_black_list))
		if len(all_black_list) >= 1:
			cancel_mid = list(set(all_black_list) & set(op[12].split("\x1e")))
			if len(cancel_mid) >= 1:
				random.choice(kbot).deleteOtherFromChat(op[10],op[11])
				if len(cancel_mid) <= 7:
					for i in cancel_mid:
						random.choice(kbot).cancelChatInvitation(op[10],i)
					mid = op[11]
					abt = autoblack.put(op[10],mid,"m_invite")
					random.choice(allbot).sendMessage(op[10],f"""{mid[:5]} >> autoblack\n解除：{str(abt["time"])}秒\nid：{str(abt["ab_id"])}""")
					rate.down_rate(mid,"minvite")

				else:
					mid = op[11]
					abt = autoblack.put(op[10],mid,"f_invite")
					random.choice(allbot).sendMessage(op[10],f"""{mid[:5]} >> autoblack\n解除：{str(abt["time"])}秒\nid：{str(abt["ab_id"])}""")
					rate.down_rate(mid,"finvite")

		if data["inv"][op[10]] == True:
			if op[11] in allmid:
				return
			random.choice(kbot).deleteOtherFromChat(op[10],op[11])
			inv_list = op[12].split("\x1e")
			if len(inv_list) <= 7:
				sec = 900
				for i in inv_list:
					random.choice(kbot).cancelChatInvitation(op[10],i)
			else:
				sec = 3600
				for i in inv_list:
					data["joinklist"][op[10]].append(i)
				data_save()
			mid = op[11]
			if len(inv_list) <= 7:
				abt = autoblack.put(op[10],mid,"m_invite")
				random.choice(allbot).sendMessage(op[10],f"""{mid[:5]} >> autoblack\n解除：{str(abt["time"])}秒\nid：{str(abt["ab_id"])}""")
				rate.down_rate(mid,"minvite")
			else:
				abt = autoblack.put(op[10],mid,"f_invite")
				random.choice(allbot).sendMessage(op[10],f"""{mid[:5]} >> autoblack\n解除：{str(abt["time"])}秒\nid：{str(abt["ab_id"])}""")
				rate.down_rate(mid,"finvite")
	
	elif op[3] == 55:
		if op[11] in allmid:
			return
		try:
			if op[11] in data["gblist"][op[10]]:
				random.choice(kbot).deleteOtherFromChat(op[10],op[11])
		except:
			pass

		try:
			if op[11] in data["sblist"]:
				random.choice(kbot).deleteOtherFromChat(op[10],op[11])
		except:
			pass

		try:
			if autoblack.black_check(op[10],op[11]):
				random.choice(kbot).deleteOtherFromChat(op[10],op[11])
		except:
			pass
		try:
			mid=data["invadmin"][op[10]]
			if op[11] in data["blist"][mid]:
				random.choice(kbot).deleteOtherFromChat(op[10],op[11])
		except:
			pass



	elif op[3] == 130:
		if op[11] in allmid:
			return
		try:
			if op[11] in data["joinklist"][op[10]]:
				random.choice(kbot).deleteOtherFromChat(op[10],op[11])
				data["joinklist"][op[10]].remove(op[11])
				data_save()
		except:
			pass

		try:
			if op[11] in data["gblist"][op[10]]:
				random.choice(kbot).deleteOtherFromChat(op[10],op[11])
		except:
			pass

		try:
			if op[11] in data["sblist"]:
				random.choice(kbot).deleteOtherFromChat(op[10],op[11])
		except:
			pass

		try:
			if autoblack.black_check(op[10],op[11]):
				random.choice(kbot).deleteOtherFromChat(op[10],op[11])
		except:
			pass

		try:
			mid=data["invadmin"][op[10]]
			if op[11] in data["blist"][mid]:
				random.choice(kbot).deleteOtherFromChat(op[10],op[11])
		except:
			pass

		try:
			if data["joinms"][op[10]]["send_TF"] == True:
				try:
					if op[11] in random.choice(allbot).getChatJoinMids(op[10]):
						if data["joinms"][op[10]]["message"] is not None:
							message = data["joinms"][op[10]]["message"]
							metadata = gen_metadata(message,op[11])
							random.choice(allbot).sendMessage(op[10],message,contentMetadata=metadata)
				except:
					pass
		except:
			pass

	elif op[3] in [125,126]:
		gid=op[10]
		if op[11] in data["joinklist"][op[10]]:
			data["joinklist"][op[10]].remove(op[11])
			data_save()
		if op[11] in allmid:
			return
		if op[12] in data["dev"] or op[12] in data["invadmin"][gid]:
			random.choice(kbot).deleteOtherFromChat(op[10],op[11])
			ct = op[12]
			ra = random.choice(kbot)
			if ct not in ra.getAllContactIds():
				ra.findAndAddContactsByMid(ct)
			ra.inviteIntoChat(to,[ct])
			mid = op[11]
			abt = autoblack.put(op[10],mid,"cancel")
			random.choice(allbot).sendMessage(op[10],f"""{mid[:5]} >> autoblack\n解除：{str(abt["time"])}秒\nid：{str(abt["ab_id"])}""")
			rate.down_rate(mid,"cancel")
		elif data["cancel"][op[10]] == True:
			gid=op[10]
			gadmin=data["invadmin"][gid]
			if op[11] in allmid:
				return
			if op[11] in data["dev"] or op[11] in data["lv0"][gid] or op[11] in data["invadmin"][gid] or op[11] in data["swlist"]:
				return
			try:
				if op[11] in data["gwlist"][gid]:
					return
			except:
				pass
			try:
				if op[11] in data["wlist"][gadmin]:
					return
			except:
				pass
			random.choice(kbot).deleteOtherFromChat(op[10],op[11])
			mid = op[11]
			abt = autoblack.put(op[10],mid,"cancel")
			random.choice(allbot).sendMessage(op[10],f"""{mid[:5]} >> autoblack\n解除：{str(abt["time"])}秒\nid：{str(abt["ab_id"])}""")
			rate.down_rate(mid,"cancel")

	elif op[3] in [121,122]:
		if op[11] in allmid:
			return
		if op[12] == "4":
			if data["url"][op[10]] == True:
				gid=op[10]
				gadmin=data["invadmin"][gid]
				if op[11] in data["dev"] or op[11] in data["lv0"][gid] or op[11] in data["invadmin"][gid]:
					return
				try:
					if op[11] in data["gwlist"][gid]:
						return
				except:
					pass
				try:
					if op[11] in data["wlist"][gadmin]:
						return
				except:
					pass
				random.choice(kbot).deleteOtherFromChat(op[10],op[11])
				mid = op[11]
				abt = autoblack.put(op[10],mid,"url")
				random.choice(allbot).sendMessage(op[10],f"""{mid[:5]} >> autoblack\n解除：{str(abt["time"])}秒\nid：{str(abt["ab_id"])}""")
				rate.down_rate(mid,"url")

		elif op[12] == "1":
			if data["name"][op[10]] == True:
				gid=op[10]
				gadmin=data["invadmin"][gid]
				if op[11] in data["dev"] or op[11] in data["lv0"][gid] or op[11] in data["invadmin"][gid]:
					return
				try:
					if op[11] in data["gwlist"][gid]:
						return
				except:
					pass
				try:
					if op[11] in data["wlist"][gadmin]:
						return
				except:
					pass
				random.choice(kbot).deleteOtherFromChat(op[10],op[11])
				mid = op[11]
				abt = autoblack.put(op[10],mid,"name")
				random.choice(allbot).sendMessage(op[10],f"""{mid[:5]} >> autoblack\n解除：{str(abt["time"])}秒\nid：{str(abt["ab_id"])}""")
				rate.down_rate(mid,"name")

		elif op[12] == "2":
			if data["pic"][op[10]] == True:
				gid=op[10]
				gadmin=data["invadmin"][gid]
				if op[11] in data["dev"] or op[11] in data["lv0"][gid] or op[11] in data["invadmin"][gid]:
					return
				try:
					if op[11] in data["gwlist"][gid]:
						return
				except:
					pass
				try:
					if op[11] in data["wlist"][gadmin]:
						return
				except:
					pass
				random.choice(kbot).deleteOtherFromChat(op[10],op[11])
				mid = op[11]
				abt = autoblack.put(op[10],mid,"icon")
				random.choice(allbot).sendMessage(op[10],f"""{mid[:5]} >> autoblack\n解除：{str(abt["time"])}秒\nid：{str(abt["ab_id"])}""")
				rate.down_rate(mid,"icon")

	elif op[3] == 19 or op[3] == 133:
		to = op[10]
		kf = op[11]
		kt = op[12]
		if kf in allmid:
			return
		gadmin = data["invadmin"][to]
		if kt in allmid:
			if kf not in data["dev"] and kf not in data["invadmin"][to]:
				jbot = []
				for i in allbot:
					if i.mid not in kt:
						jbot.append(i)
				random.choice(jbot).deleteOtherFromChat(to,kf)
				c=random.choice(jbot)
				join(to,c)
				mid = kf
				abt = autoblack.put(op[10],mid,"botkick")
				random.choice(allbot).sendMessage(op[10],f"""{mid[:5]} >> autoblack\n解除：{str(abt["time"])}秒\nid：{str(abt["ab_id"])}""")
				swsw.log(f"bot were kicked\n\n{to}\n{kf}")
				rate.down_rate(mid,"botkick")

		elif kt in data["dev"] or kt in data["lv0"][to] or kt in data["invadmin"][to]:
			if kf in data["dev"] or kf in data["invadmin"][to] or kf in data["swlist"]:
				return
			random.choice(kbot).deleteOtherFromChat(to,kf)
			ra = random.choice(kbot)
			if kt not in ra.getAllContactIds():
				ra.findAndAddContactsByMid(kt)
			ra.inviteIntoChat(to,[kt])
			mid = kf
			abt = autoblack.put(op[10],mid,"adminkick")
			random.choice(allbot).sendMessage(op[10],f"""{mid[:5]} >> autoblack\n解除：{str(abt["time"])}秒\nid：{str(abt["ab_id"])}""")
			swsw.log(f"admin were kicked\n\n{to}\n{kf}")
			rate.down_rate(mid,"adminkick")

		elif data["kick"][to] == True:
			gid=op[10]
			gadmin=data["invadmin"][gid]
			if op[11] in data["dev"] or op[11] in data["lv0"][gid] or op[11] in data["invadmin"][gid]:
				return
			try:
				if op[11] in data["gwlist"][gid]:
					return
			except:
				pass
			try:
				if op[11] in data["wlist"][gadmin]:
					return
			except:
				pass
			random.choice(kbot).deleteOtherFromChat(to,kf)
			mid = kf
			ms = ""
			try:
				abt = autoblack.put(op[10],mid,"memberkick")
				random.choice(allbot).sendMessage(op[10],f"""{mid[:5]} >> autoblack\n解除：{str(abt["time"])}秒\nid：{str(abt["ab_id"])}""")
				swsw.log(f"members were kicked\n\n{to}\n{kf}")
				rate.down_rate(mid,"memberkick")
			except Exception as e:
				print(e)
		else:
			pass	

	elif op[3] == 26:
		msg = op[20]
		to = msg[2]
		msg_from = msg[1]
		if msg[15] == 0:
			if msg[3] == 2:
				if 18 in msg:
					if '''"A":"1"''' in str(msg[18]):
						try:
							for i in cl.getChatAllMids(to):
								try:
									mention_data["mention_data"][to]
								except:
									mention_data["mention_data"][to]={}
								try:
									mention_data["mention_data"][to][i]
								except:
									mention_data["mention_data"][to][i]=[]
								try:
									mention_data["mention_data"][to][i].append(msg[4])
								except Exception as e:
									print(e)
							mention_data_save()
						except Exception as e:
							print(e)
						if data["allm"][to] == True:
							if msg_from in allmid:
								return
							gadmin=data["invadmin"][to]
							if msg_from in data["dev"] or msg_from in data["lv0"][to] or msg_from in data["invadmin"][to]:
								return
							try:
								if msg_from in data["gwlist"][to]:
									return
							except:
								pass
							try:
								if msg_from in data["wlist"][gadmin]:
									return
							except:
								pass
							random.choice(kbot).deleteOtherFromChat(to,msg_from)
							mid = msg_from
							abt = autoblack.put(op[10],mid,"allm")
							random.choice(allbot).sendMessage(op[10],f"""{mid[:5]} >> autoblack\n解除：{str(abt["time"])}秒\nid：{str(abt["ab_id"])}""")
							rate.down_rate(mid,"allm")
					else:
						try:
							metadata = msg[18]
							if 'MENTION' in metadata:
								key = eval(metadata["MENTION"])
								tags = key["MENTIONEES"]
								for tag in tags:
									mid = tag["M"]
									try:
										mention_data["mention_data"][to]
									except:
										mention_data["mention_data"][to]={}
									try:
										mention_data["mention_data"][to][mid]
									except:
										mention_data["mention_data"][to][mid]=[]
									try:
										mention_data["mention_data"][to][mid].append(msg[4])
									except:
										pass
								mention_data_save()
						except Exception as e:
							print(e)
				text = msg[10]
				try:
					mid=data["invadmin"][to]
					if msg_from in data["blist"][mid]:
						if msg_from in data["dev"]:
							return
						random.choice(kbot).deleteOtherFromChat(to,msg_from)
				except:
					pass
				try:
					if msg_from in data["gblist"][to]:
						if msg_from in data["dev"]:
							return
						random.choice(kbot).deleteOtherFromChat(to,msg_from)
				except:
					pass
				try:
					if autoblack.black_check(to,msg_from):
						if msg_from in data["dev"]:
							return
						random.choice(kbot).deleteOtherFromChat(to,msg_from)
				except:
					pass

				if text == "めんかく":
					if wait.check(f"mc:{msg_from}") is None:
						wait.wait(3,f"mc:{msg_from}")
						try:
							if not mention_data["mention_data"][to][msg_from]:
								random.choice(allbot).sendMessage(to,f"None")
							for i in mention_data["mention_data"][to][msg_from]:
								try:
									random.choice(allbot).sendMessage(to,f".",relatedMessageId=i)
									mention_data["mention_data"][to][msg_from].remove(i)
								except:
									pass
							time.sleep(0.1)
							mention_data_save()
							for i in mention_data["mention_data"][to][msg_from]:
								try:
									random.choice(allbot).sendMessage(to,f".",relatedMessageId=i)
									mention_data["mention_data"][to][msg_from].remove(i)
								except:
									pass
							time.sleep(0.1)
							mention_data_save()
							for i in mention_data["mention_data"][to][msg_from]:
								try:
									random.choice(allbot).sendMessage(to,f".",relatedMessageId=i)
									mention_data["mention_data"][to][msg_from].remove(i)
								except:
									pass
							time.sleep(0.1)
							mention_data_save()
							for i in mention_data["mention_data"][to][msg_from]:
								try:
									random.choice(allbot).sendMessage(to,f".",relatedMessageId=i)
									mention_data["mention_data"][to][msg_from].remove(i)
								except:
									pass
							time.sleep(0.1)
							mention_data_save()
							for i in mention_data["mention_data"][to][msg_from]:
								try:
									random.choice(allbot).sendMessage(to,f".",relatedMessageId=i)
									mention_data["mention_data"][to][msg_from].remove(i)
								except:
									pass
							time.sleep(0.1)
							mention_data_save()
						except Exception as e:
							random.choice(allbot).sendMessage(to,f"None")

				elif text == "acheck" or text == "権限":
					try:
						if wait.check(f"acheck:{msg_from}") is None:
							wait.wait(3,f"acheck:{msg_from}")
							adminname = f"<{msg_from[:7]}>\n"
							if msg_from in data["dev"]:
								adminname += f"\n-開発者権限"

							if msg_from in data["invadmin"][to]:
								adminname += f"\n-招待者権限"		

							if msg_from in data["lv0"][to]:
								adminname += f"\n-local"
						
							if msg_from in data["lv1"]:
								adminname += f"\n-user"

							if msg_from in data["lv2"]:
								adminname += f"\n-lv2"

							if msg_from in data["lv3"]:
								adminname += f"\n-lv3"

							if msg_from in data["lv4"]:
								adminname += f"\n-lv4"			

							if msg_from in data["gwlist"][to]:
								adminname += f"\n-グル別ホワリス"	

							if adminname == f"<{msg_from[:7]}>\n":
								random.choice(allbot).sendMessage(to,f"{adminname}\nnull")
							else:
								random.choice(allbot).sendMessage(to,adminname)
					except:
						pass

				elif text.startswith("idcheck:"):
					if wait.check(f"idcheck:{msg_from}") is None:
						wait.wait(6,f"idcheck:{msg_from}")
						cmd = text.split(":")
						try:
							autoblack_id = cmd[1]
							temp_check = autoblack.check(autoblack_id)
							if temp_check is None:
								return random.choice(allbot).sendMessage(to,"Error")
							ms = "autoblack status\n"
							ms += f"""\nname：{random.choice(allbot).getContact(temp_check["mid"])[22]}"""
							ms += f"""\ntype：{temp_check["v_type"]}"""
							ms += f"""\ntime：{str(temp_check["i_time"])}sec"""
							ms += f"""\ntime left：{str(temp_check["l_time"])}sec"""
							ms += f"""\nmid：{temp_check["mid"]}"""
							ms += f"""\ngid：{temp_check["gid"]}"""
							random.choice(allbot).sendMessage(to,ms)
						except:
							random.choice(allbot).sendMessage(to,"Error")

				if msg_from in data["dev"] or msg_from in data["lv1"] or msg_from in data["lv2"] or msg_from in data["lv3"] or msg_from in data["lv4"]or msg_from in data["lv0"][to]:
					text = msg[10]
					if text == "checkprefix":
						try:
							if msg_from in data["prefix"]:
								random.choice(allbot).sendMessage(to,data["prefix"][msg_from])
							else:
								random.choice(allbot).sendMessage(to,f"null")
						except:
							random.choice(allbot).sendMessage(to,f"null")

				text = msg[10]
				try:
					if not text.startswith(data["prefix"][msg_from]):
						return
				except:
					pass
				try:
					if text.startswith(data["prefix"][msg_from]):
						prefix_len = len(data["prefix"][msg_from])
						text = text[prefix_len:]
				except:
					pass
				if msg_from in data["dev"] or msg_from in data["lv1"] or msg_from in data["lv2"] or msg_from in data["lv3"] or msg_from in data["lv4"]or msg_from in data["lv0"][to]:

					if text == "test":
						count = 0
						for i in allbot:
							try:
								i.getContact("u3629e2dc9c1abb89d6defe27f779aa35")
								count += 1
							except:
								pass
						random.choice(allbot).sendMessage(to,f"{str(count)}/{str(len(allbot))} normal")

					elif text == "ver":
						random.choice(allbot).sendMessage(to,ver)

					elif text.startswith("mid"):
						try:
							metadata = msg[18]
							if 'MENTION' in metadata:
								key = eval(metadata["MENTION"])
								tags = key["MENTIONEES"]
								for tag in tags:
									mid = tag["M"]
									random.choice(allbot).sendMessage(to,mid)
						except:
							if text == "mid":
								random.choice(allbot).sendMessage(to,msg_from)

					elif text == "権限一覧"	:
						devname = ""
						lv1name = ""
						lv2name = ""
						lv3name = ""
						lv4name = ""
						ms = ""

						if not data["dev"]:
							devname += "-None\n"
						elif data["dev"]:
							for m in data["dev"]:
								devname += f"-{cl.getContact(m)[22]}\n"

						if not data["lv1"]:
							lv1name += "-None\n"
						elif data["lv1"]:
							for m in data["lv1"]:
								lv1name += f"-{cl.getContact(m)[22]}\n"

						if not data["lv2"]:
							lv2name += "-None\n"
						elif data["lv2"]:
							for m in data["lv2"]:
								lv2name += f"-{cl.getContact(m)[22]}\n"

						if not data["lv3"]:
							lv3name += "-None\n"
						elif data["lv3"]:
							for m in data["lv3"]:
								lv3name += f"-{cl.getContact(m)[22]}\n"

						if not data["lv4"]:
							lv4name += "-None\n"
						elif data["lv4"]:
							for m in data["lv4"]:
								lv4name += f"-{cl.getContact(m)[22]}\n"

						ms += f'権限一覧\n開発者権限\n{devname}\nuser\n{lv1name}\nlv2\n{lv2name}\nlv3\n{lv3name}\nlv4\n{lv4name}'
						random.choice(allbot).sendMessage(to,ms)

					elif text.startswith("prefix:"):
						new_prefix = text[7:]
						try:
							old_prefix = data["prefix"][msg_from]
						except:
							old_prefix = ""
						data["prefix"][msg_from]=new_prefix
						data_save()
						change_prefix_message = f"old_prefix：{old_prefix}\nnew_prefix：{new_prefix}"
						random.choice(allbot).sendMessage(to,change_prefix_message)

					elif text == "ucheck":
						try:
							whitename = ""
							blackname = ""
							adminname = ""
							ms = ""

							if msg_from not in data["wlist"]:
								whitename += "-None\n"
							elif not data["wlist"][msg_from]:
								whitename += "-None\n"
							elif data["wlist"][msg_from]:
								for m in data["wlist"][msg_from]:
									try:
										whitename += f"-{cl.getContact(m)[22]}\n"
									except:
										pass

							if msg_from not in data["blist"]:
								blackname += "-None"
							elif not data["blist"][msg_from]:
								blackname += "-None"
							elif data["blist"][msg_from]:
								for i, m in enumerate(data["blist"][msg_from]):
									if i == len(data["blist"][msg_from]) - 1:
										try:
											blackname += f"-{cl.getContact(m)[22]}"
										except:
											pass
									else:
										try:
											blackname += f"-{cl.getContact(m)[22]}\n"
										except:
											pass

							adminnamelist = ["dev","lv0","lv1","lv2","lv3","lv4"]
							for iadmin in adminnamelist:
								if "dev" in iadmin:
									if msg_from in data[iadmin]:
										adminname += f"-{iadmin}\n"
								elif "lv0" == iadmin:
									if to in data[iadmin]:
										if msg_from in data[iadmin][to]:
											adminname += f"-{iadmin}\n"
								elif "lv" in iadmin:
									if msg_from in data[iadmin]:
										adminname += f"-{iadmin}\n"

							ms += f'権限\n{adminname}\nホワリス\n{whitename}\nブラリス\n{blackname}'
							random.choice(allbot).sendMessage(to,ms)
						except Exception as e:
							print(e)

					elif text == "fin":
						flag=data["lflag"][to]
						if flag != False:
							data["lflag"][to]=False
							data_save()
							random.choice(allbot).sendMessage(to,f"{flag} >> fin")
						else:
							random.choice(allbot).sendMessage(to,"Error")

				if msg_from in data["dev"] or msg_from in data["lv0"][to] or msg_from in data["invadmin"][to]: #開発者orグル別権限or招待者

					if text == "help":
						ms = "shelp ふつうのhelp\ndhelp すごく詳しいhelp\nnotify おしらせ表示"
						random.choice(allbot).sendMessage(to,ms)

					elif text == "shelp":
						random.choice(allbot).sendMessage(to,helpmessage)

					elif text == "dhelp":
						ms = f"{ver} helpmessage"
						for i in commands:
							ms += f"\n\n{i}"
							for cmd in commands[i]:
								ms += f"\n{cmd}"
								for function in commands[i][cmd]["function"]:
									ms += f"\n>>{function}"
								if "example" in commands[i][cmd]:
									ms += f"""\n>>example: {commands[i][cmd]["example"]}"""
						random.choice(allbot).sendMessage(to,ms)

					elif text.startswith("hsearch:"):
						scmd = text[8:]
						ms = f"search：{scmd}"
						for i in commands:
							for cmd in commands[i]:
								if scmd in cmd or scmd in str(commands[i][cmd]["function"]):
									if i not in ms:
										ms += f"\n\n{i}"
									ms += f"\n{cmd}"
									for function in commands[i][cmd]["function"]:
										ms += f"\n>>{function}"
									if "example" in commands[i][cmd]:
										ms += f"""\n>>example: {commands[i][cmd]["example"]}"""
								elif "example" in commands[i][cmd]:
									if scmd in commands[i][cmd]["example"]:
										if i not in ms:
											ms += f"\n\n{i}"
										ms += f"\n{cmd}"
										for function in commands[i][cmd]["function"]:
											ms += f"\n>>{function}"
										if "example" in commands[i][cmd]:
											ms += f"""\n>>example: {commands[i][cmd]["example"]}"""
						random.choice(allbot).sendMessage(to,ms)
					
					elif text == "gid":
						random.choice(allbot).sendMessage(to,to)

					#elif text.startswith("add:ng:"):
					#	i = text[7:].split()
					#	if i not in data["nglist"]:
					#		data["nglist"].append(i)
					#	data_save()	
					#	random.choice(allbot).sendMessage(to,"nglistadd")

					elif text == "scheck":
						ms = ""	
						ms += f'{data["kick"][to]}:kick\n{data["inv"][to]}:inv\n{data["url"][to]}:url\n{data["cancel"][to]}:cancel\n{data["name"][to]}:name\n{data["pic"][to]}:pic\n{data["allm"][to]}:allm\n{data["joinms"][to]["send_TF"]}:joinms\n\n招待者：{cl.getContact(data["invadmin"][to])[22]}'
						random.choice(allbot).sendMessage(to,ms)

					elif text == "lcheck":
						gadminname = ""
						gwhitename = ""
						gblackname = ""
						sblistname = ""
						ms = ""
						
						if not data["lv0"][to]:
							gadminname += "-None\n"
						elif data["lv0"][to]:
							for m in data["lv0"][to]:
								gadminname += f"-{cl.getContact(m)[22]}\n"

						if not data["gblist"][to]:
							gblackname += "-None\n"
						elif data["gblist"][to]:
							for m in data["gblist"][to]:
								gblackname += f"-{cl.getContact(m)[22]}\n"

						if not data["gwlist"][to]:
							gwhitename += "-None\n"
						elif data["gwlist"][to]:
							for m in data["gwlist"][to]:
								gwhitename += f"-{cl.getContact(m)[22]}\n"	

						if not data["sblist"]:
							sblistname += "-None\n"
						elif data["sblist"]:
							for m in data["sblist"]:
								sblistname += f"-{cl.getContact(m)[22]}\n"		

						ms += f'個別権限\n{gadminname}\n個別ホワリス\n{gwhitename}\n個別ブラリス\n{gblackname}\n永久ブラリス\n{sblistname}\n招待者：{cl.getContact(data["invadmin"][to])[22]}'
						random.choice(allbot).sendMessage(to,ms)	

					elif text.startswith("set:on:"):
						cmd = text[7:].split()
						ms = ""
						c = 0
						new_setlist = setlist.copy()
						new_setlist.remove("joinms")
						for i in cmd:
							if i in new_setlist:
								if data[i][to] == False:
									data[i][to]=True
									ms += f"{i}：False >> True\n"
									c += 1
								elif data[i][to] == True:
									ms += f"{i}：already\n"
							elif i == "joinms":
								if data["joinms"][to]["send_TF"] == False:
									data["joinms"][to]={
										"send_TF":True,
										"message":data["joinms"][to]["message"]
									}
									ms += f"joinms：False >> True\n"
									c += 1
								elif data["joinms"][to]["send_TF"] == True:
									ms += f"joinms：already\n"
						data_save()
						random.choice(allbot).sendMessage(to,f"{ms}\ntotal：{str(c)}")

					elif text.startswith("set:off:"):
						cmd = text[8:].split()
						ms = ""
						c = 0
						new_setlist = setlist.copy()
						new_setlist.remove("joinms")
						for i in cmd:
							if i in new_setlist:
								if data[i][to] == True:
									data[i][to]=False
									ms += f"{i}：True >> False\n"
									c += 1
								elif data[i][to] == False:
									ms += f"{i}：already\n"
							elif i == "joinms":
								if data["joinms"][to]["send_TF"] == True:
									data["joinms"][to]={
										"send_TF":False,
										"message":data["joinms"][to]["message"]
									}
									ms += f"joinms：True >> False\n"
									c += 1
								elif data["joinms"][to]["send_TF"] == False:
									ms += f"joinms：already\n"
						data_save()
						random.choice(allbot).sendMessage(to,f"{ms}\ntotal：{str(c)}")

					
					elif text == "join":
						join(to)

					elif text.startswith("joinms:"):
						message = text[7:]
						if not message:
							data["joinms"][to]={
								"send_TF":data["joinms"][to]["send_TF"],
								"message":None
							}
							data_save()
							random.choice(allbot).sendMessage(to,f"join message remove")
						else:
							data["joinms"][to]={
								"send_TF":data["joinms"][to]["send_TF"],
								"message":message
							}
							data_save()
							random.choice(allbot).sendMessage(to,f"join message set\n\n{message}")

					elif text.startswith("un:"):
						unsend_num = text[3:]
						try:
							int(unsend_num)
						except:
							return random.choice(allbot).sendMessage(to,"Please specify an integer")
						try:
							if int(unsend_num) > 10:
								return random.choice(allbot).sendMessage(to,"Please specify less than 10")
						except:
							return random.choice(allbot).sendMessage(to,"Error")
						msg_ids = random.choice(allbot).getRecentMessagesV2(to,300)
						unsend_len = int(unsend_num)
						unsend_ids = {}
						for i_ids in msg_ids:
							for i_allbot in allbot:
								if i_allbot.mid in i_ids[1] and "UNSENT" not in i_ids[18]:
									unsend_ids[str(i_ids[4])]=i_allbot
									if len(unsend_ids) == unsend_len:
										break
									else:
										pass
								else:
									pass
							else:
								continue
							break
						for unsend_id in unsend_ids:
							try:
								time.sleep(0.8)
								unsend_ids[unsend_id].unsendMessage(unsend_id)
							except:
								unsend_ids[unsend_id].sendMessage(to,"Messages that are 24 hours old cannot be cancelled.")
								break

					elif text.startswith("add:gwlist") or text.startswith("add:lwhite"):
						try:
							metadata = msg[18]
							if 'MENTION' in metadata:
								key = eval(metadata["MENTION"])
								tags = key["MENTIONEES"]
								ms = "[add]\n"
								c = 0
								for tag in tags:
									mid = tag["M"]
									if mid not in data["gwlist"][to]:
										data["gwlist"][to].append(mid)
										ms += f"{mid[:5]} >> gwlist\n"
										c += 1
								data_save()
								random.choice(allbot).sendMessage(to,f"{ms}\ntotal：{str(c)}")
							else:
								random.choice(allbot).sendMessage(to, 'e')
						except:
							random.choice(allbot).sendMessage(to,"e")

					elif text.startswith("del:gwlist") or text.startswith("del:lwhite"):
						try:
							metadata = msg[18]
							if 'MENTION' in metadata:
								key = eval(metadata["MENTION"])
								tags = key["MENTIONEES"]
								ms = "[del]\n"
								c = 0
								for tag in tags:
									mid = tag["M"]
									if mid in data["gwlist"][to]:
										data["gwlist"][to].remove(mid)
										ms += f"{mid[:5]} >> gwlist\n"
										c += 1
								data_save()
								random.choice(allbot).sendMessage(to,f"{ms}\ntotal：{str(c)}")
							else:
								random.choice(allbot).sendMessage(to, 'e')
						except:
							random.choice(allbot).sendMessage(to,"e")

					elif text.startswith("add:gblist") or text.startswith("add:lblack"):
						try:
							metadata = msg[18]
							if 'MENTION' in metadata:
								key = eval(metadata["MENTION"])
								tags = key["MENTIONEES"]
								ms = "[add]\n"
								c = 0
								for tag in tags:
									mid = tag["M"]
									if mid not in data["gblist"][to]:
										data["gblist"][to].append(mid)
										ms += f"{mid[:5]} >> gblist\n"
										c += 1
								data_save()
								random.choice(allbot).sendMessage(to,f"{ms}\ntotal：{str(c)}")
							else:
								random.choice(allbot).sendMessage(to, 'e')
						except:
							data["lflag"][to]="gblistadd"
							data_save()
							random.choice(allbot).sendMessage(to,"[gblistadd]\n連絡先を送信してください")

					elif text.startswith("del:gblist") or text.startswith("del:lblack"):
						try:
							metadata = msg[18]
							if 'MENTION' in metadata:
								key = eval(metadata["MENTION"])
								tags = key["MENTIONEES"]
								ms = "[del]\n"
								c = 0
								for tag in tags:
									mid = tag["M"]
									if mid in data["gblist"][to]:
										data["gblist"][to].remove(mid)
										ms += f"{mid[:5]} >> gblist\n"
										c += 1
								data_save()
								random.choice(allbot).sendMessage(to,f"{ms}\ntotal：{str(c)}")
							else:
								random.choice(allbot).sendMessage(to, 'e')
						except:
							data["lflag"][to]="gblistdel"
							data_save()
							random.choice(allbot).sendMessage(to,"[gblistdel]\n連絡先を送信してください")

					elif text.startswith("del:autoblack"):
						cmd = text.split(":")
						try:
							autoblack_id = cmd[2]
							if autoblack.check(autoblack_id) is None:
								return random.choice(allbot).sendMessage(to,"Error")
							mid = autoblack.check(autoblack_id)["mid"]
							if autoblack.black_del(autoblack_id) == "success":
								random.choice(allbot).sendMessage(to,f"[del]\n{mid[:5]} >> autoblack")
						except:
							data["lflag"][to]="autoblackdel"
							data_save()
							random.choice(allbot).sendMessage(to,"[autoblackdel]\n連絡先を送信してください")

				if msg_from in data["dev"] or msg_from in data["invadmin"][to]: #開発者or招待者

					if text == "speed":
						start1 = time.time()
						asyncio_message(test_message_mid,".")
						end1 = time.time()
						send_time = end1 - start1
						start2 = time.time()
						asyncio.new_event_loop().run_in_executor(None, random.choice(allbot).getContact, "u3629e2dc9c1abb89d6defe27f779aa35")
						end2 = time.time()
						get_time = end2 - start2
						speed_results=f"sendMessage：{str(send_time)[:7]}\ngetContact：{str(get_time)[:7]}"
						random.choice(allbot).sendMessage(to,speed_results)

					elif text.startswith("invitee"):
						try:
							metadata = msg[18]
							if 'MENTION' in metadata:
								key = eval(metadata["MENTION"])
								tags = key["MENTIONEES"]
								for tag in tags:
									mid = tag["M"]
									data["invadmin"][to]=mid
									data_save()
									random.choice(allbot).sendMessage(to,f"{mid[:5]} >> invitee")
									break
						except:
							random.choice(allbot).sendMessage(to,"e")						

					elif text == "leave":
						random.choice(allbot).sendMessage(to,"bye")
						for i in allbot:
							i.deleteSelfFromChat(to)
						swsw.log(f"left\n\n{to}\n{msg_from}")
						asyncio.new_event_loop().run_in_executor(None, jl_log, to, msg_from)
					
					elif text.startswith("add:local"):
						try:
							metadata = msg[18]
							if 'MENTION' in metadata:
								key = eval(metadata["MENTION"])
								tags = key["MENTIONEES"]
								ms = "[add]\n"
								c = 0
								for tag in tags:
									mid = tag["M"]
									if mid not in data["lv0"][to]:
										data["lv0"][to].append(mid)
										ms += f"{mid[:5]} >> local\n"
										c += 1
								data_save()
								random.choice(allbot).sendMessage(to,f"{ms}\ntotal：{str(c)}")
							else:
								random.choice(allbot).sendMessage(to, 'e')
						except:
							random.choice(allbot).sendMessage(to,"e")

					elif text.startswith("del:local"):
						try:
							metadata = msg[18]
							if 'MENTION' in metadata:
								key = eval(metadata["MENTION"])
								tags = key["MENTIONEES"]
								ms = "[del]\n"
								c = 0
								for tag in tags:
									mid = tag["M"]
									if mid in data["lv0"][to]:
										data["lv0"][to].remove(mid)
										ms += f"{mid[:5]} >> local\n"
										c += 1
								data_save()
								random.choice(allbot).sendMessage(to,f"{ms}\ntotal：{str(c)}")
							else:
								random.choice(allbot).sendMessage(to, 'e')
						except:
							random.choice(allbot).sendMessage(to,"e")

					elif text == "call":
						c = 0
						for i in allbot:
							c += 1
							i.sendMessage(to,f"{c}：ok")

				if msg_from in data["dev"] or msg_from in data["lv1"] or msg_from in data["lv2"] or msg_from in data["lv3"] or msg_from in data["lv4"]:

					if text.startswith("add:black"):
						if msg_from not in list(data["blist"].keys()):
							data["blist"][msg_from]=[]
							data_save()
						try:
							metadata = msg[18]
							if 'MENTION' in metadata:
								key = eval(metadata["MENTION"])
								tags = key["MENTIONEES"]
								ms = "[add]\n"
								c = 0
								for tag in tags:
									mid = tag["M"]
									if mid not in data["blist"][msg_from]:
										data["blist"][msg_from].append(mid)
										ms += f"{mid[:5]} >> black\n"
										c += 1
								data_save()
								random.choice(allbot).sendMessage(to,f"{ms}\ntotal：{str(c)}")
						except:
							data["lflag"][to]="blackadd"
							data_save()
							random.choice(allbot).sendMessage(to,"[blackadd]\n連絡先を送信してください")

					elif text.startswith("del:black"):
						if msg_from not in list(data["blist"].keys()):
							data["blist"][msg_from]=[]
							data_save()
						try:
							metadata = msg[18]
							if 'MENTION' in metadata:
								key = eval(metadata["MENTION"])
								tags = key["MENTIONEES"]
								ms = "[del]\n"
								c = 0
								for tag in tags:
									mid = tag["M"]
									if mid in data["blist"][msg_from]:
										data["blist"][msg_from].remove(mid)
										ms += f"{mid[:5]} >> black\n"
										c += 1
								data_save()
								random.choice(allbot).sendMessage(to,f"{ms}\ntotal：{str(c)}")
						except:
							data["lflag"][to]="blackdel"
							data_save()
							random.choice(allbot).sendMessage(to,"[blackdel]\n連絡先を送信してください")

					elif text.startswith("add:white"):
						if msg_from not in list(data["wlist"].keys()):
							data["wlist"][msg_from]=[]
							data_save()
						try:
							metadata = msg[18]
							if 'MENTION' in metadata:
								key = eval(metadata["MENTION"])
								tags = key["MENTIONEES"]
								ms = "[add]\n"
								c = 0
								for tag in tags:
									mid = tag["M"]
									if mid not in data["wlist"][msg_from]:
										data["wlist"][msg_from].append(mid)
										ms += f"{mid[:5]} >> white\n"
										c += 1
								data_save()
								random.choice(allbot).sendMessage(to,f"{ms}\ntotal：{str(c)}")
						except:
							data["lflag"][to]="whiteadd"
							data_save()
							random.choice(allbot).sendMessage(to,"[whiteadd]\n連絡先を送信してください")

					elif text.startswith("del:white"):
						if msg_from not in list(data["wlist"].keys()):
							data["wlist"][msg_from]=[]
							data_save()
						try:
							metadata = msg[18]
							if 'MENTION' in metadata:
								key = eval(metadata["MENTION"])
								tags = key["MENTIONEES"]
								ms = "[del]\n"
								c = 0
								for tag in tags:
									mid = tag["M"]
									if mid in data["wlist"][msg_from]:
										data["wlist"][msg_from].remove(mid)
										ms += f"{mid[:5]} >> white\n"
										c += 1
								data_save()
								random.choice(allbot).sendMessage(to,f"{ms}\ntotal：{str(c)}")
							else:
								random.choice(allbot).sendMessage(to, 'e')
						except:
							data["lflag"][to]="whitedel"
							data_save()
							random.choice(allbot).sendMessage(to,"[whitedel]\n連絡先を送信してください")

				if msg_from in data["dev"] or msg_from in data["lv2"] or msg_from in data["lv3"] or msg_from in data["lv4"]:
					
					if text.startswith("add:user"):
						try:
							metadata = msg[18]
							if 'MENTION' in metadata:
								key = eval(metadata["MENTION"])
								tags = key["MENTIONEES"]
								ms = "[add]\n"
								c = 0
								for tag in tags:
									mid = tag["M"]
									if mid not in data["lv1"]:
										data["lv1"].append(mid)
										ms += f"{mid[:5]} >> user\n"
										c += 1
								data_save()
								random.choice(allbot).sendMessage(to,f"{ms}\ntotal：{str(c)}")
							else:
								random.choice(allbot).sendMessage(to, 'e')
						except:
							random.choice(allbot).sendMessage(to,"e")

					elif text.startswith("del:user"):
						try:
							metadata = msg[18]
							if 'MENTION' in metadata:
								key = eval(metadata["MENTION"])
								tags = key["MENTIONEES"]
								ms = "[del]\n"
								c = 0
								for tag in tags:
									mid = tag["M"]
									if mid in data["lv1"]:
										data["lv1"].remove(mid)
										ms += f"{mid[:5]} >> user\n"
										c += 1
								data_save()
								random.choice(allbot).sendMessage(to,f"{ms}\ntotal：{str(c)}")
							else:
								random.choice(allbot).sendMessage(to, 'e')
						except:
							random.choice(allbot).sendMessage(to,"e")

				if msg_from in data["dev"] or msg_from in data["lv3"] or msg_from in data["lv4"]:
					
					if text.startswith("add:lv2"):
						try:
							metadata = msg[18]
							if 'MENTION' in metadata:
								key = eval(metadata["MENTION"])
								tags = key["MENTIONEES"]
								ms = "[add]\n"
								c = 0
								for tag in tags:
									mid = tag["M"]
									if mid not in data["lv2"]:
										data["lv2"].append(mid)
										ms += f"{mid[:5]} >> lv2\n"
										c += 1
								data_save()
								random.choice(allbot).sendMessage(to,f"{ms}\ntotal：{str(c)}")
							else:
								random.choice(allbot).sendMessage(to, 'e')
						except:
							random.choice(allbot).sendMessage(to,"e")

					elif text.startswith("del:lv2"):
						try:
							metadata = msg[18]
							if 'MENTION' in metadata:
								key = eval(metadata["MENTION"])
								tags = key["MENTIONEES"]
								ms = "[del]\n"
								c = 0
								for tag in tags:
									mid = tag["M"]
									if mid in data["lv2"]:
										data["lv2"].remove(mid)
										ms += f"{mid[:5]} >> lv2\n"
										c += 1
								data_save()
								random.choice(allbot).sendMessage(to,f"{ms}\ntotal：{str(c)}")
							else:
								random.choice(allbot).sendMessage(to, 'e')
						except:
							random.choice(allbot).sendMessage(to,"e")

					elif text.startswith("add:lv3"):
						try:
							metadata = msg[18]
							if 'MENTION' in metadata:
								key = eval(metadata["MENTION"])
								tags = key["MENTIONEES"]
								ms = "[add]\n"
								c = 0
								for tag in tags:
									mid = tag["M"]
									if mid not in data["lv3"]:
										data["lv3"].append(mid)
										ms += f"{mid[:5]} >> lv3\n"
										c += 1
								data_save()
								random.choice(allbot).sendMessage(to,f"{ms}\ntotal：{str(c)}")
							else:
								random.choice(allbot).sendMessage(to, 'e')
						except:
							random.choice(allbot).sendMessage(to,"e")

					elif text.startswith("del:lv3"):
						try:
							metadata = msg[18]
							if 'MENTION' in metadata:
								key = eval(metadata["MENTION"])
								tags = key["MENTIONEES"]
								ms = "[del]\n"
								c = 0
								for tag in tags:
									mid = tag["M"]
									if mid in data["lv3"]:
										data["lv3"].remove(mid)
										ms += f"{mid[:5]} >> lv3\n"
										c += 1
								data_save()
								random.choice(allbot).sendMessage(to,f"{ms}\ntotal：{str(c)}")
							else:
								random.choice(allbot).sendMessage(to, 'e')
						except:
							random.choice(allbot).sendMessage(to,"e")

				if msg_from in data["dev"]: #開発者
					
					if text == "0x01000001000101001011110101001":
						pass

					elif text.startswith("exec:"):
						cmd = text[5:]
						try:
							exec(cmd)
						except Exception as e:
							random.choice(allbot).sendMessage(to,e)

					elif text.startswith("checkrate"):
						try:
							metadata = msg[18]
							if 'MENTION' in metadata:
								key = eval(metadata["MENTION"])
								tags = key["MENTIONEES"]
								for tag in tags:
									mid = tag["M"]
									random.choice(allbot).sendMessage(to,f"<{random.choice(allbot).getContact(mid)[22]}>\nrate >> {str(rate.check_rate(mid))}")
						except Exception as e:
							print(e)

					elif text.startswith("rate:"):
						cmd = text.split(":")
						try:
							metadata = msg[18]
							if 'MENTION' not in metadata:
								return
						except:
							pass
						try:
							metadata = msg[18]
							if 'MENTION' in metadata:
								key = eval(metadata["MENTION"])
								tags = key["MENTIONEES"]
								for tag in tags:
									mid = tag["M"]
									if "@" in cmd[3]:
										num = int(cmd[1])
										c_type = cmd[2]
										change_rate_data = rate.change_rate(num,c_type,mid)
									else:
										if cmd[3] in ["botkick","adminkick","memberkick","minvite","finvite","cancel","name","icon","url","allm","others"]:
											num = int(cmd[1])
											c_type = cmd[2]
											r_type = cmd[3]
											change_rate_data = rate.change_rate(num,c_type,mid,r_type)
									random.choice(allbot).sendMessage(to,f"""<{random.choice(allbot).getContact(mid)[22]}>\n{str(change_rate_data["old_rate"])} >> {str(change_rate_data["new_rate"])}""")
						except Exception as e:
							print(f"hogo:{e}")

					elif text == "data_view":
						random.choice(allbot).sendMessage(to,str(wait_data))

					elif text.startswith("add:autoblack"):
						try:
							metadata = msg[18]
							if 'MENTION' in metadata:
								key = eval(metadata["MENTION"])
								tags = key["MENTIONEES"]
								ms = ""
								c = 0
								temp_kick_list = []
								for tag in tags:
									mid = tag["M"]
									if not autoblack.black_check(to,mid):
										tempp = autoblack.put(to,mid)
										ms += f"""{mid[:5]} >> autoblack\n>time：{str(tempp["time"])}\n>id：{str(tempp["ab_id"])}\n"""
										c += 1
										temp_kick_list.append(mid)
								data_save()
								random.choice(allbot).sendMessage(to,f"{ms}\ntotal：{str(c)}")
								for kick_mid in temp_kick_list:
									random.choice(allbot).deleteOtherFromChat(to,kick_mid)
							else:
								random.choice(allbot).sendMessage(to, 'e')
						except:
							pass

					elif text.startswith("getop:"):
						cmd = text[6:]
						num = int(cmd)
						get_op_list = random.choice(allbot).getRecentMessagesV2(to,300)
						random.choice(allbot).sendMessage(to,get_op_list[num])

					elif text == "comp_data":
						ms = "データ補完\n"
						all_gid = cl.getAllChatMids()[1]
						for i in all_gid:
							pass

					elif text == "rename:":
						spl = text[8:]
						if len(text) == 8:
							for i in allbot:
								i.updateProfileAttribute(2,spl)
								i.sendMessage(to,"ok")
						else:
							for i in allbot:
								randlst = [random.choice(string.ascii_letters + string.digits) for p in range(13)]
								rn = str(''.join(randlst))
								i.updateProfileAttribute(2,rn)
								i.sendMessage(to,"ok")

					elif text.startswith("repic:"): #repic: file_Path
						key = text[6:]
						for i in allbot:
							i.updateProfileImage(key)
							i.sendMessage(to,"ok")

					elif text.startswith("add:dev"):
						try:
							metadata = msg[18]
							if 'MENTION' in metadata:
								key = eval(metadata["MENTION"])
								tags = key["MENTIONEES"]
								ms = "[add]\n"
								c = 0
								for tag in tags:
									mid = tag["M"]
									if mid not in data["dev"]:
										data["dev"].append(mid)
										ms += f"{mid[:5]} >> dev\n"
										c += 1
								data_save()
								random.choice(allbot).sendMessage(to,f"{ms}\ntotal：{str(c)}")
							else:
								random.choice(allbot).sendMessage(to, 'e')
						except:
							random.choice(allbot).sendMessage(to,"e")

					elif text.startswith("del:dev"):
						try:
							metadata = msg[18]
							if 'MENTION' in metadata:
								key = eval(metadata["MENTION"])
								tags = key["MENTIONEES"]
								ms = "[del]\n"
								c = 0
								for tag in tags:
									mid = tag["M"]
									if mid in data["dev"]:
										data["dev"].remove(mid)
										ms += f"{mid[:5]} >> dev\n"
										c += 1
								data_save()
								random.choice(allbot).sendMessage(to,f"{ms}\ntotal：{str(c)}")
							else:
								random.choice(allbot).sendMessage(to, 'e')
						except:
							random.choice(allbot).sendMessage(to,"e")

					elif text.startswith("mk"):
						try:
							metadata = msg[18]
							if 'MENTION' in metadata:
								key = eval(metadata["MENTION"])
								tags = key["MENTIONEES"]
								kick_list = []
								for tag in tags:
									kick_list.append(tag["M"])
								kick_amount = len(kick_list)
								start = time.time()
								for kick_mid in kick_list:
									asyncio.new_event_loop().run_in_executor(None, random.choice(allbot).deleteOtherFromChat, to, kick_mid)
								end = time.time()
								kick_time = end - start
								time.sleep(1)
								kick_message = f"[Kick complete]\n\nkick amount：{str(kick_amount)}\nkick time {str(kick_time)[:7]}"
								random.choice(allbot).sendMessage(to,kick_message)	
						except:
							pass

					elif text == "noop":
						for i in allbot:
							try:
								i.noop()
							except:
								random.choice(allbot).sendMessage(to,f"{i.mid[:5]} >> error")	
						random.choice(allbot).sendMessage(to,"fin")	

		elif msg[15] == 13:
			if msg[3] == 2:
				if msg_from in allmid:
					return
				if wait.check(f"contact:{msg_from}") is None:
					wait.wait(3,f"contact:{msg_from}")
					mid=msg[18]['mid']
					name=msg[18]['displayName']
					ms = ""
					ms += f"<{name}>"
					if mid in data["dev"]:
						ms += f"\n-開発者権限"
					if mid in data["invadmin"][to]:
						ms += f"\n-招待者権限"
					try:		
						if mid in data["lv0"][to]:
							ms += f"\n-local"
					except:
						pass
					try:
						if mid in data["gblist"][to]:
							ms += f"\n-グル別ブラリス"
					except:
						pass
					try:
						if mid in data["gwlist"][to]:
							ms += f"\n-グル別ホワリス"
					except:
						pass
					if mid in data["lv1"]:
						ms += f"\n-user"
					if mid in data["lv2"]:
						ms += f"\n-lv2"
					if mid in data["lv3"]:
						ms += f"\n-lv3"
					if mid in data["lv4"]:
						ms += f"\n-lv4"
					if ms != f"<{name}>":
						random.choice(allbot).sendMessage(to,ms)
					else:
						random.choice(allbot).sendMessage(to,f"<{name}>\nnull")
					try:
						mid=msg[18]['mid']
						name=msg[18]['displayName']
						if autoblack.black_check(to,mid):
							num = str(autoblack.time_check(to,mid))
							random.choice(allbot).sendMessage(to,f"<{name}>\n-autoblack\n>>{num}秒後に解除されます")
					except Exception as e:
						print(e)

				if msg_from in data["dev"] or msg_from in data["lv1"] or msg_from in data["lv2"] or msg_from in data["lv3"] or msg_from in data["lv4"]:
					mid=msg[18]['mid']
					if data["lflag"][to] != False:
						if data["lflag"][to] == "blackadd":
							if mid not in data["blist"][msg_from]:
								data["blist"][msg_from].append(mid)
								data_save()
								data["lflag"][to]=False
								data_save()
								random.choice(allbot).sendMessage(to,f"[add]\n{mid[:5]} >> black")
							else:
								random.choice(allbot).sendMessage(to,"Error")

						elif data["lflag"][to] == "blackdel":
							if mid in data["blist"][msg_from]:
								data["blist"][msg_from].remove(mid)
								data_save()
								data["lflag"][to]=False
								data_save()
								random.choice(allbot).sendMessage(to,f"[del]\n{mid[:5]} >> black")
							else:
								random.choice(allbot).sendMessage(to,"Error")

						elif data["lflag"][to] == "whiteadd":
							if mid not in data["wlist"][msg_from]:
								data["wlist"][msg_from].append(mid)
								data_save()
								data["lflag"][to]=False
								data_save()
								random.choice(allbot).sendMessage(to,f"[add]\n{mid[:5]} >> white")
							else:
								random.choice(allbot).sendMessage(to,"Error")

						elif data["lflag"][to] == "whitedel":
							if mid in data["wlist"][msg_from]:
								data["wlist"][msg_from].remove(mid)
								data_save()
								data["lflag"][to]=False
								data_save()
								random.choice(allbot).sendMessage(to,f"[del]\n{mid[:5]} >> white")
							else:
								random.choice(allbot).sendMessage(to,"Error")

						elif data["lflag"][to] == "gblistadd":
							if mid not in data["gblist"][to]:
								data["gblist"][to].append(mid)
								data_save()
								data["lflag"][to]=False
								data_save()
								random.choice(allbot).sendMessage(to,f"[add]\n{mid[:5]} >> gblist")
							else:
								random.choice(allbot).sendMessage(to,"Error")		

						elif data["lflag"][to] == "gblistdel":
							if mid in data["gblist"][to]:
								data["gblist"][to].remove(mid)
								data_save()
								data["lflag"][to]=False
								data_save()
								random.choice(allbot).sendMessage(to,f"[del]\n{mid[:5]} >> gblist")
							else:
								random.choice(allbot).sendMessage(to,"Error")

						elif data["lflag"][to] == "autoblackdel":
							if autoblack.black_check(to,mid):
								try:
									autoblack.black_del_uid(to,mid)
									data["lflag"][to]=False
									data_save()
									random.choice(allbot).sendMessage(to,f"[del]\n{mid[:5]} >> autoblack")
								except:
									random.choice(allbot).sendMessage(to,"Error")
							else:
								random.choice(allbot).sendMessage(to,"Error")

		if msg[15] == 13:  # user infomation
			if msg[3] == 2:  # for chat room
				pass

		if msg[15] == 18:  # del Album or photo or inv_someone or cancel_someone
			pass

"""threading"""
threading.Thread(target=recovery_rate_a).start()
"""fetchOps"""
cl.trace(bot)