import time, os, concurrent, asyncio, random, json, requests, datetime, copy, string, base64, concurrent, timeit, re

notify_gid = ""

class Kurosawa:
	def __init__(self, cl, all_account, all_account_mid, kicker_account, kicker_account_mid, notify_id=notify_gid):
		self.cl = cl
		self.all_account = all_account
		self.all_account_mid = all_account_mid
		self.kicker_account = kicker_account
		self.kicker_account_mid = kicker_account_mid
		self.notify_id = notify_id

	def log(self,message):
		cl = random.choice(self.all_account)
		asyncio.new_event_loop().run_in_executor(None, cl.sendMessage, self.notify_id, message)