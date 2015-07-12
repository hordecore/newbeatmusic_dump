import json, os, re, urllib

wall_get_url = 'https://api.vk.com/method/wall.get?owner_id=-18312682'

if not os.path.isfile('newbeat.json'):
    print "TODO: dynamic offset eval, but now:"
    print "curl 'https://api.vk.com/method/wall.get?owner_id=-18312682&count=100&offset=0' > newbeat.json"
    print "curl 'https://api.vk.com/method/wall.get?owner_id=-18312682&count=100&offset=100' > newbeat2.json"
    print "curl 'https://api.vk.com/method/wall.get?owner_id=-18312682&count=100&offset=200' > newbeat3.json"
    return

if not os.path.isdir('download'):
    os.mkdir('download')
    
for file in [ 'newbeat.json', 'newbeat2.json', 'newbeat3.json' ]:
    with open(file) as f:
        data = json.loads(f.read())

    if not 'response' in data:
        print 'no response in data of ' + file + ':'
        print data
        exit(1)

    data['response'].remove(data['response'][0])

    for post in data['response']:
        if not 'attachments' in post:
            continue
        for attach in post['attachments']:
            if attach['type'] == 'audio':
                track = {
                    'url':          re.sub("\?.*$", "", attach['audio']['url']),
                    'performer':    re.sub("&gt;", ")", re.sub("&lt;", "(", attach['audio']['performer'])),
                    'title':        re.sub("&gt;", ")", re.sub("&lt;", "(", attach['audio']['title'])),
                }
                filename = track['performer'] + " - " + track['title'] + ".mp3"
                filename = "download/" + re.sub("/", "_", filename)
                print filename.replace("/", ": ")
                if os.path.isfile(filename):
                    print "... already here, skip"
                    continue
                if not track['url']:
                    print '... no url, skip'
                    continue
                urllib.urlretrieve(track['url'], filename)
