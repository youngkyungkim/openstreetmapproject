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



def is_street_name(elem):
    ''' check whether the element is street type'''
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:street")

def is_post_code(elem):
    ''' check whether the element is postal code'''
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:postcode")

def is_state_name(elem):
    ''' check whether the element is state name'''
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:state")

def is_fax(elem):
    ''' check whether the element is a number'''
    return (elem.tag == "tag") and (elem.attrib['k'] == "fax")

def is_phone(elem):
    ''' check whether the element is a number'''
    return (elem.tag == "tag") and (elem.attrib['k'] == "phone")

def audit(elem):
    ''' check the type of element's value of "v" and update the value to make values consistent.'''
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



if __name__ == '__main__':
    audit(OSMFILE)
