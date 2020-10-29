import asyncio
import json, mqttools
import time
from uuid import uuid4
from datetime import datetime as dt


class MQTTAgent:
    """
    Permette di generare infiniti agenti, attivati su specifici topic (in subs e pubs) a cui è possibile asscoiare una specifica callback (cb)
    """

    def __init__(self, server, port, name="standard", manifest=dict, ):
        self.client_uuid = uuid4().__str__()
        self.client_name = name
        self.server = server
        self.port = int(port)
        self.subs_manifest = manifest.get("subs", dict())
        self.pubs_manifest = manifest.get("pubs", dict())

    async def start_client(self, resume_session=False):
        client = mqttools.Client(self.server, self.port, connect_delays=[0.1])
        await client.start(resume_session=resume_session)
        return client

    def generate(self):
        return self.generate_subscriber() + self.generate_publisher()

    def generate_subscriber(self):
        """
        Generazione di sottoscrittori tramite subs_manifest
        :param resume_session:
        :return:
        """
        buffer = []
        for k in self.subs_manifest.keys():
            print("SUBS", k)
            if self.subs_manifest.get(k).get("wrapper", None) is None:
                buffer.append(self.subscriber(input_topic=k,
                                              cb=self.subs_manifest.get(k).get(
                                                  "core")
                                              ))
        return buffer

    def generate_publisher(self):
        """

        :return:
        """
        buffer = []
        for k in self.pubs_manifest.keys():
            print("PUBS", k, self.pubs_manifest.get(k))
            cfg = self.pubs_manifest.get(k)
            buffer.append(self.publisher(
                topic=k,
                **cfg
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

            print(
                f'{dt.now()}[SUBS][{topic_content}] := {str(content.get("header", dict()))}')
            if cb is not None and topic_content is not None:
                try:
                    await cb(topic=topic_content, raw=content,
                             header=content.get("header", dict()),
                             payload=content.get("payload", dict()),
                             client=client, cb_next_hop=self.publisher)
                except Exception as e:
                    print(e)
                    print("CB ERRORE")

    async def publisher(self, topic: str = None,
                        header: dict = None,
                        payload=None,
                        retain=False,
                        loop=False,
                        wait_seconds=0.5):
        async def _loop_pubs():
            client= await self.start_client()
            while True:
                message["header"]["ts"] = dt.utcnow().__str__()
                print(f'{dt.now()}[PUBS][{topic}] := {str(header)}')
                client.publish(topic=topic,
                               message=json.dumps(message).encode('utf-8'),
                               retain=retain)
                time.sleep(wait_seconds)

        async def _single_pubs():
            client = await self.start_client()
            print(f'{dt.now()}[PUBS][{topic}] := {str(header)}')
            client.publish(topic=topic,
                           message=json.dumps(message).encode('utf-8'),
                           retain=retain)

        if topic is None:
            return None
        if header is None:
            header = dict(uuid=self.client_uuid,
                          name=self.client_name,
                          ts=dt.utcnow().__str__())
        message = dict(
            header=header,
            payload=payload if payload is not None else dict()
        )
        if loop:
            await _loop_pubs()
        else:
            await _single_pubs()
