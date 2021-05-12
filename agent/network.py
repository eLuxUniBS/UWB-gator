import asyncio

import mqttools,json
from datetime import datetime as dt


from agent.skeleton import MQTTAgent, prepare_message
import orm


def pong(*args, **kwargs):
    print("PONG", args, "\n", kwargs)


def network_refresh(topic="/net", raw={}, header={}, payload={},
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
                    node = orm.db.Node.get_by_id(id=node_id)
                    collect_node[net.name][subnet.name][node.pk.__str__()] \
                        = node.to_dict()
    except Exception as e:
        print(__name__,"Errore in DB", e)
    client.publish(topic=topic, message=json.dumps(prepare_message(
            topic="/geo",payload=collect_node)).encode("UTF-8"))


def network_query(topic="", raw={}, header={}, payload={},
                        client: mqttools.Client = None,
                        cb_next_hop: MQTTAgent.publisher = None):
    if client is None:
        print("Impossibile aggiornare la rete")



async def standalone(topic_root="/net"):
    client = mqttools.Client(client_id="Network",host="127.0.0.1",port=10008)

    await client.start()
    await client.subscribe(topic=topic_root+'/#')

    while True:
        topic, message = await client.messages.get()
        topic=topic.strip()
        print("TOPIC", topic)
        if topic == topic_root:
            pong(**json.loads(message))
        elif topic == topic_root+"/ping":
            pong(**json.loads(message))
        elif topic == topic_root+"/refresh":
            network_refresh(client=client)
        elif topic == topic_root+"/update":
            network_query(**json.loads(message))
        elif topic.find(topic_root)!=-1:
            print("SIDE TOPIC",topic)
            print(message)


if __name__=="__main__":
    asyncio.run(standalone())