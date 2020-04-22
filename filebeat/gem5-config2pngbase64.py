#!/usr/bin/env python
# encoding: utf-8

# base64.b64encode(open("filename.png", "rb").read())

# In python3, base64.b64encode returns a bytes instance,
# so it's necessary to call decode to get a str,
# if you are working with unicode text.
#
# ------------------------------------------------------
# # Image data from [Wikipedia][1]
# >>>image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x05\x00\x00\x00\x05\x08\x06\x00\x00\x00\x8do&\xe5\x00\x00\x00\x1cIDAT\x08\xd7c\xf8\xff\xff?\xc3\x7f\x06 \x05\xc3 \x12\x84\xd01\xf1\x82X\xcd\x04\x00\x0e\xf55\xcb\xd1\x8e\x0e\x1f\x00\x00\x00\x00IEND\xaeB`\x82'
#
# # String representation of bytes object includes leading "b" and quotes,
# # making the uri invalid.
# >>> encoded = base64.b64encode(image_data) # Creates a bytes object
# >>> 'data:image/png;base64,{}'.format(encoded)
# "data:image/png;base64,b'iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=='"
#
#
# # Calling .decode() gets us the right representation
# >>> encoded = base64.b64encode(image_data).decode()
# >>> 'data:image/png;base64,{}'.format(encoded)
# 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=='
# ------------------------------------------------------
#
#
# If you are working with bytes directly,
# you can use the output of base64.b64encode without further decoding.
#
# ------------------------------------------------------
# >>> encoded = base64.b64encode(image_data)
# >>> b'data:image/png;base64,' + encoded
# b'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=='
# ------------------------------------------------------

# I find some code on  http://www2.stat.duke.edu/~sayan/python/pydot.py
# After some time I know that it is the source code of pydot module
# (The documentation of pydot is emmm)

# The do_dot() and callgraph.write_svg are in gem5/src/python/m5/util/dot_writer.py

# This link talks about how to read .dot file and convert it to png string not a file
# https://stackoverflow.com/questions/38301651/is-it-possible-to-get-output-of-pydot-graph-without-intermediate-file

import base64
import pydot
import os
import dot_parser

def config2pngbase64():
    gem5_path = os.getenv('GEM5_PATH')
    if (gem5_path):
        config_dot_path = os.path.join(gem5_path, "m5out/config.dot")
        callgraph = pydot.graph_from_dot_file(config_dot_path)
        if (callgraph):
            png_string = callgraph[0].create_png()
            # it seems that both with and without decode() work well
            encoded = base64.b64encode(png_string).decode()
            encoded = 'data:image/png;base64,{}'.format(encoded)
            with open(os.path.join(gem5_path, "m5out/config.dot.png.base64"), "w+") as f:
                length = len(encoded)
                for i in range(length-80,79,-80):
                    if (i>=0 and i<=len(encoded)):
                        encoded = encoded[0:i] + '\n' + encoded[i:]
                f.write(encoded)
    else:
        print "The GEM5_PATH is not set. Can not create index for config.dot.svg."
if __name__ == "__main__":
    config2pngbase64()
