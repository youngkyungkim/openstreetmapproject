# OpenStreetMap Data Case Study

### Map Area
Phoenix, Arizona, United States

- [https://www.openstreetmap.org/relation/111257#map=10/33.6055/-112.1258](https://www.openstreetmap.org/relation/111257#map=10/33.6055/-112.1258)
- [https://mapzen.com/data/metro-extracts/metro/phoenix_arizona/](https://mapzen.com/data/metro-extracts/metro/phoenix_arizona/)

I used to live in Phoenix. I wanted to look back at those places I used to go and to see how much the city, since I have left.


## Problems Encountered in the Map
After downloading file of Phoenix area, I ran smaller.py to get small sample from the file I had just downloaded.
From examining the sample through running a mapparser.py which shows tag elements, I noticed few problems with the data.

1. Inconsistent postal code *("AZ 84032", "85023-254", "AZ 85375 \u200e", "85302")*
2. Inconsistent state name *("Arizona", "AZ")*
3. Over­abbreviated  street names *("Ave", "St")*
4. Inconsistent phone and fax number *("+1 403 948 923", "406 403 305")*


### 1. Inconsistent postal code
I used audit.py to find postal code that are inconsistent and update the code to make postal code consistent. Below is the part of the code from the audit.py

```python
def is_post_code(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:postcode")

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

```
This updated all the postal codes, which had abbreviation in the front of the code(AZ 54368) or have more than 5 numbers(54368-345), into just five numbers(54368).

### 2. Inconsistent state name
I used audit.py to find state names that are inconsistent and update the names to make state names consistent. Below is the part of the code from the audit.py

```python
def is_state_name(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:state")

elif is_state_name(elem):
    if elem.attrib['v'] == "Arizona":
        elem.attrib['v'] = "AZ"
        return elem.attrib['v']
    else:
        return elem.attrib['v']
```
This updated all the states names, which had full name as Arizona, into abbreviation of state as AZ

### 3. Overabbreviated street name
I used mapparser.py to find overabbreviated street name. Below is the part of the code from the mapparser.py
```python
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
```

I used audit.py to update abbreviated street name into full name. Below is the part of the code from the audit.py

```python
def is_street_name(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:street")

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
```
This updated all the street names, which had abbreviation as St, into full name as Street.


### 4. Inconsistent phone and fax number
I used audit.py to find numbers that are inconsistent and update the numbers to become consistent. Below is the part of the code from the audit.py.
```python
def is_phone(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "phone")

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
```

This updated all the numbers, which had country code or other symbols as + or (), into number without country code and other symbols.

# Data Overview and Additional Ideas
This section contains basic statistics about the dataset, the SQL queries used to gather them, and some additional ideas about the data in context.

### Size of the file
```
phoenix_arizona.osm ......... 687.6 MB
mydb.db .......... 395.7 MB
nodes.csv ............. 254.4 MB
nodes_tags.csv ........ 11.6 MB
ways.csv .............. 23.8 MB
ways_tags.csv ......... 60.5 MB
ways_nodes.cv ......... 85.8 MB  
```  
### Number of Unique users
```sql
select count(distinct uid) from (select uid from nodes union all select uid from ways) un;
```
1485

### Number of Nodes
```sql
select count(*) from nodes;
```
2999366

### Number of Ways
```sql
select count(*) from ways;
```
389536

### Number of shops
```sql
select key, count(*) as num from nodes_tags where key="shop" group by key;
```
shop|1974

### Top five types of shops
```sql
 select value, count(*) as num from nodes_tags where key="shop" group by value order by num desc limit 5;
```
convenience|597
supermarket|191
clothes|143
car_repair|113
mobile_phone|65

### Other ideas about the dataset

```sql
select key, count(*) as num from nodes_tags group by key order by num desc;
```
From looking at the above sql, I could notice some keys need a update, especially "fixme" or "FIXME" keys.

```sql
select type, key, value from nodes_tags where key="FIXME";
```
regular|FIXME|The church is no longer here it is a taco place. The change should be reported to the geonames people.
regular|FIXME|check religion

From looking at the value given above, there is a lot of fields that need to be update. For example, the we should check whether the place is a church or a taco place, and also check the religion of given place.

```sql
select nodes.lat, nodes.lon from nodes, nodes_tags where nodes.id=nodes_tags.id and nodes_tags.value="check religion";
```

33.5059155|-112.0356437
I used sql above to find the latitude and longitude of the place that had "check religion" value.
[http://www.latlong.net/Show-Latitude-Longitude.html](http://www.latlong.net/Show-Latitude-Longitude.html)
I went to above link and inserted the latitude and longitude to find the address.
I used the address to look at street map provided by google map.
However, there wasn't any building related to religion.

```sql
select nodes.timestamp from nodes, nodes_tags where nodes.id=nodes_tags.id and nodes_tags.value="check religion";
```

2014-06-20T04:17:44Z
Maybe there might have been some building related to religion in 2014 but have changed into malls and hospital.

From this I learned that we should check the timestamp or the day it was edited before using the data because the older the dates are there is a more chance of data being inaccurate.

Therefore, before using a data we should look at timestamp of the data through using a sql as below.

```sql
select timestamp from nodes order by timestamp limit 20;
```
2006-08-12T23:48:13Z
2007-12-29T04:02:39Z
2007-12-29T04:04:46Z
2007-12-29T04:04:46Z
2007-12-30T08:04:54Z
2007-12-30T19:36:34Z
2007-12-30T19:36:34Z
2007-12-30T19:36:34Z
2007-12-30T19:36:34Z
2007-12-30T19:36:38Z
2007-12-31T00:12:45Z
2007-12-31T00:39:43Z
2007-12-31T00:43:21Z
2007-12-31T00:43:21Z
2007-12-31T00:43:21Z
2007-12-31T00:43:21Z
2007-12-31T00:43:21Z
2007-12-31T00:43:21Z
2007-12-31T01:01:55Z
2007-12-31T01:10:16Z
From looking at the sql above we have data that is almost 10 years old. We should "where" method in sql to use recent data. For example we could set "where timestamp > 2014" to use only data that has been fixed after 2014.

The benefit of doing this would be that we could avoid using obsolete data. However, the challenges is that whether timestamp is the best variable in deciding the data is obsolete or not.

It is possible that nothing had changed in the location through numerous years.
However, from looking at different variables in the database I do not think there is a better variable than timestamp that could indicate whether data is obsolete or not, so I think using timestamp has more benefit than challenge, especially when we are aware of the possible challenge. 
