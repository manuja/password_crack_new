from curses import echo
from flask import Flask, request, jsonify
from utils import register_service_consul, get_ports, generate_unique_id, get_greater_than_nodes, get_node_election,announce_message, ready_for_get_node_election, get_node_details, check_health,generate_shedule
from algo import Algo
import threading
import time
import random
import sys
import requests
from multiprocessing import Value
import logging
from itertools import combinations
from itertools import permutations
import asyncio
import websockets
import socket
import json
import numpy as np
from ast import literal_eval
from flask import Flask
from flask import Response
from flask import request
import logging
import logging.handlers
import json

counter = Value('i', 0)
app = Flask(__name__)

# verifying if port number and node name have been entered as command line arguments.
port_number = int(sys.argv[1])
assert port_number

node_name = sys.argv[2]
assert node_name

def init(wait=True):
    
    print("The side car implemenatation ......")


#this api is used to exchange details with each node
@app.route('/logDetails', methods=['POST'])
def side_car_log():
    data = request.get_json()
    print("daataaaaaa",data)
    node_name = data
    logging.basicConfig(filename=f"logs/{node_name}.log", level=logging.INFO)
    return jsonify({'responce': 'Sucessfully logged'}), 200

# @app.route('/logDetails', methods=['POST'])
# def handle_log():
#     if request.method == 'POST':
#        rd=request.form.to_dict()
#        rec=json.loads(rd['record'])
#        record = logging.makeLogRecord(rec)
#        #log1.handle(record)
#        return "OK"

@app.route('/announce_found', methods=['POST'])
def announce_found():
    data = request.get_json()
    message = data['message']
    print('Password have been cracked by %s ' % message)
    return jsonify({'response': 'OK'}), 200

@app.route('/')
def hello_world():
    return 'logging server'


# @app.route('/logDetails', methods=['POST'])
# def handle_log():
#     if request.method == 'POST':
#         log1=logging.getLogger('MTEST')
#         log1.setLevel(logging.DEBUG)
#         rd=request.form.to_dict()
#         print("eddddccccccccccccccccccccccccccccc",rd)
#         rec=json.loads(rd['record'])
#         print("redoooooooode",rec)
#         node_name=json.loads(rd['filename'])
#         print("aaaaaaaaaaaaa",node_name)
#         record = logging.makeLogRecord(rec)
#         log1.handle(record)
#         mfl=myflt()

        
#         rfh=logging.handlers.RotatingFileHandler(f"logs/{node_name}.log",'a',maxBytes=10000000,backupCount=10)
#         formatter = logging.Formatter('%(asctime)s %(name)-15s %(levelname)-8s %(message)s')
#         rfh.setFormatter(formatter)
#         log1.addHandler(rfh)
#         #log1.addFilter(mfl)
#        # log1.error("First error generated locally")
#         #app.run()
#         return "OK"

class myflt(logging.Filter):
  def filter(self,rec):
    print(rec.__dict__)
    return 1

@app.route('/getConfigInfo', methods=['GET'])
def get_node_details():

    PASSWORD_FILE = "passwordinfo.txt"
   
    return jsonify(PASSWORD_FILE), 200


timer_thread1 = threading.Timer(15, init)
timer_thread1.start()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=port_number)