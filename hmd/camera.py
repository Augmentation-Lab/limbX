import subprocess

def take_photo():
    subprocess.call(['sh', 'take_photo.sh'])
    return