import login
import json

from collections import deque

def main():
    w, c = login.doInteractiveLogin()
    conf = c._config['location_explorer']

    max_place_count = conf['max_place_count']
    output_filename = conf['output_filename']
    origin = conf['origin']

    places = {}
    queue = deque([{ 'id': origin }])
    processed = {origin}

    while queue and len(places) < max_place_count:
        nx = queue.popleft()
        pid = nx['id']
        places[pid] = w.getPlaceById(pid)
        for p in places[pid].nearby:
            if p['id'] in processed: continue
            processed.add(p['id'])
            queue.append({ 'id': p['id'], 'name': p['name'] })

    processed = []
    unprocessed = []
    for p in places.items():
        processed.append({
            'id': p[1].id,
            'name': p[1].name,
            'lat': p[1].latitude,
            'lng': p[1].longitude
        })
    while queue:
        nx = queue.popleft()
        unprocessed.append({
            'id': nx['id'],
            'name': nx['name']
        })

    with open(output_filename, 'w') as f:
        f.write(json.dumps({
            'proc': processed,
            'queue': unprocessed
        }, indent=4))

if __name__ == '__main__':
    main()
