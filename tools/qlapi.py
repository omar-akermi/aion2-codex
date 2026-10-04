import json, urllib.request, urllib.parse

BASE = 'https://questlog.gg/aion-2/api/trpc/'


def get(proc, inp):
    url = BASE + proc + '?input=' + urllib.parse.quote(json.dumps(inp, separators=(',', ':')))
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://questlog.gg/aion-2/en'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())['result']['data']


if __name__ == '__main__':
    lb = get('armory.getLeaderboard', {'region': 'tw', 'type': 'nightmare', 'classId': 'templar', 'page': 1})
    print(list(lb.keys()), len(lb['pageData']), json.dumps(lb['pageData'][0])[:300])
    cid = lb['pageData'][0]['characterId']
    for inp in [{'region': 'tw', 'characterId': cid}, {'characterId': cid, 'region': 'tw', 'language': 'en'}]:
        try:
            c = get('armory.getCharacter', inp); print('OK', list(c.keys())); break
        except Exception as e:
            print('ERR', inp, e)
