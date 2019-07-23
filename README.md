# bt_to_mqtt

Une interface pour piloter une imprimante UV A700 avec un raspberry pi et un bouton

## Sur le raspberry pi

bt_to_mqtt.service
--> bt_to_mqtt.py

Quand appuie sur le bouton, envoie d'un message mqtt

## Sur le PC windows (avec le logiciel de RIP):

mqtt_sendkeys.py


###Installation sous windows:

TODO avec service
actuellement raccourci dasn le dossier démarrage
~\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
ligne de commande : "C:\Program Files (x86)\Python37-32\python.exe" c:\Applications\mqtt_Sendkeys\mqtt_sendkeys.py

###Installation sur le raspberry:

sudo systemctl enable /home/pi/mqtt_sendkeys/bt_to_mqtt.service
sudo systemctl start bt_to_mqtt.service
