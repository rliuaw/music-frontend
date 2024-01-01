# -*- coding: utf-8 -*-

import os
import errno
import json
import sys
import datetime
from _load_metadata_csv import get_checker
from _aws_list_s3_objects import to_s3_url, compress


metadata = dict()
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
        listdir = os.listdir(path)
        dd = [path_to_dict(os.path.join(path, x)) for x in listdir]
        d['children'] = [x for x in dd if x is not None]
    else:
        if path.endswith(".csv"):
            # print(f"loading {path}")
            load_csv(path)
            return None
        elif path.endswith(".mp3"):
            # print(f"mp3: {path}")
            pass
        else:
            print(f"skipping {path}")
            return None
            # ok, new_path = compress(path)
            # if not ok:
            #     assert False, new_path
            # path = new_path
        d['type'] = "file"
        d['title'] = os.path.splitext(d['name'])[0]
        d['file'] = '/' + '/'.join(names[-3:])
        d['file'] = to_s3_url(file=names[-1], prefix='/'.join(names[-3:-1]))
        d['howl'] = None
        # print(path)
        d['created'] = os.stat(path).st_birthtime
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
        res.append(c)
    return res


def dir_dir_as_songlist(d):
    res = list()
    assert d['type'] == "directory", f"{d['type']} is not a directory"
    for c in d['children']:
        res += dir_as_songlist(c)
    return res


def backfill_metadata(d):
    for c in d['children']:
        mk = c['name']
        assert mk in metadata, f"{mk}"
        for g in c['children']:
            gk = g['name']
            if gk not in metadata[mk]:
                matches = [k for k in metadata[mk].keys() if k.startswith(gk.split(".mp3")[0])]
                assert len(matches) >= 1, f"{gk} {matches}"
                gk = min(matches, key=len)
            assert gk in metadata[mk], f"{mk} {gk}"
            g['created'] = metadata[mk][gk]
    return d


def load_csv(path):
    checker = None
    d = dict()
    with open(path, 'r') as f:
        m = f.read()
        m = m.split('\n')
        for k in m:
            if len(k) == 0:
                continue
            if checker is None:
                checker = get_checker(k)
                if checker is None:
                    if k == '"Name","CreationTime"':
                        continue
                    print(f"no checker for {k}, skipping")
                    continue
            assert checker.check_date_format(k), f"{path} {k} {checker.format} {checker.dateIx}"
            name, created = checker.convert(k)
            d[name] = created
    path = path.split('/')[-1].split('.')[0]
    global metadata
    metadata[path] = d


if __name__ == '__main__':
    try:
        directory = sys.argv[1]
    except IndexError:
        # directory = "D:\\Download\\Touhou\\th-music-video-generator\\audio\\temp"
        directory = "/Users/richard.liu/extra/music-frontend/audio"

    # print(json.dumps(path_hierarchy(directory), indent=2, sort_keys=True, ensure_ascii=False))
    # path = "/Users/richard.liu/extra/music/audio/daw1piano/Coalescent 90.wav"
    # import pdb; pdb.set_trace()
    # d = path_to_dict(path)
    d = path_to_dict(directory)
    d = backfill_metadata(d)
    d = dir_dir_as_songlist(d)
    d = json.dumps(d, indent=2, sort_keys=True)
    with open("database/music.json", "w") as f:
        f.write(d)
# {
#     "title": "東方靈異伝",
#     "file": null,
#     "code": "th01"
# }