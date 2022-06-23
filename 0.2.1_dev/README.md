## GNU Radio Safety Sniffer for Verisure

---

**Contents of this repository:**

1. Multichannel Safety Sniffer GRC flowgraph (in "GRC Multichannel Sniffer" folder).
2. GRC examples & tests (in "GRC Tests and Examples" folder).
3. Additional non-GRC test resources (in "Sniffer_Test_Resources" folder).

Note: When checking out a commit with .grc files instantiating hierarchical blocks,
in order for them to work properly each one should be regenerated. This is done by
opening the .grc file of the hier. block and executing the flowgraph (play button).
Then, on the main .grc flowgraph run the "reload blocks" option marked with a 
circular arrow on the main bar. This should be done because GRC hierarchical blocks
are saved by default on the .grc_gnuradio folder inside the user directory. If these
files are moved to the main .grc file directory, then they will be lauched from there
but when updating/regenerating them, their changes will be saved on the .grc_gnuradio
directory.


---
