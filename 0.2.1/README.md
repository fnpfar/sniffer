## Veriure SDR Safety Multichannel Sniffer

**Description:**

This software allows its user to employ the hardware SDR interface "HackRF One" as a frame
sniffer on the "Safety" and "High Speed" channels of the Verisure radio protocol. In order 
to do this, it enables a TCP server which accepts connections from multiple simultaneous 
clients (e.g. Rf Analyzer) sending them the captured frames, in addition to representing 
statistics and radio parameters through the terminal.

---

**Contents of this branch:**

This branch includes all of the releases containing each one both all the python and config. 
files needed for executing the sniffer and the user documentation). For the develoment files,
test and examples see the development branch. 

---

**Installation & user guide:**

For installation and user guide of the current release, see Installation_and_UserGuide.md

---

**About:**

This software has been developed in the Securitas Direct/Verisure university-company chair
by Francisco Nicolás Pérez Fernández under the supervision and collaboration of Diego Herranz
Lázaro. In addition, Carlos Gonzalo Peces contributed providing relevant information about
the decoding of the channels not present at the moment of development in the Verisure Radio
Protocol, and Alvaro Araujo Pinto conducted the Sprint workflow methodology as Scrum Master.

