import json
import os
import re
import urllib

# TODO use wall_post_count and dynamic offset eval
# curl 'https://api.vk.com/method/wall.get?owner_id=-18312682&count=100&offset=100' > newbeat2.json

wall_get_url = 'https://api.vk.com/method/wall.get?owner_id=-18312682'


def wall_get_post_count():
	data = urllib.urlopen(wall_get_url + '&count=1').read()
	return json.loads(data)['response'][0]


def simplify(j):
	return {
		'url': 		re.sub("\?.*$", "", j['audio']['url']),
		'performer':	re.sub("&gt;", ")", re.sub("&lt;", "(", j['audio']['performer'])),
		'title':	re.sub("&gt;", ")", re.sub("&lt;", "(", j['audio']['title'])),
	}


def download(z):
	print "Download: " + z['performer'] + " - " + z['title']
	filename = z['performer'] + " - " + z['title'] + ".mp3"
	filename = "download/" + re.sub("/", "_", filename)
	print 'url: ' + z['url'] + ' to ' + filename
	if os.path.isfile(filename):
		print ".. skipping"
		return
	if not z['url']:
		print 'no url'
		return
	urllib.urlretrieve(z['url'], filename)


def file2response(file):
	with open(file) as f:
		x = json.loads(f.read())

	x['response'].remove(x['response'][0])
	return x['response']


def download_all_response(response):
	y = []
	for i in response:
		if 'attachments' in i:
			for j in i['attachments']:
				if j['type'] == 'audio':
					download(simplify(j))

def main():
	wall_post_count = wall_get_post_count()
	offset = 0
	for file in [ 'newbeat.json', 'newbeat2.json', 'newbeat3.json' ]:
		response = file2response(file)
		download_all_response(response)
		
main()
