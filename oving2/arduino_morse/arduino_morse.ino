#include <SoftwareSerial.h>

// 0 = DOT
// 1 = DASH
// 2 = SHORT PAUSE
// 3 = MEDIUM PAUSE
// 4 = LONG PAUSE

//Button pressed     = 0
//Button not pressed = 1

const int buttonPin = 7;
const int ledPin1 = 6;
const int ledPin2 = 5;
const int ledPin3 = 4;
const int ledPin4 = 3;
const int ledPin5 = 2;
const int timeInterval = 500;

int buttonState = 1; //Button is currently not pressed
int lastButtonState = 1;
long timeChanged = millis();
long timeSinceChange = 0;


void setup() {
  Serial.begin(9600);
  pinMode(buttonPin, INPUT);
  pinMode(ledPin1, OUTPUT);
  pinMode(ledPin2, OUTPUT);
  pinMode(ledPin3, OUTPUT);
  pinMode(ledPin4, OUTPUT);
  pinMode(ledPin5, OUTPUT);
}



void loop() {
  buttonState = digitalRead(buttonPin);
  if(buttonState != lastButtonState){
    delay(7);
    buttonState = digitalRead(buttonPin);
    if(buttonState != lastButtonState){
      if(buttonState == 0){ //Button is currently pressed
        if(timeSinceChange >= 20*timeInterval){
          Serial.print(5);
        }
        else if(timeSinceChange >= 10*timeInterval){
          Serial.print(4);
        }
        else if(timeSinceChange >= 7*timeInterval){
          Serial.print(3);
        }
        else if(timeSinceChange >= 3*timeInterval){
          Serial.print(2);
        }
      }
      else{//Button is currently not pressed
        if(timeSinceChange >= 3*timeInterval){
          Serial.print(1);
        }
        else if(timeSinceChange >= timeInterval){
          Serial.print(0);
        }
      }
      timeChanged = millis();
      
    }
  }
  
  
  timeSinceChange = millis() - timeChanged;
  if(timeSinceChange >= timeInterval){
    digitalWrite(ledPin2, HIGH);
  }
  else{
    digitalWrite(ledPin2, LOW);
  }
  
  if(timeSinceChange >= 3*timeInterval){
    digitalWrite(ledPin3, HIGH);
  }
  else{
    digitalWrite(ledPin3, LOW);
  }

  if(timeSinceChange >= 7*timeInterval && buttonState == 1){
    digitalWrite(ledPin4, HIGH);
  }
  else{
    digitalWrite(ledPin4, LOW);
  }
  
  if(timeSinceChange >= 10*timeInterval && buttonState == 1){
    digitalWrite(ledPin5, HIGH);
  }
  else{
    digitalWrite(ledPin5, LOW);
  }

  if(buttonState == 0 || timeSinceChange >= 20*timeInterval){
    digitalWrite(ledPin1, HIGH);
  }
  else{
    digitalWrite(ledPin1, LOW);
  }
  
  lastButtonState = buttonState;
  
}
