//*****************
//Gestion de translation motorisée unique
// 04/10/2025
//*****************

//librairie utilisée
#include <AccelStepper.h>
#define STEPPER AccelStepper::DRIVER

//Versionning a changer a chaque modification du code.
const String Version="Multimotor 3 axes V1.2 - 12-10-2025";

//pin moteur 
const int M1PinEnable=2;
const int M1PinDirection=3;
const int M1PinPulse=4;

const int M2PinEnable=5;
const int M2PinDirection=6;
const int M2PinPulse=7;

const int M3PinEnable=8;
const int M3PinDirection=9;
const int M3PinPulse=10;

//pin limitswitch
const int M1PinLimitAvant=A0;
const int M1PinLimitArriere=A1;

const int M2PinLimitAvant=A2;
const int M2PinLimitArriere=A3;

const int M3PinLimitAvant=A4;
const int M3PinLimitArriere=A5;

int LimitSwitchAvant[]={M1PinLimitAvant,M2PinLimitAvant,M3PinLimitAvant};
int LimitSwitchArriere[]={M1PinLimitArriere,M2PinLimitArriere,M3PinLimitArriere};
//pin Opto :
  //const int PinOptoM1=A0;
  //int ValeurOptoM1=0;
  //const int PinOptoM1Bis=A1;
  //int ValeurOptoM1Bis=A;

//défintion paramètre moteur
int VitesseMax=5000; 
int VitesseMin=100;
bool EnMarcheM1=false;
bool EnMarcheM2=false;
bool EnMarcheM3=false;

AccelStepper Moteur1(STEPPER,M1PinPulse,M1PinDirection);
AccelStepper Moteur2(STEPPER,M2PinPulse,M2PinDirection);
AccelStepper Moteur3(STEPPER,M3PinPulse,M3PinDirection);
AccelStepper MoteurActif[]= {Moteur1,Moteur2,Moteur3};

//Variable nécessaire à la communication série 
int Separateur=-1; //permet de séparer la commande de l'ordre de commande 
 String Message ="";
 String Ordre ="";
 String Valeur ="" ; 
bool SensRotationCMD[]={true,true,true};
int AccelerationCMD[]={10000,10000,10000}; //Attribut de la commande d'accélération du système 
int SpeedCMD[]={1000,1000,1000};
int Nb_Pas_CMD=0;
int MoteurSelectionner=0;

int PinEnable=M1PinEnable;


//fonction homing : demande à la platine de translation d'aller à la position avant
void GoHome(int Moteur){
  if (Moteur==0){
    Moteur1.setAcceleration(5000);
    Moteur1.setSpeed(VitesseMax);
    //Avance rapide jusqu'à butée 
    while (digitalRead(M1PinLimitAvant)==true){
      Moteur1.move(-10);
      while(Moteur1.distanceToGo()>0){
        Moteur1.run();
      }
    }
    //Retour arrière pour sortir de la butée
    while (digitalRead(M1PinLimitAvant)==false){
      Moteur1.move(10);
      while(Moteur1.distanceToGo()>0){
        Moteur1.run();
      }
    }
    //Recherche de la position butée faible vitesse
    Moteur1.setAcceleration(5000);
    Moteur1.setSpeed(VitesseMin);
    //Avance rapide jusqu'à butée 
    while (digitalRead(M1PinLimitAvant)==true){
      Moteur1.move(-1);
      while(Moteur1.distanceToGo()>0){
        Moteur1.run();
      }
    }
    Moteur1.stop();
    Moteur1.setCurrentPosition(0);
    Serial.println("End Home");
  }
    if (Moteur==1){
    Moteur2.setAcceleration(5000);
    Moteur2.setSpeed(VitesseMax);
    //Avance rapide jusqu'à butée 
    while (digitalRead(M2PinLimitAvant)==true){
      Moteur2.move(-10);
      while(Moteur2.distanceToGo()>0){
        Moteur2.run();
      }
    }
    //Retour arrière pour sortir de la butée
    while (digitalRead(M2PinLimitAvant)==false){
      Moteur2.move(10);
      while(Moteur2.distanceToGo()>0){
        Moteur2.run();
      }
    }
    //Recherche de la position butée faible vitesse
    Moteur2.setAcceleration(5000);
    Moteur2.setSpeed(VitesseMin);
    //Avance rapide jusqu'à butée 
    while (digitalRead(M2PinLimitAvant)==true){
      Moteur2.move(-1);
      while(Moteur2.distanceToGo()>0){
        Moteur2.run();
      }
    }
    Moteur2.stop();
    Moteur2.setCurrentPosition(0);
    Serial.println("End Home");
  }
    if (Moteur==2){
    Moteur3.setAcceleration(5000);
    Moteur3.setSpeed(VitesseMax);
    //Avance rapide jusqu'à butée 
    while (digitalRead(M3PinLimitAvant)==true){
      Moteur3.move(-10);
      while(Moteur3.distanceToGo()>0){
        Moteur3.run();
      }
    }
    //Retour arrière pour sortir de la butée
    while (digitalRead(M3PinLimitAvant)==false){
      Moteur3.move(10);
      while(Moteur3.distanceToGo()>0){
        Moteur3.run();
      }
    }
    //Recherche de la position butée faible vitesse
    Moteur3.setAcceleration(5000);
    Moteur3.setSpeed(VitesseMin);
    //Avance rapide jusqu'à butée 
    while (digitalRead(M3PinLimitAvant)==true){
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
void Lecture(){
  //réinitialisation du séparateur pour nouvelle lecture 
 Separateur =-1; 
  //Lecture du port Série
 while (Serial.available()>0){
    Message=Serial.readStringUntil('\n');
    delay(15);
  }
  //Séparation de la partie message et de la valeur si elle existe 
  if (Message !="") {
    Separateur=Message.indexOf("_");
    //Cas d'une commande chiffrée 
    if (Separateur !=-1){
      Ordre = Message.substring(0,Separateur);
      Valeur = Message.substring(Separateur+1,Message.length());
    }
    // Cas d'une demande d'information
    if (Separateur == -1) {
      Ordre = Message.substring(0,Message.length());
      Valeur = "NULL";
    }
    //Gestion de selection du moteur 
    if (Ordre.substring(0,2)=="M1"){
      MoteurSelectionner=0;
      PinEnable=M1PinEnable;
      }
    else {
     if (Ordre.substring(0,2)=="M2"){
        MoteurSelectionner=1;
        PinEnable=M2PinEnable;
      }
      else {
        if (Ordre.substring(0,2)=="M3"){
          MoteurSelectionner=2;
          PinEnable=M3PinEnable;  
        }
        else {
          if (Ordre=="VERSION"){
            Serial.println(Version);
          }
          else{ Serial.println("ERROR");}
        }          
      }
      
    } 
    Ordre=Ordre.substring(2,Ordre.length());
  }
  //traitement d'une commande
  if (Valeur !="NULL" and Valeur!="") {
    //Cas d'un ordre de direction Si DIREC_0 ==> Sens direction = false , Sinon Sens direction = true
    if (Ordre == "DIREC") {
      if (Valeur == "0"){
        SensRotationCMD[MoteurSelectionner]=false;
      }
      else {
        SensRotationCMD[MoteurSelectionner]=true;
      }
      Serial.println("VALID");
    }
    //Cas d'un ordre de désactivation moteur 
    if (Ordre=="ENABL") {
        if (Valeur=="0"){
          digitalWrite(PinEnable,LOW);
        }
        else{
          digitalWrite(PinEnable,HIGH);
        }
      Serial.println("VALID");
    }
    //Cas d'un ordre d'accélération : stock la valeur d'accélération dans la Variable AccelerationCMD
    if (Ordre == "ACCEL") {
      AccelerationCMD[MoteurSelectionner]=Valeur.toInt();
      if (MoteurSelectionner==0) {
        Moteur1.setAcceleration(Valeur.toInt());
        Serial.println("VALID");
      }
      if (MoteurSelectionner==1) {
        Moteur2.setAcceleration(Valeur.toInt());
        Serial.println("VALID");
      }
      if (MoteurSelectionner==2) {
        Moteur3.setAcceleration(Valeur.toInt());
        Serial.println("VALID");
      }     
    }
        //Cas d'une commande de vitesse : stock la valeur de vitesse dans la valeur ValeurVitesseCMD
    if (Ordre == "SPEED") {
      SpeedCMD[MoteurSelectionner]=Valeur.toInt();
       if (MoteurSelectionner==0) {
        Moteur1.setMaxSpeed(Valeur.toInt());
        Serial.println("VALID");
      }
      if (MoteurSelectionner==1) {
        Moteur2.setMaxSpeed(Valeur.toInt());
        Serial.println("VALID");
      }
      if (MoteurSelectionner==2) {
        Moteur3.setMaxSpeed(Valeur.toInt());
        Serial.println("VALID");
      }
    }
    //Cas de commande d'un nombre de pas 
    if (Ordre == "DRIVE") {
        if (SensRotationCMD[MoteurSelectionner]==true){
          Nb_Pas_CMD=1*Valeur.toInt();
        }
        else {
          Nb_Pas_CMD=(-1)*Valeur.toInt();
        }
        Serial.println(Nb_Pas_CMD);
         if (MoteurSelectionner==0) {
          Moteur1.move(Nb_Pas_CMD);
          EnMarcheM1=true;
          Serial.println("START M1");
        }
        if (MoteurSelectionner==1){
          Moteur2.move(Nb_Pas_CMD);
          EnMarcheM2=true;
          Serial.println("START M2");
        } 
        if (MoteurSelectionner==2){
          Moteur3.move(Nb_Pas_CMD);
          EnMarcheM3=true;
          Serial.println("START M3");
        } 
    }
  }
  //Cas de message d'information
  else{
    //Cas d'un ordre Stop
    if (Ordre == "STOP"){ 
       if (MoteurSelectionner==0) {
        Moteur1.stop();
        EnMarcheM1=false;
        Serial.println("VALID");
      }
      if (MoteurSelectionner==1) {
        Moteur2.stop();
        Serial.println("VALID");
      }
      if (MoteurSelectionner==2){
        Moteur3.stop();
        Serial.println("VALID");
      }
    }
    //Cas d'un ordre de Homing
    if (Ordre == "HOME"){
      Serial.println("VALID");
      GoHome(MoteurSelectionner);
      }
  }
  Message ="";
  Ordre ="";
  Valeur ="";
}






void setup() {
  //Définition des pins limits
  pinMode(M1PinLimitAvant,INPUT_PULLUP);
  pinMode(M1PinLimitArriere,INPUT_PULLUP);
  pinMode(M2PinLimitAvant,INPUT_PULLUP);
  pinMode(M2PinLimitArriere,INPUT_PULLUP);
  //Définition des pins ENABLE Moteur
  pinMode(M1PinEnable,OUTPUT);
  digitalWrite(M1PinEnable,HIGH);
  pinMode(M2PinEnable,OUTPUT);
  digitalWrite(M2PinEnable,HIGH);
  //Port série définition
  Serial.begin(9600);
  delay(1000);
  //Définition entrée série 
  Message="";
  Ordre="";
  Valeur="" ; 
  //Définition Entrée Moteur de base
  Moteur1.setMaxSpeed(SpeedCMD[0]);
  Moteur1.setAcceleration(AccelerationCMD[0]);
  Moteur1.setCurrentPosition(0);
  Moteur2.setMaxSpeed(SpeedCMD[1]);
  Moteur2.setAcceleration(AccelerationCMD[1]);
  Moteur2.setCurrentPosition(0);
}

void loop() {
 //Vérification de lecture d'une entrée
  Lecture();
 //Cas moteur 1 en marche
  if ((EnMarcheM1==true && SensRotationCMD[0]==false && digitalRead(M1PinLimitArriere)==false)||(EnMarcheM1==true && SensRotationCMD[0]==true && digitalRead(M1PinLimitAvant)==false)){
    Serial.print("Butée rencontrée / reste : ");
    Serial.println(Moteur1.distanceToGo());
    Moteur1.stop();
    EnMarcheM1=false;
  }
  if (EnMarcheM1==true){
    Moteur1.run();
    if (Moteur1.distanceToGo()==0){
      EnMarcheM1=false;
      Moteur1.stop();
      Serial.println("End Move M1");
    }
  }
  //Cas moteur 2 en marche 
  if ((EnMarcheM2==true && SensRotationCMD[1]==false && digitalRead(M2PinLimitArriere)==false)||(EnMarcheM2==true && SensRotationCMD[1]==true && digitalRead(M2PinLimitAvant)==false)){
    Serial.print("Butée rencontrée / reste : ");
    Serial.println(Moteur2.distanceToGo());
    Moteur2.stop();
    EnMarcheM2=false;
  }
  if (EnMarcheM2==true){
    Moteur2.run();
    if (Moteur2.distanceToGo()==0){
      EnMarcheM2=false;
      Moteur2.stop();
      Serial.println("End Move M2");
    }
  //Cas moteur 3 en marche 
  if ((EnMarcheM3==true && SensRotationCMD[2]==false && digitalRead(M3PinLimitArriere)==false)||(EnMarcheM3==true && SensRotationCMD[2]==true && digitalRead(M3PinLimitAvant)==false)){
    Serial.print("Butée rencontrée / reste : ");
    Serial.println(Moteur3.distanceToGo());
    Moteur3.stop();
    EnMarcheM3=false;
  }
  if (EnMarcheM3==true){
    Moteur3.run();
    if (Moteur3.distanceToGo()==0){
      EnMarcheM3=false;
      Moteur3.stop();
      Serial.println("End Move M3");
    }
  }
  }
}
    

