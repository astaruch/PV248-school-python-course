#!/usr/bin/python

import time

for i in range(10):
    print('Sleeping {}s'.format(i))
    time.sleep(1)
print('OK')