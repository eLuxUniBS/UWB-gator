import json, mqttools
from uuid import uuid4
from datetime import datetime as dt


class MQTTAgent:
    """
    Permette di generare infiniti agenti, attivati su specifici topic (in subs e pubs) a cui è possibile asscoiare una specifica callback (cb)
    """

    def __init__(self, server, port, name="standard", manifest={}):
        self.client_uuid = uuid4().__str__()
        self.client_name = name
        self.server = server
        self.port = int(port)
        self.manifest = manifest

    async def start_client(self, resume_session=False):
        client = mqttools.Client(self.server, self.port, connect_delays=[0.1])
        await client.start(resume_session=resume_session)
        return client

    def generate_subscriber(self):
        """
        Generazione di sottoscrittori tramite manifest
        :param resume_session:
        :return:
        """
        buffer = []
        for k in self.manifest.keys():
            buffer.append(self.subscriber(input_topic=k,
                                          cb=self.manifest.get(k)
                                          ))
        return buffer

    async def subscriber(self, input_topic=None, cb=None):
        """
        Creazione singolo sottoscrittore
        :param topic:
        :param cb:
        :return:
        """
        client = await self.start_client()
        await client.subscribe(topic=input_topic)
        print("SUBS", input_topic)
        while True:
            topic_content, byte_content = await client.messages.get()
            if byte_content is None:
                continue
            try:
                content = json.loads(byte_content.decode('utf-8'))
            except Exception as e:
                print("Errore in codifica messaggio")
                print(byte_content)
                print(e)
                continue

            print(f'{dt.now()}[SUBS][{topic_content}] := {str(content)[:100]}')
            if cb is not None and topic_content is not None:
                try:
                    await cb(topic=topic_content, raw=content,
                             header=content.get("header", dict()),
                             payload=content.get("payload", dict()),
                             client=client, cb_next_hop=self.publisher)
                except Exception as e:
                    print(e)
                    print("CB ERRORE")
                except:
                    print("CB ERRORE EMPTY")

    async def publisher(self, topic: str = None, header: dict = None,
                        payload={},
                        retain=False):
        if topic is None:
            return None
        if header is None:
            header = dict(uuid=self.client_uuid,
                          name=self.client_name,
                          ts=dt.utcnow().__str__())
        message = json.dumps(
            dict(
                header=header,
                payload=payload
            )
        ).encode('utf-8')
        client = await self.start_client()
        await client.subscribe(topic=topic)
        print(f'{dt.now()}[PUBS][{topic}] := {str(message)[:100]}')
        client.publish(topic=topic,
                       message=message,
                       retain=retain)
