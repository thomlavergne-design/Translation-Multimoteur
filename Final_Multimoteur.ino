//*****************
//Gestion de translation motorisée unique
// 07/06/2025
//*****************

//librairie utilisée
#include <AccelStepper.h>
#define STEPPER AccelStepper::DRIVER

//Versionning a changer a chaque modification du code.


//pin moteur 
const int M1PinEnable=5;
const int M1PinDirection=6;
const int M1PinPulse=7;

const int M2PinEnable=10;
const int M2PinDirection=11;
const int M2PinPulse=12;

//pin limitswitch
const int M1PinLimitAvant=3;
const int M1PinLimitArriere=4;
const int M2PinLimitAvant=8;
const int M2PinLimitArriere=9;

//pin Opto :
const int PinOptoM1=A0;
int ValeurOptoM1=0;
const int PinOptoM1Bis=A1;
int ValeurOptoM1Bis=A;

int Vitesse=400; 
bool EnMarcheM1=false;
bool EnMarcheM2=false;

AccelStepper Moteur1(STEPPER,M1PinPulse,M1PinDirection);
AccelStepper Moteur2(STEPPER,M2PinPulse,M2PinDirection);

//Variable nécessaire à la communication série 
int Separateur=-1; //permet de séparer la commande de l'ordre de commande 
 String Message ="";
 String Ordre ="";
 String Valeur ="" ; 
bool SensRotationCMD[]={true,true};
int AccelerationCMD[]={10000,10000}; //Attribut de la commande d'accélération du système 
int SpeedCMD[]={1000,1000};
int Nb_Pas_CMD=0;
int MoteurSelectionner=0;
int PinEnable=M1PinEnable;

void GoHome(){
  Moteur1.setAcceleration(500);
  Moteur1.setSpeed(1000);
  ValeurOptoM1=analogRead(PinOptoM1);
  while(ValeurOptoM1>550){
    Moteur1.runSpeed();
    ValeurOptoM1=analogRead(PinOptoM1);
    }
  Moteur1.move(-200);
  while(Moteur1.distanceToGo()>0){
    Moteur1.run();
    }
  Moteur1.setSpeed(100);
  ValeurOptoM1=analogRead(PinOptoM1);
  while(ValeurOptoM1>550){
    Moteur1.runSpeed();
    ValeurOptoM1=analogRead(PinOptoM1);
  }
  Moteur1.stop();
  Moteur1.setCurrentPosition(0);
  Serial.println("VALID");
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
      else {Serial.println("ERROR");}
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
    }
    //Cas de commande d'un nombre de pas 
    if (Ordre == "DRIVE") {
        Nb_Pas_CMD=Valeur.toInt();
        if (SensRotationCMD[MoteurSelectionner]==true){
          Nb_Pas_CMD=Valeur.toInt();
        }
        else {
          Nb_Pas_CMD=(-1)*Valeur.toInt();
        }
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
    }
    //Cas d'un ordre de Homing
    if (Ordre == "HOME"){
      GoHome();
      }
  }
    //if (Ordre=="COMPTE"){
    //  if (MoteurSelectionner==0){
    //    Serial.println(ComptePasLampes);
    //  }
    //  if (MoteurSelectionner==1){
    //    Serial.println(ComptePasFente);
    //  }
    //}
  //Remise à O des valeur d'ordre
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
    }
  }
  if ((EnMarcheM2==true && SensRotationCMD[1]==false && digitalRead(M2PinLimitArriere)==false)||(EnMarcheM2==true && SensRotationCMD[1]==true && digitalRead(M2PinLimitAvant)==false)){
    Serial.print("Butée rencontrée / reste : ");
    Serial.println(Moteur2.distanceToGo());
    Moteur1.stop();
    EnMarcheM2=false;
  }
 //Cas moteur 2 en marche 
  if (EnMarcheM2==true){
    Moteur2.run();
    if (Moteur1.distanceToGo()==0){
      EnMarcheM2=false;
      Moteur2.stop();
    }
  }
}
    

