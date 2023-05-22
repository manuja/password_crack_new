import time
import json
import requests
import numpy as np
from random import randint
import asyncio
import websockets
import logging, logging.handlers
import json

 
# asyncio.get_event_loop().run_until_complete(test())
class myHTTPHandler(logging.handlers.HTTPHandler):
  def mapLogRecord(self,record):
    #print("record is sss",record)
    trec={'record':json.dumps(record.__dict__),'filename': json.dumps("sidecar")}
    #trec={'filename': json.dumps(node_name)}
    return trec


def generate_unique_id():
    millis = int(round(time.time() * 10000))
    node_id = millis + randint(700000000000, 900000000000)
    return node_id


# Used to register the service in the service registry
def register_service_consul(node_name, node_port, node_id):
    invoke_url = "http://localhost:8500/v1/agent/service/register"
    data = {
        "Name": node_name,
        "ID": str(node_id),
        "port": node_port,
        "check": {
            "name": "Check Counter health %s" % node_port,
            "tcp": "localhost:%s" % node_port,
            "interval": "10s",
            "timeout": "1s"
        }
    }
    put_request_send = requests.put(invoke_url, json=data)
    return put_request_send.status_code

#check the health service
def check_health(service_detail):
    #print('Checking health of the %s' % service)
    url = 'http://localhost:8500/v1/agent/health/service/name/%s' % service_detail
    response_out = requests.get(url)
    response_content = json.loads(response_out.text)
    aggregated_state = response_content[0]['AggregatedStatus']
    service_status_out = aggregated_state
    if response_out.status_code == 503 and aggregated_state == 'critical':
        service_status_out = 'crashed'
    #print('Service status: %s' % service_status)
    return service_status_out


# get ports of all the registered nodes from consul
def get_ports():
    ports_dictionery = {}
    response = requests.get('http://127.0.0.1:8500/v1/agent/services')
    nodes_out = json.loads(response.text)
    for each_service in nodes_out:
        service = nodes_out[each_service]['Service']
        status = nodes_out[each_service]['Port']
        key = service
        value = status
        ports_dictionery[key] = value
    return ports_dictionery

#this fucntion get nodes which has higher nodes then current node
def get_greater_than_nodes(node_details, node_id):
    higher_nodes = []
    for each in node_details:
        if each['node_id'] > node_id:
            higher_nodes.append(each['port'])
    return higher_nodes

#get all ports of the node
def get_node_ports(node_details):
    higher_nodes = []
    for each in node_details:
        higher_nodes.append(each['port'])
    return higher_nodes

# this code create shedule for all the nodes
def generate_shedule(node_id):
    print("ccccccccccccccccccccc",node_id)
    ports_of_all_nodes = get_ports()
    print(ports_of_all_nodes)
    node_details=get_node_details(ports_of_all_nodes)
    print(len(node_details))

    #remove the leader node id from node details and need to send shedules to te other nodes
   # ports_of_all_nodes.pop(node_id)


    nodefactor=(len(ports_of_all_nodes)-1)
    # # creating an input array
    # numeric_array = np.array([0,1,2,3,4,5,6,7,8,9])
    # simple_array = np.array(["a","b","c","d","e","f","g","h","i","j"])
    # capital_array = np.array(["A","B","C","D","E","F","G","H","I","J"])
    numeric_array = np.array([0,1,2,3])
    simple_array = np.array(["a","b","c","d"])
    capital_array = np.array(["A","B","C","D"])

    # use numpy.split() function
    divided_numeric_array = np.split(numeric_array,nodefactor)
    divided_simple_array = np.split(simple_array,nodefactor)
    divided_capital_array = np.split(capital_array,nodefactor)  

    # use of range() to define a range of values
    values = range(nodefactor)
    abc = {}
    onearray = {}

    # iterate from i = 0 to i = 3
    for i in values:
        print(i)
        abc['result%s' % i] = np.concatenate((divided_numeric_array[i], divided_simple_array[i],divided_capital_array[i]))
        #print(abc['result%s' % i])
        onearray[i] = abc['result%s' % i]
   # workloaddevide(onearray,node_id)
    return onearray

# this method is used to share the workload to other nodes.
def workloaddevide(conarray,node_id):
    #print("combined array is",conarray)
    all_nodes=[]
    all_nodes = get_ports()
    print("current all nodes",all_nodes);
    print("need to remove id",node_id);
    all_nodes.pop(node_id)
    print("after remove id",all_nodes);

    # data = {
    #      'conarraycoordinator': conarray.tolist()
    # }
    incre=0
    for each_node in all_nodes:

        data = {
         "conarraycoordinator": conarray[incre].tolist(),
         "nodename" : node_id
        }
        incre = incre + 1
        url = 'http://localhost:%s/destributeworkload' % all_nodes[each_node]
        print(url)

        print(data)
        
        #requests.post(url, json=data)
        response= requests.post(url, json=data)
        # print("okkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
        # myLogger = logging.getLogger('MTEST')
        # myLogger.setLevel(logging.DEBUG)
        # httpHandler = myHTTPHandler('localhost:5009',url='/logDetails',method="POST")
        # myLogger.addHandler(httpHandler)
        # myLogger.info("tetx hiiiiii")










        #response= await asyncio.run(url)
        #print("retuenssss issss",json.loads(response.text))
        # nodes ={}
        # nodes = json.loads(response.text)

        # for each_service in nodes:
        #     print("retuenssss",nodes[each_service])
        
        # print("Responce is",nodes['response'])
        # if(nodes['response']=='01234c'):
        #     print("ok doeneeeeeeeeeeeeeeeeeeeeeeeeee")
    # for each_service in nodes:
    #     service = nodes[each_service]['Service']
    #     status = nodes[each_service]['Port']
    #     key = service
    #     value = status
    #     ports_dict[key] = value
    # return ports_dict

        
    

    # print(divided_numeric_array)
    # print(divided_simple_array)
    # print(divided_capital_array)
def read_password_file():
    password_array=[]
    # with open('passwordinfo.txt') as f:
    #  for line in f.readlines():
    #      password_array=line
    # print("my array is",password_array[2])
    # response = requests.get('http://127.0.0.1:5009/getConfigInfo')
    # passwordfile = json.loads(response.text)
    passwordfile = "passwordinfo.txt"
    print("File nameis for password",passwordfile)

    with open(passwordfile) as f:
        while True:
            line = f.readline()
            if not line:
                break
            print(line.strip())
            password_array.append(line.strip())
    #print(password_array)
    return password_array


#send the higher node id to the proxy
def get_node_election(higher_nodes, node_id):
    status_code = []
    for each_port in higher_nodes:
        url = 'http://localhost:%s/proxy' % each_port
        data = {
            "node_id": node_id
        }
        post_response = requests.post(url, json=data)
        
        status_code.append(post_response.status_code)
    if 200 in status_code:
        return 200

# def get_node_election(higher_nodes_array, node_id):
#     status_code_array = []
#     for each_port in higher_nodes_array:
        
#         url = 'http://localhost:%s/proxy' % each_port
#         data = {
#             "node_id": node_id
#         }
#         post_response = requests.post(url, json=data)
#         # myLogger = logging.getLogger('MTEST')
#         # myLogger.setLevel(logging.DEBUG)
#         # httpHandler = myHTTPHandler('localhost:5009',url='/logDetails',method="POST")
#         # myLogger.addHandler(httpHandler)
#         # myLogger.info("tetx hiiiiii")
#         status_code_array.append(post_response.status_code)
#     if 200 in status_code_array:
#         return 200




# this method returns if the cluster is ready for the election
def ready_for_get_node_election(ports_of_all_nodes, self_election, self_coordinator):
    coordinator_array = []
    election_array = []
    print(ports_of_all_nodes)
    print("-------------------")
    node_details = get_node_details(ports_of_all_nodes)
    print(node_details)

    for each_node in node_details:
        coordinator_array.append(each_node['coordinator'])
        election_array.append(each_node['election'])
    coordinator_array.append(self_coordinator)
    election_array.append(self_election)

    if True in election_array or True in coordinator_array:
        return False
    else:
        return True


# this method is used to get the details of all the nodes by syncing with each node by calling each nodes' API.
def get_node_details(ports_of_all_nodes):
    node_details = []
    for each_node in ports_of_all_nodes:
        url = 'http://localhost:%s/nodeDetails' % ports_of_all_nodes[each_node]
        data = requests.get(url)
        # myLogger = logging.getLogger('MTEST')
        # myLogger.setLevel(logging.DEBUG)
        # httpHandler = myHTTPHandler('localhost:5009',url='/logDetails',method="POST")
        # myLogger.addHandler(httpHandler)
        # myLogger.info(str(data.status_code) + str(data.reason) + " Node details extracted")
        node_details.append(data.json())
    return node_details


# this method is used to announce that it is the master to the other nodes.
def announce_message(coordinator_node):
    all_nodes = get_ports()
    data = {
        'coordinator': coordinator_node
    }
    for each_node in all_nodes:
        invoke_url = 'http://localhost:%s/announce' % all_nodes[each_node]
        print(invoke_url)
        requests.post(invoke_url, json=data)


# this method is used to announce that it is the master to the other nodes.
def broadcastFound(nodefound):
    #print("vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv")
    all_nodes = get_ports()
    data = {
        'message': nodefound
    }
    for each_node in all_nodes:
        url = 'http://localhost:%s/announce_found' % all_nodes[each_node]
        print(url)
        requests.post(url, json=data)