# Tema 3 SCD - Rares Dumitru Miculescu - 342C3

## Introducere

Tema include generare de informatii de la diverse dispozitive, care random dau informatii catre MQTT. Din MQTT sunt luate de catre un parser, care le adauga in InfluxDB, ca la final sa fie afisate in Grafana.

## Componente

mqtt : container-ul de mqtt, am folosit eclipse-mosquitto, a fost configurat pentru a folosi portul 1883 si a permite accesul anonim

IoT_payload : acesta este un feeder de date facut extra de mine, pentru a se putea genera random datele ce trebuie trimise catre mqtt. Acesta ia un numar random de payload-uri care sa fie trimise random intr-un timestamp, cu locatia random, numarul de componente random (si implicit componentele random), si valorile din ele (care pot fi random ori string ori numar). De asemenea trimiterea timestamp-ului e alesa random.

IoT_receiver : script in python care primeste toate mesajele date de feeder prin mqtt, filtreaza datele care sunt numerice, verifica daca avem timestamp (daca nu, adauga timestamp now()), ca apoi sa trimita json-ul catre InfluxDB

InfluxDB : baza de date unde se stocheaza informatia

Grafana : aplicatia de afisare a datelor

run.sh : script cu care am rulat / oprit swarm-ul

## Observatii

Am fost nevoit sa introduc feeder-ul in swarm, pentru ca mi sa parut cea mai buna alternativa ca simulator. 
Alte explicatii mai sunt drept comentarii in cod.
