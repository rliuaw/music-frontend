# -*- coding: utf-8 -*-

import os
import errno
import json
import sys
import datetime
from _aws_list_s3_objects import to_s3_url

# Expects songs to be stored as .../<keyword>/<name>
# keywords: daw1, daw2, rec1, rec2, rec3
def path_hierarchy(path):
    path_save = '/' + path.split('\\', 4)[4].replace('\\', '/')
    names = path.split('\\')
    hierarchy = {
        'name': names[len(names) - 1],
        'path': path_save,
        'character': names[len(names) - 2],
        'keyword': names[len(names) - 2],
    }
    try:
        hierarchy['songs'] = [
            path_hierarchy(os.path.join(path, contents))
            for contents in os.listdir(path)
        ]
        del hierarchy['character']
        del hierarchy['keyword']
    except OSError as e:
        if e.errno != errno.ENOTDIR:
            raise
    return hierarchy


def path_to_dict(path):
    d = {'name': os.path.basename(path)}
    names = path.split('/')
    if os.path.isdir(path):
        d['type'] = "directory"
        d['children'] = [path_to_dict(os.path.join(path, x)) for x in os.listdir(path)]
    else:
        d['type'] = "file"
        d['title'] = os.path.splitext(d['name'])[0]
        d['file'] = '/' + '/'.join(names[-3:])
        # d['file'] = to_s3_url(file=names[-1], prefix='/'.join(names[-3:-1]))
        d['howl'] = None
        d['created'] = os.path.getctime(path)
    return d


def dir_as_songlist(d):
    res = list()
    assert d['type'] == "directory", f"{d['type']} is not a directory"
    t = dict()
    t['title'] = d['name']
    t['code'] = d['name']
    t['file'] = None
    res.append(t)
    for c in d['children']:
    # for c in d['children'][:5]:
        res.append(c)
    return res


def dir_dir_as_songlist(d):
    res = list()
    assert d['type'] == "directory", f"{d['type']} is not a directory"
    for c in d['children']:
        res += dir_as_songlist(c)
    return res


if __name__ == '__main__':
    try:
        directory = sys.argv[1]
    except IndexError:
        # directory = "D:\\Download\\Touhou\\th-music-video-generator\\audio\\temp"
        directory = "/Users/richard.liu/extra/music/audio"

    # print(json.dumps(path_hierarchy(directory), indent=2, sort_keys=True, ensure_ascii=False))
    path = "/Users/richard.liu/extra/music/audio/daw1piano/Coalescent 90.wav"
    # import pdb; pdb.set_trace()
    # d = path_to_dict(path)
    d = path_to_dict(directory)
    d = dir_dir_as_songlist(d)
    d = json.dumps(d, indent=2, sort_keys=True)
    with open("database/music.json", "w") as f:
        f.write(d)
# {
#     "title": "東方靈異伝",
#     "file": null,
#     "code": "th01"
# }