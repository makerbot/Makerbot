int blinkdelay = 500; //This basically controls brightness. Lower is dimmer
int runspeed = 50;   //smaller = faster

int pad1 = 10;
int pad2 = 11;
int pad3 = 12;
int pad4 = 13;

const int ledMap[12][2] = {{pad4, pad3}, {pad3, pad4}, {pad4, pad1},
{pad1, pad4}, {pad4, pad2}, {pad2, pad4}, {pad2, pad3}, {pad3, pad2}, 
{pad2, pad1}, {pad1, pad2}, {pad3, pad1}, {pad1, pad3}};

void setup(){
  allOff();
  blinkall(2);
}


void loop() {
  
  for (int i = 0; i < 10; i++) {
    allOff();
    turnOn(i);
    delay(100);
    allOff();
  }
    
  for (int i = 11; i > 0 ; i--) {
    allOff();
    turnOn(i);
    delay(100);
    allOff();
  }
  
  
  for (int i = 0; i < 13; i++) {
    for (int k = 0; k < runspeed; k++) {
      for (int j = 0; j < i; j++) {
        turnOn(j);
        delayMicroseconds(blinkdelay);
        allOff();
      }
    }
  }
    
  for (int i = 0; i < 12; i++) {
    for (int k = 0; k < runspeed; k++) {
      for (int j = i; j < 12; j++) {
        turnOn(j);
        delayMicroseconds(blinkdelay);
        allOff();
      }
    }
  }
    
  
}


void turnOn(int led) {
  int highPin = ledMap[led][0];
  int lowPin = ledMap[led][1];
  pinMode(highPin, OUTPUT);
  pinMode(lowPin, OUTPUT);
  digitalWrite(highPin, HIGH);
  digitalWrite(lowPin, LOW);
}

void allOff() {
  PORTB = B00000000;
  DDRB = B00000000; 
}

void blinkall(int numblink) {
  allOff();
  for(int n = 0;n < numblink;n++)   {
    for(int i = 0; i < runspeed; i++)     {
      for(int j = 0; j < 12; j++)       {
        turnOn(j);
        delayMicroseconds(blinkdelay);
        allOff();
      }
    }
    delay(500);
  }
}
