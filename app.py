#!/usr/bin/python3.9
from flask import Flask, redirect, url_for, render_template
import bus_main

app = Flask(__name__)

@app.route('/')
def entrance():
    return render_template("bus_all_routes.html", all_company_routes = bus_main.get_all_company_routes())

@app.route('/<company>/<route>/<direction>/<stop_code>/')
def eta(company, route, direction, stop_code):
    bus_route = bus_main.bus_main(company, route, direction)
    stop_code = int(stop_code)
    return render_template("bus_eta.html", stop_code=stop_code, eta_data=bus_route.get_eta(stop_code))

@app.route('/<company>/<route>/')
def route_inout(company, route):
    bus_route_inbound = bus_main.bus_main(company, route, "inbound")
    bus_route_outbound = bus_main.bus_main(company, route, "outbound")
    return render_template("bus_route_inout.html", route=bus_route_outbound.route, route_inbound=bus_route_inbound.get_bus_stop(), route_outbound=bus_route_outbound.get_bus_stop())

# app.run()

