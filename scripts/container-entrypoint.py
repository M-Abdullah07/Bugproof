"""Initialize mount ownership, then drop privileges before serving requests."""
import os
from pathlib import Path

if os.getuid()==0:
    # A newly mounted volume may hide the image's /data ownership.
    data=Path("/data")
    data.mkdir(exist_ok=True)
    os.chown(data,10001,10001)
    os.setgroups([])
    os.setgid(10001)
    os.setuid(10001)
os.execvp("python",["python","-m","bugproof"])
