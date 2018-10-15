#!/usr/bin/python3

# Aswf - Web fuzzer
# 100% tiny, 100% effective

from argparse import ArgumentParser
import urllib.request
import re
import random

# Défaut user-agent
default_ua = "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"

# Directories to test
dirs = [
	"phpmyadmin","pma","tmp","temp","sql","backup",
	"bak","www","db","save","test","tests","dev",
	"includes","include","inc","admin","administrateur",
	"administrator","adm","secret","private","cache",
	"config","configuration","conf","install",
	"installation",".git",".svn","gestion","php",
	"cgi-bin","cgi-sys","old", "secure","mysql",
	"xml","api", "files","upload","file","uploads",
	"upload","download","downloads","wp-content",
	"wp-upload","default""site","sites","log","logs",
	"stats","stat","status"
]

# Files to test
files = [
	"index.php~","index.php.bak","index.php.old",
	"index.old","test.php","dev.php","phpinfo.php",
	"phpinfos.php","oldindex.php","db.sqlite","db.sqlite3",
	"api.php",".htaccess",".htpasswd","security.txt"
]

# Files which content will be displayed
files_content = [
	"robots.txt"
]

# Domains to test
domains = [
	"mail",
	"dev",
	"test",
	"beta"
]

def get_base_url(url):
        p = re.compile('http(s?)://(www\.)?')
        return p.sub('', url)

def make_domaine_url(_url, _itm):
	ret_url = _url.split(":")[0] + '://' +  _itm 
	ret_url += '.' + get_base_url(_url) + '/'
	return ret_url

# Arguments management
parser = ArgumentParser()
parser.add_argument(
	"-u","--url",type=str,dest="url",
	help="Use -u or --url to define the target URL."
		   )
parser.add_argument(
	"-a","--user-agent",type=str,dest="ua",
	help="Use -a or --user-agent to define an optionnal user-agent.",
	default=default_ua
)

parser.add_argument(
	"-t","--temporisation",type=int,dest="tempo",
	help="Use -t val or --temporisation val to wait val ms between requests.",
	default=0
)

args = parser.parse_args()

if( not args.url):
	print("Use -u your.url.pliz")
	exit(1)

_url = args.url

if(_url[-1] == "/"):
	_url = _url[:-1]


scan_routine = [ 
	["directories", dirs + 
	[ "v" + str(i) for i in range(1,5)]
		+ list(range(2010,2019))
		+ [ "v" + str(i) for i in range(2010,2019)]
		, False],
	["files", files, False,],
	["readables files",files_content,False] ,
	["domains", domains, True]
]
i = 1

# Start scan
for r in scan_routine:
	print("Scanning " + r[0])
	for item in r[1]:
		res = None
		_itm = str(item)
		_method = 'HEAD'

		# url like http://the.url/dir/		 
		if (r[0][0:11]=="directories"):
			url = _url + '/' + _itm + '/'
			#_method='GET'

		#url like http(s?)://item.the.url
		elif (r[0][0:8]=="domains"):
			url = make_domaine_url(_url, _itm)
			#_method='GET'

		else:
			url = _url + '/' + _itm

		req = urllib.request.Request(url=url, method=_method)
		req.add_header("User-Agent", args.ua)
		code = -1

		try:
			res = urllib.request.urlopen(req)
			code = res.getcode()
		except urllib.error.HTTPError as e:
			code = e.getcode()
		

		if(code != 404):
			print(code, "\t", url)
			#print(i,"/",50, end="")
			if(r[0] == "readables files"):
				print(res.read().decode("utf-8"))
		i += 1
