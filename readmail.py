# -*- coding: utf-8 -*-
"""
@author: TsingJyujing
"""

import email
import re

class eml():
	def loadfile(self,file_name):
		try:
			fp = open(file_name,'r');
			self.msg = email.message_from_file(fp);
			fp.close();
			return True
		except:
			return False
			
	def getinfo(self,key):
		try:
			return self.msg.get(key)
		except:
			return ""
			
	def getfrom(self):
		str = self.getinfo("from")
		if str==None:
			return []
		user = re.findall("<.*?>",str,re.DOTALL)
		if len(user)<=0:
			return []
		else:
			return [user[0][1:-1]]
			
	def getto(self):
		str = self.getinfo("to")
		if str==None:
			return []
		users = re.findall("<.*?>",str,re.DOTALL)
		if len(users)<=0:
			return []
		else:
			rtnval = [];
			for user in users:
				rtnval.append(user[1:-1])
			return rtnval
				
if __name__=="__main__":
	fn = 'dnc_mails/3.eml';
	msg = eml();
	print msg.loadfile(fn)
	print msg.getfrom()
	print msg.getto()
	
