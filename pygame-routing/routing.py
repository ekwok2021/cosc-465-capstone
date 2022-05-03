from asyncio.windows_events import NULL
import json
import random
from simulator import Advertisement
from simulator import AutonomousSystem




def Genroute(ases):
    rand_start = random.randint(1,len(ases))
    rand_end = random.randint(1,len(ases))
    while rand_end == rand_start:
        rand_end = random.randint(1,len(ases)+1)
    count = 1
    start = NULL
    end = NULL
    for AS in ases.keys():
        print(AS)
        if count == rand_start:
            start = AS
        elif count == rand_end:
            end = AS
        count += 1
    return (start, end)

def Update_cus(ases, customer, provider):

    old_pro = ases[customer]["providers"]
    old_pro.append(provider)
    ases[customer]["providers"] = old_pro

    old_cus = ases[provider]["customers"]
    old_cus.append(customer)
    ases[provider]["customers"] = old_cus

    return ases

def Update_peer(ases, peerA, peerB):
    old_p1 = ases[peerA]["peers"]
    old_p1.append(peerB)
    ases[peerA]["peers"] = old_p1

    old_p2 = ases[peerB]["peers"]
    old_p2.append(peerA)
    ases[peerB]["peers"] = old_p2

    return ases

def Genrelations(topo):
    ases = {}
    # initialize the dictionary
    for AS in topo["ases"]:
        num = AS["number"]
        ases[num] = {}
        ases[num]["prefix"] = AS["prefix"]
        ases[num]["customers"] = []
        ases[num]["providers"] = []
        ases[num]["peers"] = []

    
    # update all relationships in the dictionary
    for relationship in topo["relationships"]:
        if "customer" in relationship:
            customer = relationship["customer"]
            provider = relationship["provider"]
            ases = Update_cus(ases, customer, provider)
        else:
            peerA = relationship["peerA"]
            peerB = relationship["peerB"]
            ases = Update_peer(ases, peerA, peerB)

    return ases

def Gengraphs(level):
    if level == 1:
        with open("topologies/linear.json") as topo_file:
            topo = json.load(topo_file)

    elif level == 2: 
        with open("topologies/warm-up.json") as topo_file:
            topo = json.load(topo_file)
    else:
        with open("topologies/example.json") as topo_file:
            topo = json.load(topo_file)
    ases = Genrelations(topo)

    return ases