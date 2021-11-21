---
```
Attenzione, questa parte è in fase di revisione. Considerare solamente la wiki allegata alla repo.
```
---
# Come fare una rilevazione con il firmware UniTN

Sia emittitore che ricevente devono poter accedere al broker. -p e -i permettono di impostare porta ed indirizzo ip del broker.

## Servizio Emittitore

```bash
python3 main.py -m pub_serial -sp /dev/serial/by-idusb-SEGGER_J-Link_000760029246-if00 -wb 0 -wa 2
```

Dove

- ```-m pub_serial``` modalità pubbicazione da seriale
- ```-sp``` indirizzo dispositivo seriale collegato
- ```-wb``` secondi di attesa prima di ascoltare la seriale
- ```-wa``` secondi di attesa dopo aver ascoltato la seriale ed inviato il messaggio su mqtt 


I secondi di attesa appartengono al renge [0,inf.[

## Servizio Ricevente

```bash
python3 main.py -m sub_db_unrel_serial
```

Dove ```-m sub_db_unrel_serial``` modalità ricezione su mongodb di messaggi seriali. Se la callback usata nel parsing del messaggio seriale, ritorna un valore 
```python
detected=True
```
allora verrà salvato in una collection specifica (oltre ad esser salvato nella collezione raw).


# Demo

## Dispositivo body
- wifi accesspoint
```bash
python3 -m agent_py --mode pub_raspi_gpio
```
```bash
python3 -m agent_py --mode repeater_gpio_to_net
```
## Dispositivo estremità
```bash
python3 -m agent_py --mode pub_raspi_gpio
```

## Dispositivo gpio

Ogni volta che riceve un messaggio con topic dedicato al gpio, aggiorna i gpio

```bash
python3 -m agent_py --mode sub_raspi_gpio
```
