#! /usr/bin/env python

import os
import subprocess
import xml.etree.ElementTree as ET

import requests


DDB_BUCKET_URL = 'https://s3-us-west-2.amazonaws.com/dynamodb-local/'


req = requests.get(DDB_BUCKET_URL)
root = ET.fromstring(req.text)

keys = [key.text for content in root.findall('{http://s3.amazonaws.com/doc/2006-03-01/}Contents')
        for key in content.findall('{http://s3.amazonaws.com/doc/2006-03-01/}Key')
        if key.text.endswith('.tar.gz')]
print(keys)

dockerfile = open('Dockerfile').read()
for key in keys:
    version = key.replace('dynamodb_local_', '').replace('.tar.gz', '')
    print('Key = ' + key + ', version = ' + version)
    if (version == 'latest' or version < '2016-01-01'):
        # Ignore older versions
        continue
    try:
        os.mkdir(version)
    except:
        pass
    new_dockerfile = dockerfile.replace('latest', version)
    open(os.path.join(version, 'Dockerfile'), 'w').write(new_dockerfile)

# test
for d in os.listdir('.'):
    if os.path.isdir(d) and not d.startswith('.'):
        print ('Working on ' + d)
        subprocess.call(
            ['docker', 'build', '--tag', 'cnadiminti/dynamodb-local:' + d, d])
