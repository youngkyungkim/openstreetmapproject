#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Your task is to use the iterative parsing to process the map file and
find out not only what tags are there, but also how many, to get the
feeling on how much of which data you can expect to have in the map.
Fill out the count_tags function. It should return a dictionary with the
tag name as the key and number of times this tag can be encountered in
the map as value.

Note that your code will be tested with a different data file than the 'example.osm'
"""
import xml.etree.cElementTree as ET
import pprint

def count_tags(filename):
    tags = {}
    n=0
    for event, elem in ET.iterparse(filename):
        for sub in elem:
            if sub.tag == "tag":
                if sub.attrib['k'] in tags:
                    tags[sub.attrib['k']].append(sub.attrib['v'])
                else:
                    tags[sub.attrib['k']] = []
                    tags[sub.attrib['k']].append(sub.attrib['v'])

    return tags
        # YOUR CODE HERE

def count_street(filename):
    tags = {}
    for event, elem in ET.iterparse(filename):
        for sub in elem:
            if sub.tag == "tag":
                if sub.attrib['k'] == "addr:street":
                    if elem.tag in tags:
                        tags[sub.attrib['v']] += 1
                    else:
                        tags[sub.attrib['v']] = 1
    return tags

def test():

#    tags = count_tags('sample3.osm')
    tags = count_street('sample3.osm')
    pprint.pprint(tags)



if __name__ == "__main__":
    test()
