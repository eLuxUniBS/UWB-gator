import mqttools
from datetime import datetime as dt

from agent.skeleton import MQTTAgent
import orm


async def pong(*args, **kwargs):
    print("PONG", args, "\n", kwargs)


async def network_refresh(topic="", raw={}, header={}, payload={},
                          client: mqttools.Client = None,
                          cb_next_hop: MQTTAgent.publisher = None):
    """
    Aggiorna tutti i subs con la nuova rete!
    :param topic:
    :param raw:
    :param header:
    :param payload:
    :param client:
    :param cb_next_hop:
    :return:
    """
    print("REQUEST REFRESH NETWORK")
    collect_node = dict()
    print(orm.db.Net.__name__)
    try:
        for net in orm.db.Net.objects.get(dict(avaiable=True)):
            collect_node[net.name] = dict()
            for subnet in orm.db.SubNet.objects.get(dict(net=net)):
                collect_node[net.name][subnet.name] = dict()
                for node in orm.db.Node.objects.get(dict(subnet=subnet)):
                    collect_node[net.name][subnet.name][node._id]=node
        print(collect_node)
    except Exception as e:
        print("Errore in DB",e)
    await cb_next_hop(topic="/net", payload={
        "message":
            "Ricevuto {}#{} alle {}, e rinviato alle {}".format(
                header.get("name", "-missing-"),
                header.get("uuid", "-missing-"),
                header.get("ts", "-missing-"),
                dt.utcnow().__str__())})



async def network_update(topic="", raw={}, header={}, payload={},
                         client: mqttools.Client = None,
                         cb_next_hop: MQTTAgent.publisher = None):
    if client is None:
        print("Impossibile aggiornare la rete")
    await cb_next_hop(topic="/net/refresh/request", payload={
        "message":
            "Ricevuto {}#{} alle {}, e rinviato alle {}".format(
                header.get("name", "-missing-"),
                header.get("uuid", "-missing-"),
                header.get("ts", "-missing-"),
                dt.utcnow().__str__())})
