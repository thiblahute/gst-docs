#!/usr/bin/env python3
import os
import sys


CDIR = os.path.dirname(os.path.realpath(__file__))

print(os.path.join(CDIR, 'sitemap.txt'))
if __name__ == "__main__":
    with open(os.path.join(CDIR, 'sitemap.txt')) as f:
        index = f.read()
        if sys.argv[1]:
            index += sys.argv[1]

            index = '\n'.join('\t' + l for l in index.splitlines())
            index = 'gst_index.md\n' + index
        with open(os.path.join(CDIR, 'generated_sitemap.txt'), 'w') as fw:
            fw.write(index)
