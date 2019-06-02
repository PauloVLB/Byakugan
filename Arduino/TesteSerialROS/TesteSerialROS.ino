#include <Servo.h>

Servo servo;

#define TIMEOUT 3

float tAtual, tAntes; 
bool timeOut = false;

void setup() {
  Serial.begin(9600);
  servo.attach(9);  
}

void loop() {
  float angulo = getAngulo();
  
  servo.write(angulo);
}

float getAngulo(){
  Serial.print('.');
  
  bool recebeu = false;
  
  tAntes = millis();
  while(Serial.available() < 0 && !timeOut){
        tAtual = millis();
        timeOut = (tAtual - tAntes) > TIMEOUT;
        if(!timeOut) recebeu = true;
  }
  if(recebeu){
    return Serial.parseInt();
  }else{
    Serial.read();
    return servo.read();
  }
}

