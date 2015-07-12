import json, os, re, urllib

# TODO use wall_post_count and dynamic offset eval
# curl 'https://api.vk.com/method/wall.get?owner_id=-18312682&count=100&offset=100' > newbeat2.json

wall_get_url = 'https://api.vk.com/method/wall.get?owner_id=-18312682'


def wall_get_post_count():
	data = urllib.urlopen(wall_get_url + '&count=1').read()
	return json.loads(data)['response'][0]


def simplify(attach):
	return {
		'url': 		re.sub("\?.*$", "", attach['audio']['url']),
		'performer':	re.sub("&gt;", ")", re.sub("&lt;", "(", attach['audio']['performer'])),
		'title':	re.sub("&gt;", ")", re.sub("&lt;", "(", attach['audio']['title'])),
	}


def download(track):
	print "Download: " + track['performer'] + " - " + track['title']
	filename = track['performer'] + " - " + track['title'] + ".mp3"
	filename = "download/" + re.sub("/", "_", filename)
	print 'url: ' + track['url'] + ' to ' + filename
	if os.path.isfile(filename):
		print ".. skipping"
		return
	if not track['url']:
		print 'no url'
		return
	urllib.urlretrieve(track['url'], filename)


def file2response(file):
	with open(file) as f:
		data = json.loads(f.read())
	data['response'].remove(data['response'][0])
	return data['response']


def download_all_response(response):
	for post in response:
		if not 'attachments' in post:
			continue
		for attach in post['attachments']:
			if attach['type'] == 'audio':
				download(simplify(attach))

def main():
	wall_post_count = wall_get_post_count()
	offset = 0
	for file in [ 'newbeat.json', 'newbeat2.json', 'newbeat3.json' ]:
		response = file2response(file)
		download_all_response(response)
		
main()
