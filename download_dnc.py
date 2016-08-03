from pyinternet import download_image

if __name__=="__main__":
	start_n = input("input start num:")
	process_n = input("input count num:")
	for i in xrange(process_n):
		imgurl = "https://wikileaks.org/dnc-emails//get/%d" % (i+start_n)
		fpname = "dnc_mails/%d.eml" % (i+start_n)
		download_image(imgurl,fpname)
