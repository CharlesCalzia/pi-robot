# Pi Robot

## Hardware 

### Full materials list 

* Camera
* H-Bridge and 2 DC motors 
* Ultrasonic sensor 
* Battery/ power supply 
* Frame, wheels and front axle  
* Resistors: 1k and 2k for ultrasonic sensor

### Wiring
* Ultrasonic sensor (from sensor to Pi):
  * VCC : 5V 
  * GND : GND (ground) 
  * Trig : Pin 16 
  * Echo : Pin 18  (must be wired using potential divider with 330Ω and 470Ω resistors- wiring can be found online)

* Driving motors (from H-bridge to Pi):
  * Pin 1 : Pin 19
  * Pin 2 : Pin 11
  * Pin 3 : Pin 13
  * Pin 4 : Pin 15

* Power:
  * Select suitable power suppply for the Pi and motors
 
## Software

* Camera:
  * Uses motion software
  * Installed through: sudo apt-get install motion
 
* Main script:
  * See main_app.py and edit variable pi_ip to your Pi's IP address and port to your Pi's motion hosting port
  * Dependencies:
    * Flask: pip install Flask
    * RPi.GPIO: pip install RPi.GPIO
  * This will then create a flask web server which can be acessed through your host's ip address on any port (default port is 5000). This will then prompt for username and password: default username = admin, default password = admin123. These should be changed and this can easily be done.

## License and copyright

Copyright (c) Computing_
Licensed under the [MIT License](LICENSE)
