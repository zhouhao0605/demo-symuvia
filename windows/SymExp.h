//------------------------------------------
// Fonctions exportées de la DLL SYMUVIA
//------------------------------------------

#include <string>
#include "TrafficState.h"

// Chargement du scenario
__declspec(dllexport) bool __cdecl SymLoadNetwork(std::string sTmpXmlDataFile, std::string sScenarioID = "");
__declspec(dllexport) bool __cdecl SymLoadNetwork(std::string sTmpXmlDataFile, eveShared::SimulationInfo * &pSInfo, eveShared::SymuviaNetwork * &pSNetwork, std::string sScenarioID = "");

// Sortie de la simulation
__declspec(dllexport) int  __cdecl SymQuit();

// ----- Simulation complète -----

// Exécution complète d'une simulation
__declspec(dllexport) bool __cdecl SymRun();

// Exécution complète d'une simulation de trafic
__declspec(dllexport) bool __cdecl SymRunTraffic();

// Exécution complète d'une simulation des émissions acoustiques
__declspec(dllexport) bool __cdecl SymRunAcousticEmissions();

// Exécution complète d'une simulation des émissions atmosphériques
__declspec(dllexport) bool __cdecl SymRunAirEmissions();


// ----- Simulation pas à pas -----

// Exécution d'un pas de temps d'une simulation (et sortie de l'état de la simulation)
__declspec(dllexport) bool __cdecl SymRunNextStep(std::string &sXmlFluxInstant, bool bTrace, bool &bNEnd);
__declspec(dllexport) bool __cdecl SymRunNextStep(eveShared::TrafficState * &pTrafficEVE, bool bTrace, bool &bNEnd);

__declspec(dllexport) char* __cdecl SymRunNextStepNode(bool bTrace, bool &bNEnd);

// Exécution d'un pas de temps d'une simulation de trafic
__declspec(dllexport) bool __cdecl SymRunNextStepTraffic(std::string &sXmlFluxInstant, bool bTrace, bool &bNEnd);
__declspec(dllexport) bool __cdecl SymRunNextStepTraffic(eveShared::TrafficState * &pTrafficEVE, bool bTrace, bool &bNEnd);

// Exécution d'un pas de temps d'une simulation de trafic et d'acoustique
__declspec(dllexport) bool __cdecl SymRunNextStepTrafficAcoustic(std::string &sXmlFluxInstant, bool bCel, bool bSrc, bool bTrace, bool &bNEnd);
__declspec(dllexport) bool __cdecl SymRunNextStepTrafficAcoustic(eveShared::TrafficState * &pTrafficEVE, bool bCel, bool bSrc, bool bTrace, bool &bNEnd);

// Exécution d'un pas de temps d'une simulation de trafic et d'atmospherique
__declspec(dllexport) bool __cdecl SymRunNextStepTrafficAtmospheric(std::string &sXmlFluxInstant, bool bTrace, bool &bNEnd);

// Déplacement vers un pas de temps d'indice donné
__declspec(dllexport) bool __cdecl SymRunToStep(int nStep, std::string &sXmlFluxInstant, bool bTrace, bool &bNEnd);
__declspec(dllexport) bool __cdecl SymRunToStep(int nStep, eveShared::TrafficState * &pTrafficEVE, bool bTrace, bool &bNEnd);

// Réinitialisation de la simulation au premier instant
__declspec(dllexport) int  __cdecl SymReset(); 

// Ménage
__declspec(dllexport) bool __cdecl SymRunDeleteTraffic(eveShared::TrafficState * &pTrafficEVE);

// ----- Mise à jour des scenari -----

// Mise à jour du scenario
__declspec(dllexport) bool __cdecl SymUpdateNetwork(std::string sXmlDataFile);

// Mise à jour d'un plan de feux du réseau
__declspec(dllexport) int  __cdecl SymSendSignalPlan(std::string sCDF, std::string sSP);

// Mise à jour d'une vitesse réglementaire d'un tronçon du réseau
__declspec(dllexport) int  __cdecl SymSendSpeedLimit(std::string sSection, std::string sVehType, double dbSpeedLimit);

// Affectation d'itinéraires pour une OD
__declspec(dllexport) int __cdecl SymSetRoutes(char* originId, char* destinationId, char* typeVeh, char** links[] , double coeffs[], int iLength);

// ----- Pilotage des véhicules -----

// Création d'un véhicule
__declspec(dllexport) int __cdecl SymCreateVehicle(std::wstring sType, std::wstring sEntree, std::wstring sSortie, int nVoie, double dbt);

// Pilotage d'un véhicule
__declspec(dllexport) int __cdecl SymDriveVehicle(int nID, std::wstring	sTroncon, int nVoie, double dbPos, bool bForce);

// Modification d'un itinéraire d'un véhicule
__declspec(dllexport) int __cdecl SymAlterRoute(int nIdVeh, char*  links[] , int iLength);

// Retourne les itinéraires actuels d'une liste de véhicules
__declspec(dllexport) char* __cdecl SymGetVehiclesPaths( char*  vehiculeId[], int iLength);

// ----- Sorties complémentaires -----

// Génération du reseau EVE
__declspec(dllimport) bool __cdecl SymGenEveNetwork(eveShared::EveNetwork * &pNetwork);

// Génération de la liste des cellules acoustiques
__declspec(dllexport) bool __cdecl SymGenAcousticCells();

// ----- Sérialisation -----

// Sauvegarde de l'état courant vers un fichier XML
__declspec(dllexport) void __cdecl SymSaveState(char* sXmlDataFile);

// Chargement d'un état sauvegardé depuis un fichier XML
__declspec(dllexport) void __cdecl SymLoadState(char* sXmlDataFile);


// ----- Post-traitement -----

// Module de calcul de décélération
__declspec(dllexport) bool __cdecl SymDeceleration(double dbRate);

// Module de calcul des trajectories
__declspec(dllexport) bool __cdecl SymGenTrajectories();

// Module PHEM
__declspec(dllexport) bool __cdecl SymGenPHEMFiles(std::string sOutputDirectory, std::vector<int> IDs = std::vector<int>());
__declspec(dllexport) bool __cdecl SymRunPHEM(std::string sPHEMPath, std::string sDRIFile);
