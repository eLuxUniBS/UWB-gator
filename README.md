# Server ad agenti MQTT

Interfacciamento MQTT per DB 
- MongoDB
- InfluxDB

## Inizializzazione DB

Basta lanciare dalla cartella install, il file `initi_db.py`; i parametri dei
 nodi sono presenti nel file dataset.csv


## Suite di TEST

Basta lanciare la suite di test
`bash launch_test_script.sh [nome-del-file]`
dove al posto del nome-del-file si possono utilizzare i seguenti script

- test_direct.py per lanciare alcuni  pubs su /net e /geo
- test_agent.py per lanciare i subs su /net e /geo (basta modificare il
 manifest per aggiungere/rimuovere funzioni)


 