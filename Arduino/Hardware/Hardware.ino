#include <robo_hardware2.h>
#include <ros.h>
#include <std_msgs/Int32MultiArray.h>
#include <byakugan/RefletanciaMsg.h>

byakugan::RefletanciaMsg dataRefletancia;
ros::Publisher pubRefletancia("refletancia", &dataRefletancia);

ros::NodeHandle nh;

#define LED_SERVO1 2
#define LED_SERVO2 3

void motoresCb(const std_msgs::Int32MultiArray &motores){
  //robo.acionarMotores(motores.data[0], motores.data[1]);
  int velEsq = motores.data[0];
  int velDir = motores.data[1];

  if (velEsq > 0) {
    digitalWrite(LED_SERVO1, 1);
  } else {
    digitalWrite(LED_SERVO1, 0);
  }

  if (velDir > 0) {
    digitalWrite(LED_SERVO2, 1);
  } else {
    digitalWrite(LED_SERVO2, 0);
  }

  /*
  if (abs(motores.data[0]) > 0) {
    digitalWrite(LED_BUILTIN, 1);
  } else if abs {
    digitalWrite(LED_BUILTIN, 0);
  }*/
}
ros::Subscriber<std_msgs::Int32MultiArray> subMotores("ctrl_motores", &motoresCb);

/*

void garraCb(const std_msgs::Int32MultiArray &garra){
  //robo.acionarServoGarra1(garra.data[0]);
  //robo.acionarServoGarra2(garra.data[1]);
  if (abs(garra.data[1]) > 0) {
    digitalWrite(LED_SERVO1, 1);
  } else if (abs(garra.data[1]) >= 80){
    digitalWrite(LED_SERVO1, 0);
  }
}

ros::Subscriber<std_msgs::Int32MultiArray> subGarras("ctrl_garras", &garraCb);
*/


void setup() {

  nh.getHardware()->setBaud(115200);
  nh.initNode();

  //pinMode(LED_BUILTIN, OUTPUT);

  pinMode(LED_SERVO1, OUTPUT);
  pinMode(LED_SERVO2, OUTPUT);

  nh.subscribe(subMotores);
  //nh.subscribe(subGarras);

  nh.advertise(pubRefletancia);

  //robo.configurar(true);
  //robo.habilitaTCS34();
}

void loop() {
  nh.spinOnce();
}
