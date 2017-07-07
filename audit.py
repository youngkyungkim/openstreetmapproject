"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
postal_check = re.compile(r'^([a-z-]|_)*$')
OSMFILE = "sample.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

street_types = defaultdict(int)
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons"]

# UPDATE THIS VARIABLE
mapping = { "St": "Street",
            "St.": "Street",
            "Ave": "Avenue",
            "Rd.": "Road",
            "Blvd.": "Boulevard",
            "RD": "Road",
            "Rd": "Road",
            "Blvd": "Boulevard",
            "Dr": "Drive",
            "Pkwy": "Parkway"
            }



def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()

        street_types[street_type] += 1

def print_sorted_dict(d):
    keys = d.keys()
    keys = sorted(keys, key=lambda s: s.lower())
    for k in keys:
        v = d[k]
        print "%s: %d" % (k, v)


def is_street_name(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:street")

def is_post_code(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:postcode")

def is_state_name(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:state")

def is_fax(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "fax")

def is_phone(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "phone")

def audit(elem):
    if is_street_name(elem):
        if elem.attrib['v'] not in expected:
            for keys in mapping.keys():
                if keys in elem.attrib['v']:
                    elem.attrib['v'] = re.sub(keys, mapping[keys], elem.attrib['v'])
                    return elem.attrib['v']
            else:
                return elem.attrib['v']
        else:
            return elem.attrib['v']

    elif is_post_code(elem):
        m = postal_check.search(elem.attrib['v'])
        if m:
            if "-" in elem.attrib['v']:
                name = elem.attrib['v'].split("-")
                elem.attrib['v'] = name[0]
                return elem.attrib['v']

            else:
                name = elem.attrib['v'].split(" ")
                elem.attrib['v'] = name[1]
                return elem.attrib['v']
        else:
            return elem.attrib['v']

    elif is_state_name(elem):
        if elem.attrib['v'] == "Arizona":
            elem.attrib['v'] = "AZ"
            return elem.attrib['v']
        else:
            return elem.attrib['v']


    elif is_fax(elem):
        if "+" in elem.attrib['v']:
            elem.attrib['v'] = elem.attrib['v'].replace("+1-", "")
            elem.attrib['v'] = elem.attrib['v'].replace("+1 ", "")
            elem.attrib['v'] = elem.attrib['v'].replace("+1", "")
            elem.attrib['v'] = elem.attrib['v'].replace("1 ", "")
            elem.attrib['v'] = elem.attrib['v'].replace("1", "")
            elem.attrib['v'] = elem.attrib['v'].replace("+ ", "")
            elem.attrib['v'] = elem.attrib['v'].replace("+", "")
#            elem.attrib['v'] = re.sub("+", "", elem.attrib['v'])
            if " " in elem.attrib['v']:
                elem.attrib['v'] = re.sub(" ", "-", elem.attrib['v'])
                return elem.attrib['v']
            else:
                return elem.attrib['v']
        elif "(" in elem.attrib['v']:
            elem.attrib['v'] = elem.attrib['v'].replace("(", "")
            elem.attrib['v'] = elem.attrib['v'].replace(")", "")
#            elem.attrib['v'] = re.sub("(", "", elem.attrib['v'])
#            elem.attrib['v'] = re.sub(")", "", elem.attrib['v'])
            if " " in elem.attrib['v']:
                elem.attrib['v'] = re.sub(" ", "-", elem.attrib['v'])
                return elem.attrib['v']
            else:
                return elem.attrib['v']
        elif " " in elem.attrib['v']:
            elem.attrib['v'] = re.sub(" ", "-", elem.attrib['v'])
            return elem.attrib['v']
        else:
            return elem.attrib['v']

    elif is_phone(elem):
        if "+" in elem.attrib['v']:
            elem.attrib['v'] = elem.attrib['v'].replace("+1-", "")
            elem.attrib['v'] = elem.attrib['v'].replace("+1 ", "")
            elem.attrib['v'] = elem.attrib['v'].replace("+1", "")
            elem.attrib['v'] = elem.attrib['v'].replace("1 ", "")
            elem.attrib['v'] = elem.attrib['v'].replace("1", "")
            elem.attrib['v'] = elem.attrib['v'].replace("+ ", "")
            elem.attrib['v'] = elem.attrib['v'].replace("+", "")
#            elem.attrib['v'] = re.sub("+", "", elem.attrib['v'])
            if " " in elem.attrib['v']:
                elem.attrib['v'] = re.sub(" ", "-", elem.attrib['v'])
                return elem.attrib['v']
            else:
                return elem.attrib['v']
        elif "(" in elem.attrib['v']:
            elem.attrib['v'] = elem.attrib['v'].replace("(", "")
            elem.attrib['v'] = elem.attrib['v'].replace(")", "")
#            elem.attrib['v'] = re.sub("(", "", elem.attrib['v'])
#            elem.attrib['v'] = re.sub(")", "", elem.attrib['v'])
            if " " in elem.attrib['v']:
                elem.attrib['v'] = re.sub(" ", "-", elem.attrib['v'])
                return elem.attrib['v']
            else:
                return elem.attrib['v']
        elif " " in elem.attrib['v']:
            elem.attrib['v'] = re.sub(" ", "-", elem.attrib['v'])
            return elem.attrib['v']
        else:
            return elem.attrib['v']
    else:
        return elem.attrib['v']



def update_name(name, mapping):
    m = street_type_re.search(name)
    if m.group() not in expected:
        if m.group() in mapping.keys():
            name = re.sub(m.group(), mapping[m.group()], name)
    return name



def test():
    st_types = audit(OSMFILE)
    assert len(st_types) == 3
    pprint.pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name
            if name == "West Lexington St.":
                assert better_name == "West Lexington Street"
            if name == "Baldwin Rd.":
                assert better_name == "Baldwin Road"


if __name__ == '__main__':
    audit(OSMFILE)
