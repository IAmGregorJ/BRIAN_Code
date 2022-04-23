'''imports'''
import shutil
import re
import os
from pathlib import Path

tf = open('tmp', 'a+') #pylint:disable=unspecified-encoding
f = Path(__file__).resolve().parents[1]
f= f / 'secrets.ini'

smtp='smtp.gmail.com'
port='555'
username='p01y61077@gmail.com'
passwd='vaiujaveebpxcpcx'

with open(f) as x: #pylint:disable=unspecified-encoding
    for line in x.readlines():
        line = re.sub('smtp_server=.*', 'smtp_server='+smtp, line)
        line = re.sub('smtp_port=.*', 'smtp_port='+port, line)
        line = re.sub('smtp_user.*', 'smtp_user='+username, line)
        line = re.sub('smtp_pass.*', 'smtp_pass='+passwd, line)
        tf.write(line)
tf.close()
x.close()
shutil.copy('tmp', f)
os.remove('tmp')
