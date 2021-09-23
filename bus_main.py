# -*- coding: utf-8 -*-
# Early prototype - use at risk

import datetime
import json
import http.client
from json.decoder import JSONDecodeError
import os
import time
from datetime import *

BASE_URL = "rt.data.gov.hk"
BASE_URL_KMB = "data.etabus.gov.hk"

# folder_prefix = "bus_data"
folder_prefix = "/home/bus_data"



def get_all_routes(company):

    # company = str(company).upper()
    
    if company == "ctb" or company == "nwfb":
        conn = http.client.HTTPSConnection(BASE_URL)
        conn.request("GET", f"/v1/transport/citybus-nwfb/route/{company}")
        all_routes_file_name = f'{folder_prefix}/{company}_all_routes.json'
        all_routes_list = {}
        try:
            with open(all_routes_file_name, encoding="utf-8") as json_file:
                all_routes_list = json.load(json_file)
                # all_routes_list_date = datetime.strptime(all_routes_list["generated_timestamp "], '%Y-%m-%dT%H:%M:%S%z').replace(tzinfo=None)
                all_routes_list_date = datetime.strptime(all_routes_list["generated_timestamp "], '%Y-%m-%dT%H:%M:%S+08:00').replace(tzinfo=None)
                if (datetime.now() - all_routes_list_date).days > 7:
                    with open(all_routes_file_name, "w", encoding="utf-8") as json_file:
                        json.dump(json.loads(conn.getresponse().read().decode("utf-8")), json_file, ensure_ascii=False, indent=4)

        except JSONDecodeError:
            all_routes_list = json.loads(conn.getresponse().read().decode("utf-8"))
            with open(all_routes_file_name, "w",encoding="utf-8") as json_file:
                json.dump(all_routes_list, json_file, ensure_ascii=False, indent=4)

        except FileNotFoundError:
            if not os.path.exists(folder_prefix):
                print(f"Folder {folder_prefix} not exist, creating.")
                os.makedirs(folder_prefix)
            all_routes_list = json.loads(conn.getresponse().read().decode("utf-8"))
            with open(all_routes_file_name, "w", encoding="utf-8") as json_file:
                json.dump(all_routes_list, json_file, ensure_ascii=False, indent=4)
    elif company == "kmb":
        conn = http.client.HTTPSConnection(BASE_URL_KMB)
        conn.request("GET", "/v1/transport/kmb/route/")
        all_routes_file_name = f'{folder_prefix}/{company}_all_routes.json'
        all_routes_list = {}

        try:
            with open(all_routes_file_name, encoding="utf-8") as json_file:
                all_routes_list = json.load(json_file)
                # all_routes_list_date = datetime.strptime(all_routes_list["generated_timestamp "], '%Y-%m-%dT%H:%M:%S%z').replace(tzinfo=None)
                all_routes_list_date = datetime.strptime(all_routes_list["generated_timestamp"], '%Y-%m-%dT%H:%M:%S+08:00').replace(tzinfo=None)
                if (datetime.now() - all_routes_list_date).days > 7:
                    with open(all_routes_file_name, "w", encoding="utf-8") as json_file:
                        json.dump(json.loads(conn.getresponse().read().decode("utf-8")), json_file, ensure_ascii=False, indent=4)

        except JSONDecodeError:
            all_routes_list = json.loads(conn.getresponse().read().decode("utf-8"))
            with open(all_routes_file_name, "w",encoding="utf-8") as json_file:
                json.dump(all_routes_list, json_file, ensure_ascii=False, indent=4)

        except FileNotFoundError:
            if not os.path.exists(folder_prefix):
                print(f"Folder {folder_prefix} not exist, creating.")
                os.makedirs(folder_prefix)
            all_routes_list = json.loads(conn.getresponse().read().decode("utf-8"))
            with open(all_routes_file_name, "w", encoding="utf-8") as json_file:
                json.dump(all_routes_list, json_file, ensure_ascii=False, indent=4)

    if company == "ctb" or company == "nwfb":
        return {"routes" : [{"co" : route["co"],"route" : route["route"], "orig_tc" : route["orig_tc"], "dest_tc" : route["dest_tc"]} for route in all_routes_list["data"]]}
    elif company == "kmb":
        return {"routes" : [{"co" : company,"route" : route["route"], "orig_tc" : route["orig_tc"], "dest_tc" : route["dest_tc"]} for route in all_routes_list["data"]]}


def get_all_company_routes():
    ctb_routes = get_all_routes("ctb")
    nwfb_routes = get_all_routes("nwfb")
    kmb_routes = get_all_routes("kmb")

    all_routes = {  "ctb" : ctb_routes["routes"], "nwfb" : nwfb_routes["routes"], "kmb" : kmb_routes["routes"]}
    return all_routes
    # for routes in [all_routes]:
    #     for route in routes:
    #         for i in route:
    #             print(f'{i["co"]}\t{i["route"]}\t{i["orig_tc"]} --> {i["dest_tc"]}')


def check_route():
    route_to_check = input("Check route number: ").upper()
    ctb_routes = get_all_routes("ctb")
    nwfb_routes = get_all_routes("nwfb")
    all_routes = [ctb_routes["routes"], nwfb_routes["routes"]]

    for routes in [all_routes]:
        for route in routes:
            for i in route:
                if i["route"] == route_to_check:
                    print(f'{i["co"]}\t{i["route"]}\t{i["orig_tc"]} --> {i["dest_tc"]}')

def print_all_routes():
    ctb_routes = get_all_routes("ctb")
    nwfb_routes = get_all_routes("nwfb")

    all_routes = [ctb_routes["routes"], nwfb_routes["routes"]]

    for routes in [all_routes]:
        for route in routes:
            for i in route:
                print(f'{i["co"]}\t{i["route"]}\t{i["orig_tc"]} --> {i["dest_tc"]}')

class bus_main:

    def __init__(self, company, route, direction):

        # import datetime
        self.BASE_URL = ""
        if company == "ctb" or company == "nwfb":
            self.BASE_URL = "rt.data.gov.hk"
            self.URL_COMPANY = "citybus-nwfb"
            self.URL_APPEND = ""
            self.URL_COMPANY2 = company
        else:
            self.BASE_URL = "data.etabus.gov.hk"
            self.URL_COMPANY = "kmb"
            self.URL_APPEND = "1"
            self.URL_COMPANY2 = ""
        self.conn = http.client.HTTPSConnection(self.BASE_URL)
        self.eta = {}
        self.updatetime = datetime.now()
        self.company = company
        self.route = route
        self.direction = direction
        self.bus_stop_code_list = []
        self.bus_stop_list = []
        self.bus_stop_file_name = f'{folder_prefix}/bus_stops_{self.company}_{self.route}_{self.direction}.json'
        self.get_bus_stop()

    def print_eta(self, bus_stop):
        eta_data = self.get_eta(bus_stop)

        print(eta_data["eta_title"])
        print(eta_data["eta_current_time"])
        for eta in eta_data["eta_list"]:
            print(eta)

    def get_eta_html(self, bus_stop):
        eta_data = self.get_eta(bus_stop)

        eta_html_text = []
        # eta_html_text.append(f'<html><head><meta charset="UTF-8"></head><body>')
        eta_html_text.append(f'<h3>{eta_data["eta_title"]}</h3>')
        eta_html_text.append(f'<h4>{eta_data["eta_current_time"]}</h4>')
        for eta in eta_data["eta_list"]:
            eta_html_text.append(f'<p>{eta}</p>')
        # eta_html_text.append(f"</body></html>")

        return eta_html_text

    def get_eta(self, bus_stop):

        self.updatetime = datetime.now()
        self.conn.request("GET", f"/v1/transport/{self.URL_COMPANY}/eta/{self.URL_COMPANY2}/{self.bus_stop_list[bus_stop-1]['bus_stop_code']}/{self.route}/{self.URL_APPEND}")
        eta_data = json.loads(self.conn.getresponse().read().decode("utf-8"))
        
        if int(self.updatetime.hour) > 18:
            eta_current_time =  (f"現在時間 ： 晚上 {int(self.updatetime.hour) % 12} 時 {self.updatetime.minute} 分")
        if int(self.updatetime.hour) > 12:
            eta_current_time =  (f"現在時間 ： 下午 {int(self.updatetime.hour) % 12} 時 {self.updatetime.minute} 分")
        else:
            eta_current_time = (f"現在時間 ： 早上 {self.updatetime.hour} 時 {self.updatetime.minute} 分")
        
        # eta_list = [datetime.strptime(eta["eta"],'%Y-%m-%dT%H:%M:%S%z') for eta in eta_data["data"]]
        # eta_list = [datetime.strptime(eta["eta"],'%Y-%m-%dT%H:%M:%S+08:00') for eta in eta_data["data"]]

        eta_list = []
        for eta in eta_data["data"]:
            if eta["eta"] == "":
                pass
            else:
                eta_list.append(datetime.strptime(eta["eta"],'%Y-%m-%dT%H:%M:%S+08:00'))

        eta_list_string = []
        eta_title = f"{self.route} 到站時間 由 {self.bus_stop_list[bus_stop-1]['bus_stop_name_tc'].split(',')[0]}"\
        f" 到 {self.bus_stop_list[len(self.bus_stop_list)-1]['bus_stop_name_tc'].split(',')[0]}:"
        for i in range(len(eta_list)):
            arrival_minutes =  eta_list[i].replace(tzinfo=None) - datetime.now()
            eta_list_string.append(f"下一班次 ： {int(arrival_minutes.seconds/60)} 分 {arrival_minutes.seconds%60} 秒 ({eta_list[i].hour%12} 時 {eta_list[i].minute} 分)")
        
        if eta_list_string == []:
            eta_list_string = ["- - 暫未有下一班次時間 - -"]

        return {
            "route_src" : self.bus_stop_list[bus_stop-1]['bus_stop_name_tc'].split(',')[0],
            "route_dest" : self.bus_stop_list[len(self.bus_stop_list)-1]['bus_stop_name_tc'].split(',')[0],
            "route" : self.route,
            "eta_current_time" : eta_current_time,
            "eta_title" : eta_title,
            "eta_list" : eta_list_string
        }

    def print_bus_stop(self):
        self.get_bus_stop()
        for i in self.bus_stop_list:
            print(f"{i['bus_stop_index']}: {i['bus_stop_name_tc']}")

    def get_bus_stop(self):
        import time

        def get_stop_list():
            self.conn.request("GET", f"/v1/transport/{self.URL_COMPANY}/route-stop/{self.URL_COMPANY2}/{self.route}/{self.direction}/{self.URL_APPEND}")
            bus_stop_data = json.loads(self.conn.getresponse().read().decode("utf-8"))

            for i in (bus_stop_data["data"]):
                self.bus_stop_code_list.append(i["stop"])

            for i in range (0, len(self.bus_stop_code_list)):
                bus_stop_code = self.bus_stop_code_list[i]
                self.conn.request("GET", f"//v1/transport/{self.URL_COMPANY}/stop/{bus_stop_code}")
                stop = json.loads(self.conn.getresponse().read().decode("utf-8"))
                self.bus_stop_list.append(
                {
                "bus_stop_index" : i+1,
                "bus_stop_code" : bus_stop_code , 
                "bus_stop_name_tc" : stop["data"]["name_tc"],
                "bus_stop_lat" : stop["data"]["lat"],
                "bus_stop_long" : stop["data"]["long"],
                })

        try:
            with open(self.bus_stop_file_name, encoding="utf-8") as json_file:
                file_create_time = datetime.strptime(time.ctime(os.path.getctime(self.bus_stop_file_name)), '%a %b %d %H:%M:%S %Y')
                self.bus_stop_list = json.load(json_file)

                # The function get_stop_list() will loop through all bus stops code tp get stop 
                # detail such as name and location via API so it will be less responsive, a JSON file
                # will be used for saving the bus stop information for this particular route.
                # If bus stop JSON file was created over 7 days, retrieve bus stops via API again

        except JSONDecodeError:
            get_stop_list()
            
            with open(self.bus_stop_file_name, "w", encoding="utf-8") as json_file:
                json.dump(self.bus_stop_list, json_file, ensure_ascii=False, indent=4)

        except FileNotFoundError:
            get_stop_list()
            if not os.path.exists(folder_prefix):
                print(f"Folder {folder_prefix} not exist, creating.")
                os.makedirs(folder_prefix)
            with open(self.bus_stop_file_name, "w", encoding="utf-8") as json_file:
                json.dump(self.bus_stop_list, json_file, ensure_ascii=False, indent=4)
        
        return self.bus_stop_list
