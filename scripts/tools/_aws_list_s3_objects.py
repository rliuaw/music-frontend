from urllib.parse import quote_plus
import os
import subprocess

def to_s3_url(file, prefix="", bucket_name="2022assets"):
    key = file
    key = quote_plus(key, safe="~()*!.'")
    object_url = f'''https://{bucket_name}.s3.amazonaws.com/music/{prefix}/{key}'''
    return object_url


def compress(path):
    size = os.path.getsize(path)
    new_path = os.path.splitext(path)[0] + ".mp3"
    payload = f'''ffmpeg -y -i "{path}" -af loudnorm -vn -ar 44100 -ac 2 -b:a 192k "{new_path}"'''
    subprocess.run(payload, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    try:
        new_size = os.path.getsize(new_path)
    except FileNotFoundError:
        return False, f"{new_path} not found"

    print(path)
    print(f"orig {size} new {new_size} = {(size - new_size)/size:.2%} redux")
    if not path.endswith(".mp3"): # mp3 input is overwritten anyways
        payload = f'''rm "{path}"'''
        subprocess.run(payload, shell=True)
    return True, new_path


def assign_ctime(file):
    d = dict()
    def format_ts(ts):
        mm, dd, yyyy = tuple(ts.split("/"))
        return f"{yyyy}{mm}{dd}0000.00" # Format: YYYYMMDDhhmm.SS

    with open(file, "r") as f:
        t = f.read()
        t = t.splitlines()
        t = [k.split(',') for k in t]
        for ts, path in t:
            d[path] = format_ts(ts)

    dir = os.path.dirname(file)
    for name in os.listdir(dir):
        if name == "rec2memos.csv":
            continue

        path = os.path.join(dir, name)
        assert name in d, f"{name} in d"

        current_time = d[name]
        subprocess.run(['touch', '-t', current_time, path])


# file = "/Users/richard.liu/extra/music-frontend/audio/rec2memos/rec2memos.csv"
# assign_ctime(file)


# directory = "/Users/richard.liu/extra/music-frontend/audio"
# file = directory + "/daw1snippet/discovery 150.wav"

# compress(file)