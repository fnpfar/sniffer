Veriure SDR Safety Multichannel Sniffer
=======================================
Installation and User Guide

## Version history:

	* 0.2.1 (23/06/2022) Added a configuration file supporting LatAm S4 & S5 channels.
	* 0.2.0 (31/05/2022) Implemented 4-GFSK demodulation capability for Europe channels
						 and given support to LatAm channel configurations.
						 Provided a file suporting Latam S1, S2 & S3 channels.
	* 0.1.0 (19/04/2022)

## Description:
	
	This software allows its user to employ the hardware SDR interface "HackRF One" as a frame
	sniffer on the "Safety" and "High Speed" channels of the Verisure radio protocol. In order 
	to do this, it enables a TCP server which accepts connections from multiple simultaneous 
	clients (e.g. Rf Analyzer) sending them the captured frames, in addition to representing 
	statistics and radio parameters through the terminal.

## Characteristics:

	* Simultaneous capture of the 5 "Safety" channels and the 4 "High Speed" channels (Europe)
	* Simultaneous capture of the first 3 "Safety" channels and the HS100-200 "High Speed" channel (LatAm)
	* Simultaneous capture of the last 2 "Safety" channels (4 & 5)(LatAm)
	* The captures can be retrieved by multiple clients (e.g. RfAnalyzer) simultaneously.
	* Features five 2-GFSK and one 4-GFSK radio-to-Verisure frame receivers.
	* Support for multiple configurations e.g. Europe, LatAm interchangeable from the config. file
	* Supported on Ubuntu 20.04 and Windows 10 (using GNU Radio 3.9.x/3.10.x and Python 3.8.x).

## Installation and running [Ubuntu 20.04]
   
	1. Run in the terminal:
		sudo add-apt-repository ppa:gnuradio/gnuradio-releases-3.9
		sudo apt-get update
		sudo apt-get install gnuradio python3-packaging		
	2. Connect the "HackRF One" interface to an USB port.
	3. Unzip the distribution file into a directory. Open a terminal inside it and run:
		python3 multichannelSniffer.py
	4. In order to close the server press Enter or Ctrl + C.
	   It is possible to change the server ipv4 address or port by editing the 
	   "multichannelSnifferConfig.conf" file.

## Installation and running [Windows 10]

    1. Download the "radioconda" Windows GUI installer available at the "download" section:
	    https://github.com/ryanvolz/radioconda
	2. Run and install.
	3. The "radioconda" directory will appear on the Windows Start menu. Inside, you have access 
       to the terminal "Conda Prompt", where the sniffer will be executed.
	4. Unzip the distribution file on a directory and access it using the said prompt:
		cd <path of the uncompressed file>
	5. Connect the "HackRF One" interface to an USB port and run the server:
		python multichannelSniffer.py
	6. In order to close the server press Enter or Ctrl + C.
	   It is possible to change the server ipv4 address or port by editing the 
	   "multichannelSnifferConfig.conf" file.
	   
	   In case the server does not recognize the HackRF interface, its driver (WinUSB) can be 
	   manually installed using "Zadig". Follow the instructions at:
	   https://github.com/ryanvolz/radioconda#installing-the-winusb-driver-with-zadig

## Configuration files (Switching between EU and LatAm) [Ubuntu 20.04 & Windows 10]
	   
	This multichannel sniffer instantiates five 2-GFSK and one 4-GFSK radio-to-Verisure frame receivers.
	All of these receivers can be enabled or disabled and configured in order to implement the reception
	of different sets of Verisure channels. For that purpose, two INI configuration files should be present
	in the same directory as the Sniffer executable "multichannelSniffer.py": first, 
	"multichannelSnifferConfig.conf" sets the TCP server socket adress and port, frame loging and decoding
	options and the channels configuration file to load. This second configuration file establishes all the
	parameters for the SDR hardware in use (HackRF) and for the available SW receivers, including which ones
	to enable and their radio settings from the Verisure Radio Protolocol Specification. Therefore, changing
	this file allows the user to load different HW and channel sets which wouldn't be possible to receive
	simultaneously due to hardware bandwidth limitations (like Europe and LatAm configurations).
	Finally, three of these channel configuration files are provided: one for the Europe "Safety" (5 channels) 
	and "High Speed" (4 channels) bands: "multichannelSnifferConfigEurope.conf", other for the LatAm 
	"Safety" (channels 1,2,3) and "High Speed" bands: multichannelSnifferConfigLatAmGroup1.conf and another
	for the LatAm "Safety" (channels 4,5): multichannelSnifferConfigLatAmGroup2.conf. Note that in the Europe 
	configuration file, "High Speed" channels HS200, HS600 and HS800 are disabled in order to save CPU 
	resources, but they can be enabled in the [4GFSK_CHANNELS] section.

## About:

	This software has been developed in the Securitas Direct/Verisure university-company chair by Francisco 
	Nicolás Pérez Fernández under the supervision and collaboration of Diego Herranz Lázaro. In addition, 
	Carlos Gonzalo Peces contributed providing relevant information about the decoding of the channels not 
	present at the moment of development in the Verisure Radio Protocol, and Alvaro Araujo Pinto conducted 
	the Sprint workflow methodology as Scrum Master. Although its operation has been tested, this is an alpha 
	version and the capture of the totality of radiated frames in the vicinity of the radio interface is not 
	guaranteed.







	
