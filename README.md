# Agenti MQTT

Ciascun agente √® dotato di uno specifico wrapper in cui inserire la propria funzione `cb` *callback* chiamata in base al topic scelto (con possibilit√† di inviare un messaggio a sua volta, su un nuovo topic specifico)

## Docs

Cartella per la documentazione ed utilizzo

## Architettura codice

### Agent_py

Contiene gli agenti scritti in python

### Agent_c

Contiene gli agenti scritti in C

## Docker

Contiene l'insieme di script per instanziare un sistema di raccolta dati (influxdb 1.8 e mongodb), con la possibilit√† di aggiungere agenti (nel file `lab_collect_data.yaml`)