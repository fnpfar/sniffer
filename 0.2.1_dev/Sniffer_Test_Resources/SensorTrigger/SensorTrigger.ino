
/*************************************
   VERISURE SENSOR TRIGGER & SEQUENCER
 * ***********************************
   This program allows to trigger Verisure
   sensors by switching it's power supply
   in a controlled sequenced way.
   Written by Francisco N. Pérez for
   testing the Verisure Multichannel
   Sniffer. May-2022
*/

/*
   Sensor numeration:
   0 -> 2BE5 FXNU (Old installation)
   1 -> 2D6G HKRD (New installation)
   2 -> 2D68 A6XX (New installation)
*/
static int sensorsActivationPin[] = {22, 24, 28};

/*
   Triggers a group of sensors. 
   This function is blocking until all sensors have been 
   triggered.
*/
void sendFrameOnSensor(int *sensorNums) {
  for(int i = 0; i < sizeof(sensorNums); i++){
    digitalWrite(sensorsActivationPin[(*(sensorNums + i))], HIGH);
    delay(10);
  }
  delay(1700);
  for(int i = 0; i < sizeof(sensorNums); i++){
    digitalWrite(sensorsActivationPin[(*(sensorNums + i))], LOW);
    delay(10);
  }
  delay(100);
}

/*
   GPIO config. & initialization
*/
void gpioConfig() {
  for (int i = 0; i < sizeof(sensorsActivationPin); i++) {
    pinMode(sensorsActivationPin[i], OUTPUT);
    digitalWrite(sensorsActivationPin[i], LOW);
  }
}

/*
   Setup function (Start of execution)
*/
void setup() {
  gpioConfig();
  int group1[] = {0,2};
  int group2[] = {1};
  for (int i = 0; i < 100; i++) {
    sendFrameOnSensor(group1);
    sendFrameOnSensor(group2);
  }
}

/*
   Main loop
*/
void loop() {
}
