# Realtime bus ETA experiment project

This project is an experimental project as a coding practice with python. Components include understanding the API provided by Citybus (and NWFB) and data.gov.hk.

## API main page

>https://data.gov.hk/en-data/dataset/ctb-eta-transport-realtime-eta


The objective of this project is to get familiar with retriving realtime data from API and the data structure.

All data retrieved from API are in `` JSON `` format. Except ETA (estinated arrival time) data are retrieved from API everytime, other functions will store the retrieved data locally into a JSON under the 

## Prerequisites
---
Python 3.7 or above, due to the need for supporting %z directive in the ``datetime.strptime()`` method introduce from 3.7 which is used by this code.

## Usage
---
To use the bus_main class, place the ``bus_main.py`` in the same folder as your code and import as below:

``` python
import bus_main
```


## Class method
---
### ``get_all_routes(``*``company``*``)``
Can be used without creating the bus_main object. This method will return all route information for a particular company. The parameter should be either **ctb** for Citybus or **nwfb** for New World First Bus.
```
get_all_routes("ctb")
```
Returns type is a python dictionay.
```
 {'routes': [{'co': 'CTB', 'dest_tc': '跑馬地 (上)', 'orig_tc': '摩星嶺', 'route': '1'},
            {'co': 'CTB', 'dest_tc': '北角碼頭', 'orig_tc': '堅尼地城', 'route': '10'},
            {'co': 'CTB', 'dest_tc': '美孚', 'orig_tc': '筲箕灣', 'route': '102'},
            {'co': 'CTB', 'dest_tc': '美孚', 'orig_tc': '筲箕灣', 'route': '102P'}]}
```

---
## To be developed....
### ```print_all_routes()```



### ```check_route()```


## Class function
### ``get_eta()``
    

### ``print_eta()``

### ``get_bus_stop()``

### ``print_bus_stop()``# BusDev
