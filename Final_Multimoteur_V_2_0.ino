//*****************
//Gestion de translation motorisée unique
// 12/12/2025
//*****************

//librairie utilisée
#include <AccelStepper.h>
#define STEPPER AccelStepper::DRIVER

//Versionning a changer a chaque modification du code.
const String Version="Multimotor 3 axes V2.0 - 12-12-2025";

//******************
// changement de stratégie moteur : Appelé désormais X-Y-Z
// pour déclenchement de plusieurs moteur en même temps
//******************

//******************
//Liste des commandes : 
//ENABL_ : suivi du moteur à démarrer X1 Y1 Z1 ou éteindre X-1 Y-1 Z-1
//ACCEL_ : suivi du XValAccélération YValAccélération ZAccélération 
//SPEED_ : suivi de XValSpeed YValSpeed ZValSpeed
//DRIVE_ : suivi de XValdrive Yvaldrive Zvaldrive 
//STOP ou STOP_ : suivi de rien du tout ou de X1,Y1,Z1 pour arréter tout les moteurs ou seulement certain
//HOME_ : suivi de X1 ou Y1 ou Z1
//*******************


//pin moteur 
const int XPinEnable=2;
const int XPinDirection=3;
const int XPinPulse=4;

const int YPinEnable=5;
const int YPinDirection=6;
const int YPinPulse=7;

const int ZPinEnable=8;
const int ZPinDirection=9;
const int ZPinPulse=10;

int PinEnable[]={XPinEnable,YPinEnable,ZPinEnable};

//pin limitswitch
const int XPinLimitAvant=A0;
const int XPinLimitArriere=A1;

const int YPinLimitAvant=A2;
const int YPinLimitArriere=A3;

const int ZPinLimitAvant=A4;
const int ZPinLimitArriere=A5;

int LimitSwitchAvant[]={XPinLimitAvant,YPinLimitAvant,ZPinLimitAvant};
int LimitSwitchArriere[]={XPinLimitArriere,YPinLimitArriere,ZPinLimitArriere};

//défintion paramètre moteur
int VitesseMax=5000; 
int VitesseMin=100;
bool EnMarcheX=false;
bool EnMarcheY=false;
bool EnMarcheZ=false;

AccelStepper Moteur1(STEPPER,XPinPulse,XPinDirection);
AccelStepper Moteur2(STEPPER,YPinPulse,YPinDirection);
AccelStepper Moteur3(STEPPER,ZPinPulse,ZPinDirection);

//Variable nécessaire à la communication série 
int Separateur=-1; //permet de séparer la commande de l'ordre de commande 
 String Message ="";
 String Ordre ="";
 String Valeur ="" ; 
bool SensRotationCMD[]={true,true,true};
int AccelerationCMD[]={10000,10000,10000}; //Attribut de la commande d'accélération du système 
int SpeedCMD[]={1000,1000,1000};
int Nb_Cmd[]={0,0,0};
String MoteurSelectionner[]={"X","Y","Z"};




//fonction homing : demande à la platine de translation d'aller à la position avant
void GoHome(String Moteur){
  if (Moteur=="X"){
    Moteur1.setAcceleration(5000);
    Moteur1.setSpeed(VitesseMax);
    //Avance rapide jusqu'à butée 
    while (digitalRead(XPinLimitAvant)==true){
      Moteur1.move(-10);
      while(Moteur1.distanceToGo()>0){
        Moteur1.run();
      }
    }
    //Retour arrière pour sortir de la butée
    while (digitalRead(XPinLimitAvant)==false){
      Moteur1.move(10);
      while(Moteur1.distanceToGo()>0){
        Moteur1.run();
      }
    }
    //Recherche de la position butée faible vitesse
    Moteur1.setAcceleration(5000);
    Moteur1.setSpeed(VitesseMin);
    //Avance rapide jusqu'à butée 
    while (digitalRead(XPinLimitAvant)==true){
      Moteur1.move(-1);
      while(Moteur1.distanceToGo()>0){
        Moteur1.run();
      }
    }
    Moteur1.stop();
    Moteur1.setCurrentPosition(0);
    Serial.println("End Home");
  }
    if (Moteur=="Y"){
    Moteur2.setAcceleration(5000);
    Moteur2.setSpeed(VitesseMax);
    //Avance rapide jusqu'à butée 
    while (digitalRead(YPinLimitAvant)==true){
      Moteur2.move(-10);
      while(Moteur2.distanceToGo()>0){
        Moteur2.run();
      }
    }
    //Retour arrière pour sortir de la butée
    while (digitalRead(YPinLimitAvant)==false){
      Moteur2.move(10);
      while(Moteur2.distanceToGo()>0){
        Moteur2.run();
      }
    }
    //Recherche de la position butée faible vitesse
    Moteur2.setAcceleration(5000);
    Moteur2.setSpeed(VitesseMin);
    //Avance rapide jusqu'à butée 
    while (digitalRead(YPinLimitAvant)==true){
      Moteur2.move(-1);
      while(Moteur2.distanceToGo()>0){
        Moteur2.run();
      }
    }
    Moteur2.stop();
    Moteur2.setCurrentPosition(0);
    Serial.println("End Home");
  }
    if (Moteur=="Z"){
    Moteur3.setAcceleration(5000);
    Moteur3.setSpeed(VitesseMax);
    //Avance rapide jusqu'à butée 
    while (digitalRead(ZPinLimitAvant)==true){
      Moteur3.move(-10);
      while(Moteur3.distanceToGo()>0){
        Moteur3.run();
      }
    }
    //Retour arrière pour sortir de la butée
    while (digitalRead(ZPinLimitAvant)==false){
      Moteur3.move(10);
      while(Moteur3.distanceToGo()>0){
        Moteur3.run();
      }
    }
    //Recherche de la position butée faible vitesse
    Moteur3.setAcceleration(5000);
    Moteur3.setSpeed(VitesseMin);
    //Avance rapide jusqu'à butée 
    while (digitalRead(ZPinLimitAvant)==true){
      Moteur3.move(-1);
      while(Moteur3.distanceToGo()>0){
        Moteur3.run();
      }
    }
    Moteur3.stop();
    Moteur3.setCurrentPosition(0);
    Serial.println("End Home");
  }
  }
  







//Programme de Lecture du port série
// Toute les commande sont écrites sous la forme : CMD_Val

void Recuperation_Valeur (String PartieValeur){
  Nb_Cmd[0]=0;
  Nb_Cmd[1]=0;
  Nb_Cmd[2]=0;
 // Extrait X
  int posX = PartieValeur.indexOf('X');
  if (posX != -1) {
    int posY = PartieValeur.indexOf('Y', posX);
    if (posY != -1) {
      Nb_Cmd[0] = PartieValeur.substring(posX + 1, posY).toInt();
      } else {
        Nb_Cmd[0] = PartieValeur.substring(posX + 1).toInt();
      }
    }
  // Extrait Y
  int posY = PartieValeur.indexOf('Y');
  if (posY != -1) {
    int posZ = PartieValeur.indexOf('Z', posY);
    if (posZ != -1) {
      Nb_Cmd[1] = PartieValeur.substring(posY + 1, posZ).toInt();
      } else {
      Nb_Cmd[1] = PartieValeur.substring(posY + 1).toInt();
      }
    }
    // Extrait Z
    int posZ = PartieValeur.indexOf('Z');
    if (posZ != -1) {
      Nb_Cmd[2] = PartieValeur.substring(posZ + 1).toInt();
      }
}

void Lecture(){
  while (Serial.available()>0){
    Message=Serial.readStringUntil('\n');
    Message.trim();
    delay(15);
    Serial.println(Message);
  }
  //Cas d'une commande ENABL:
  if (Message.startsWith("ENABL_")) {
      String Valeurs = Message.substring(6);
      Recuperation_Valeur(Valeurs);
      Serial.println(Nb_Cmd[0]+ " " +Nb_Cmd[1]);
      for (int i=0; i<=2 ; i++) {
        switch (Nb_Cmd[i]) {
          case -1 : 
            digitalWrite(PinEnable[i],HIGH);
            Serial.println(MoteurSelectionner[i]+" OFF");
            break;
          case 1 :
            digitalWrite(PinEnable[i],LOW);
            Serial.println(MoteurSelectionner[i]+" ON");
            break;
        }
      }
  } else {
  //Cas d'une commande ACCEL:
  if (Message.startsWith("ACCEL_")){
    String Valeurs = Message.substring(6);
    Recuperation_Valeur(Valeurs);
    if (Nb_Cmd[0]!=0){
      Moteur1.setAcceleration(Nb_Cmd[0]);
      Serial.println("X VALID ACCEL = " + Nb_Cmd[0]);
    }
    if (Nb_Cmd[1]!=0){
      Moteur2.setAcceleration(Nb_Cmd[1]);
      Serial.println("Y VALID ACCEL = " + Nb_Cmd[1]);
    }
    if (Nb_Cmd[2]!=0){
      Moteur3.setAcceleration(Nb_Cmd[2]);
      Serial.println("Z VALID ACCEL = " + Nb_Cmd[2]);
    }
  } else {
  //Cas d'une commande SPEED
  if (Message.startsWith("SPEED_")){
    String Valeurs = Message.substring(6);
    Recuperation_Valeur(Valeurs);
    if (Nb_Cmd[0]!=0){
      Moteur1.setMaxSpeed(Nb_Cmd[0]);
      Serial.println("X VALID SPEED = " + Nb_Cmd[0]);
    }
    if (Nb_Cmd[1]!=0){
      Moteur2.setMaxSpeed(Nb_Cmd[1]);
      Serial.println("Y VALID SPEED = " + Nb_Cmd[1]);
    }
    if (Nb_Cmd[2]!=0){
      Moteur3.setMaxSpeed(Nb_Cmd[2]);
      Serial.println("Z VALID SPEED = " + Nb_Cmd[2]);
    }
  } else {
  //Cas d'une commande DRIVE
  if (Message.startsWith("DRIVE_")){
    String Valeurs = Message.substring(6);
    Recuperation_Valeur(Valeurs);
    if (Nb_Cmd[0]!=0){
      if (Nb_Cmd[0]<0){
        SensRotationCMD[0]=false;
      }else{SensRotationCMD[0]=true;}
      Moteur1.move(Nb_Cmd[0]);
      EnMarcheX=true;
      Serial.println("X VALID DRIVE = " + Nb_Cmd[0]);
    }
    if (Nb_Cmd[1]!=0){
      if (Nb_Cmd[1]<0){
        SensRotationCMD[1]=false;
      }else{SensRotationCMD[1]=true;}
      Moteur2.move(Nb_Cmd[1]);
      EnMarcheY=true;
      Serial.println("Y VALID DRIVE = " + Nb_Cmd[1]);
    }
    if (Nb_Cmd[2]!=0){
      if (Nb_Cmd[2]<0){
        SensRotationCMD[2]=false;
      }else{SensRotationCMD[2]=true;}
      Moteur3.move(Nb_Cmd[2]);
      EnMarcheZ=true;
      Serial.println("Z VALID DRIVE = " + Nb_Cmd[2]);
    }
  } else {
  //Cas d'une commande STOP
  if (Message.startsWith("STOP")){
    if (Message.indexOf("_")==-1){
      Nb_Cmd[0]=1;
      Nb_Cmd[1]=1;
      Nb_Cmd[2]=1;
    } else{
      String Valeurs = Message.substring(5);
      Recuperation_Valeur(Valeurs);
    }
    if (Nb_Cmd[0]!=0){
      Moteur1.stop();
      EnMarcheX=false;
      Serial.println("X VALID STOP");
    }
    if (Nb_Cmd[1]!=0){
      Moteur2.stop();
      EnMarcheY=false;
      Serial.println("Y VALID STOP");
    } 
    if (Nb_Cmd[2]!=0){
      Moteur3.stop();
      EnMarcheZ=false;
      Serial.println("Z VALID STOP");
    }
  } else {
  //Cas d'une commande HOME_
  if (Message.startsWith("HOME_")){
    String Valeurs = Message.substring(5);
    Recuperation_Valeur(Valeurs);
    for (int i=0; i<=2; i++ ){
      if (Nb_Cmd[i]!=0){
        Serial.println(MoteurSelectionner[i] + " START HOMING");
        GoHome(MoteurSelectionner[i]);
      }
    }
  }
}}}}}
  Message="";
}




void setup() {
  //Définition des pins limits
  pinMode(XPinLimitAvant,INPUT_PULLUP);
  pinMode(XPinLimitArriere,INPUT_PULLUP);
  pinMode(YPinLimitAvant,INPUT_PULLUP);
  pinMode(YPinLimitArriere,INPUT_PULLUP);
  pinMode(ZPinLimitAvant,INPUT_PULLUP);
  pinMode(ZPinLimitArriere,INPUT_PULLUP);
  
  //Définition des pins ENABLE Moteur
  pinMode(XPinEnable,OUTPUT);
  digitalWrite(XPinEnable,HIGH);
  pinMode(YPinEnable,OUTPUT);
  digitalWrite(YPinEnable,HIGH);
  pinMode(ZPinEnable,OUTPUT);
  digitalWrite(ZPinEnable,HIGH);

  //Port série définition
  Serial.begin(9600);
  delay(1000);
  //Définition entrée série 
  Message="";

  //Définition Entrée Moteur de base
  Moteur1.setMaxSpeed(SpeedCMD[0]);
  Moteur1.setAcceleration(AccelerationCMD[0]);
  Moteur1.setCurrentPosition(0);
  Moteur2.setMaxSpeed(SpeedCMD[1]);
  Moteur2.setAcceleration(AccelerationCMD[1]);
  Moteur2.setCurrentPosition(0);
  Moteur3.setMaxSpeed(SpeedCMD[2]);
  Moteur3.setAcceleration(AccelerationCMD[2]);
  Moteur3.setCurrentPosition(0);
}


void loop() {
 //Vérification de lecture d'une entrée
  Lecture();
 //Cas moteur 1 en marche
  if ((EnMarcheX==true && SensRotationCMD[0]==false && digitalRead(XPinLimitArriere)==false)||(EnMarcheX==true && SensRotationCMD[0]==true && digitalRead(XPinLimitAvant)==false)){
    Serial.print("X Butée rencontrée / reste : ");
    Serial.println(Moteur1.distanceToGo());
    Moteur1.stop();
    EnMarcheX=false;
  }
  if (EnMarcheX==true){
    Moteur1.run();
    if (Moteur1.distanceToGo()==0){
      EnMarcheX=false;
      Moteur1.stop();
      Serial.println("X End Move");
    }
  }
  //Cas moteur 2 en marche 
  if ((EnMarcheY==true && SensRotationCMD[1]==false && digitalRead(YPinLimitArriere)==false)||(EnMarcheY==true && SensRotationCMD[1]==true && digitalRead(YPinLimitAvant)==false)){
    Serial.print("Y Butée rencontrée / reste : ");
    Serial.println(Moteur2.distanceToGo());
    Moteur2.stop();
    EnMarcheY=false;
  }
  if (EnMarcheY==true){
    Moteur2.run();
    if (Moteur2.distanceToGo()==0){
      EnMarcheY=false;
      Moteur2.stop();
      Serial.println("Y End Move");
    }
  //Cas moteur 3 en marche 
  if ((EnMarcheZ==true && SensRotationCMD[2]==false && digitalRead(ZPinLimitArriere)==false)||(EnMarcheZ==true && SensRotationCMD[2]==true && digitalRead(ZPinLimitAvant)==false)){
    Serial.print("Z Butée rencontrée / reste : ");
    Serial.println(Moteur3.distanceToGo());
    Moteur3.stop();
    EnMarcheZ=false;
  }
  if (EnMarcheZ==true){
    Moteur3.run();
    if (Moteur3.distanceToGo()==0){
      EnMarcheZ=false;
      Moteur3.stop();
      Serial.println("Z End Move");
    }
  }
  }
}
    

