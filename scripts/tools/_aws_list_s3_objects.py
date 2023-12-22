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
    payload = f'''ffmpeg -y -i "{path}" -vn -ar 44100 -ac 2 -b:a 192k "{new_path}"'''
    subprocess.run(payload, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    try:
        new_size = os.path.getsize(new_path)
    except FileNotFoundError:
        return False, f"{new_path} not found"

    print(f"orig {size} new {new_size} = {(size - new_size)/size:.2%} redux")
    payload = f'''rm "{path}"'''
    subprocess.run(payload, shell=True)
    return True, new_path


# directory = "/Users/richard.liu/extra/music-frontend/audio"
# file = directory + "/daw1snippet/discovery 150.wav"

# compress(file)