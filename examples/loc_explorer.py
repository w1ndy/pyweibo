import login
import json
import heapq

from geopy.distance import great_circle as dist

def writeOut(fname, num, data, queue=None):
    print('writing out archive %s...' % fname.format(n=num))
    processed = []
    unprocessed = []
    for p in data:
        processed.append({
            'id': p.id,
            'name': p.name,
            'lat': p.latitude,
            'lng': p.longitude,
            'r': p.radius,
            'wc': p.weibo_count
        })
    if queue:
        for nx in queue:
            unprocessed.append({ 'id': nx[0], 'name': nx[1] })
    with open(fname.format(n=num), 'w') as f:
        f.write(json.dumps({ \
            'proc': processed, \
            'queue': unprocessed \
        }, indent=4))

def main():
    w, c = login.doInteractiveLogin()
    conf = c._config['location_explorer']

    if 'max_place_count' in conf:
        max_place_count = conf['max_place_count']
    else:
        max_place_count = -1
    if 'search_center' in conf:
        search_cond = True
        search_center = conf['search_center']
        search_radius = conf['search_radius']
    else:
        search_cond = False
    if 'archive_size' in conf:
        archive_size = conf['archive_size']
    else:
        archive_size = None
    output_filename = conf['output_filename']
    origin = conf['origin']

    archive_count = 0
    location_count = 0
    places = []
    queue = [(0, (origin, ''))]
    processed = {origin}

    while queue and (max_place_count == -1 or len(places) < max_place_count):
        nx = heapq.heappop(queue)[1]
        pid = nx[0]
        location_count += 1
        print('processing %d location %s...' % (location_count, pid))
        loc = w.getPlaceById(pid)
        if search_cond and \
            dist(tuple(search_center), (loc.latitude, loc.longitude)).meters > \
                search_radius:
            continue
        places.append(loc)
        if archive_size and len(places) >= archive_size:
            writeOut(output_filename, archive_count, places)
            places = []
            archive_count += 1
        for p in loc.queryNearby():
            if p['id'] in processed: continue
            processed.add(p['id'])
            heapq.heappush(queue, ( \
                -p['weibo_count'], \
                ( p['id'], p['name'] ) \
            ))

    writeOut(output_filename, archive_count, places, queue)
    print('total %d locations found' % location_count)

if __name__ == '__main__':
    main()
