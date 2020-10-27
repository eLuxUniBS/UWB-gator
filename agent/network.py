import mqttools
from datetime import datetime as dt

from bson import ObjectId

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
    collect_node = dict()
    try:
        for net in orm.db.Net.objects.raw(dict(avaiable=True)):
            collect_node[net.name] = dict()
            for subnet in net.subnet:
                collect_node[net.name][subnet.name] = dict()
                obj_subnet = orm.db.SubNet.objects.get(dict(_id=subnet.pk))
                for node_id in obj_subnet.node_assigned:
                    node = orm.db.Node.objects.get(
                        dict(_id=ObjectId(node_id)))
                    collect_node[net.name][subnet.name][node.pk.__str__()] \
                        = node.to_dict()
    except Exception as e:
        print("Errore in DB", e)
    await cb_next_hop(topic="/net", payload=collect_node)


async def network_update(topic="", raw={}, header={}, payload={},
                         client: mqttools.Client = None,
                         cb_next_hop: MQTTAgent.publisher = None):
    if client is None:
        print("Impossibile aggiornare la rete")
    await cb_next_hop(topic="/net/refresh", payload={})
