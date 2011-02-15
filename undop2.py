# Author: HH Veldstra <http://veldstra.org>
# Inspired by Patrick Collison's undop <http://collison.ie/blog/2009/08/undop>
#
# License: MIT

BAD_SITES = [
    "twitter.com",
    "news.ycombinator.com",
    "reddit.com",
    "facebook.com",
    ]

import subprocess
import time

def undop():
    subprocess.call("./undop")

# FIXME: All interfaces not just en1.
cmd = "tcpdump -l -i en1 port http and host (%s)" % " or ".join(BAD_SITES)
popen = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)

previous_timestamp = time.localtime()
for line in iter(popen.stdout.readline, ""):
    # Whenever there's a line, a bad site is being visited.
    # line is something like:
    # 15:29:57.456575 IP 128.242.245.84.http > 10.40.17.161.54026: . 9601:10801(1200) ack 1585 win 9600
    current_time = time.localtime()
    timestamp = time.strptime(("%s:%s:%s " % (current_time.tm_year, current_time.tm_mon, current_time.tm_mday)) + line.split()[0].split(".")[0], "%Y:%m:%d %H:%M:%S")
    delta = time.mktime(timestamp) - time.mktime(previous_timestamp)
    if delta > 10:
        undop()
        previous_timestamp = timestamp