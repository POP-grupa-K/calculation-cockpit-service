# calculation-cockpit-service\
##Endpoints

###GET

####Taski
Panie, aby sobie pobrać taski o konkretnym statusie (np. "ongoing" i "created"), to robi się tak:
``
http://192.168.99.100:8006/cockpit/?s=ongoing,created
``

Natomiast, domyślnie są zwracane taski o statusie "created":

``
http://192.168.99.100:8006/cockpit/
``

