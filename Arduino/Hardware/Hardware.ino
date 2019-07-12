
#include <robo_hardware2.h>
#include <ros.h>
#include "ByakuganHardware.h"
#include <std_msgs/Int32MultiArray.h>
#include <byakugan/RefletanciaMsg.h>
#include <byakugan/BotoesMsg.h>
#include <byakugan/SensoresDistanciaMsg.h>


ros::NodeHandle_<ByakuganHardware> nh;


byakugan::RefletanciaMsg dataRefletancia;
ros::Publisher pubRefletancia("refletancia", &dataRefletancia);

byakugan::SensoresDistanciaMsg dataSonares;
ros::Publisher pubSonares("distancia", &dataSonares);

byakugan::BotoesMsg dataBotoes;
ros::Publisher pubBotoes("botoes", &dataBotoes);
/*
std_msgs::Float64MultiArray dataSensoresCor;
ros::Publisher pubSensoresCor("cor", &dataSensoresCor);


byakugan::PosicaoMsg dataPosicao;
ros::Publisher pubPosicao("posicao", &dataPosicao)
*/

void motoresCb(const std_msgs::Int32MultiArray &motores){
  robo.acionarMotores(motores.data[0], motores.data[1]);
}
ros::Subscriber<std_msgs::Int32MultiArray> subMotores("ctrl_motores", &motoresCb);

void garraCb(const std_msgs::Int32MultiArray &garra){
  robo.acionarServoGarra1(garra.data[0]);
  robo.acionarServoGarra2(garra.data[1]);
}
ros::Subscriber<std_msgs::Int32MultiArray> subGarras("ctrl_garras", &garraCb);


void setup() {
  nh.getHardware();
  nh.initNode();
  
  nh.subscribe(subMotores);
  nh.subscribe(subGarras);

  nh.advertise(pubRefletancia);
  nh.advertise(pubSonares);
  nh.advertise(pubBotoes);
  //nh.advertise(pubSensoresCor);

  robo.configurar(true);

  //robo.habilitaTCS34();
}

void loop() {
  dataRefletancia.refletancia[0] = robo.lerSensorLinhaMaisEsqSemRuido();
  dataRefletancia.refletancia[1] = robo.lerSensorLinhaEsqSemRuido();
  dataRefletancia.refletancia[2] = robo.lerSensorLinhaDirSemRuido();
  dataRefletancia.refletancia[3] = robo.lerSensorLinhaMaisDirSemRuido();

  dataSonares.sensoresDistancia[0] = robo.lerSensorSonarFrontal();
  dataSonares.sensoresDistancia[1] = robo.lerSensorSonarDir();
  dataSonares.sensoresDistancia[2] = robo.lerSensorSonarEsq();
 /*
  dataSensoresCor.data[0] = robo.getHSVEsquerdo().h;
  dataSensoresCor.data[1] = robo.getHSVEsquerdo().s;
  dataSensoresCor.data[2] = robo.getHSVEsquerdo().v;
 */
  dataBotoes.botao1.data = robo.botao1Pressionado();
  dataBotoes.botao2.data = robo.botao2Pressionado();
  dataBotoes.botao3.data = robo.botao3Pressionado();
  
  pubRefletancia.publish(&dataRefletancia);
  pubSonares.publish(&dataSonares);
  pubBotoes.publish(&dataBotoes);
  //pubSensoresCor.publish(&dataSensoresCor);

  nh.spinOnce();
}
