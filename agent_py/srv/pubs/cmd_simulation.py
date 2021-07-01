import math
from datetime import datetime as dt

counter=0
def movement(nodes: list, step=5000, max_step=1000000, ray=10000, step_ray=1):
    """
    Simulazione di movimento elementi presenti in area
    """
    global counter
    message = []
    for x in nodes:
        message.append(x.copy())
        if x["x"] == x["y"] == x["z"] == 0:
            next_step = (counter/max_step)*2*math.pi*step_ray
            message[-1]["x"] = math.cos(next_step)*ray
            message[-1]["y"] = math.sin(next_step)*ray
            message[-1]["z"] = math.tan(next_step)*ray
        elif x["x"] == x["y"] == x["z"] == -1:
            next_step = (counter/max_step) * \
                2*math.pi*(-step_ray)
            message[-1]["x"] = math.cos(next_step)*ray
            message[-1]["y"] = math.sin(next_step)*ray
            message[-1]["z"] = math.tan(next_step)*ray
    counter += step
    if counter >= max_step:
        counter = 0
        step_ray *= -1
    
    # values = []
    # columns = list(message[-1].keys())
    # for row in message:
    #     values.append([])
    #     for label in row.keys():
    #         values[-1].append(row[label])
    # data = dict(series=[dict(
    #      columns=columns,
    #      values=values
    #  )])
    data=[]
    for single in message:
        data.append({
            "time":0,
           "fields": {
               "mac": single["mac"], 
               "x": single["x"],
               "y": single["y"],
               "z": single["z"],
               "q": single["q"]},
           "tags": {"id": single["id"], "ts": int(dt.utcnow().timestamp()*1e6)}
         })         
    return None, dict(query="save",data=data)
