import os
import sys
import json
import xmltodict

from Utils import Utils

class HealthKitParser:

    # exportpath: str
    # formated: dict
    # healthjson: dict
    # recordlen: int

    # Class Routines
    def __init__(self, path: str):
        self.exportpath: str = (path + "/export.xml").replace("//", "/")
        self.formated: dict = {}
        self.healthjson: dict = {}
        self.recordlen: int = 0

        if not os.path.exists(path):
            raise Exception("Wrong export file: path doesn't exists.")
        if not os.path.exists(self.exportpath):
            raise Exception("No export.xml file found.")

        self.healthjson = xmltodict.parse(Utils.readFile(self.exportpath))
        self.parse()
        self.logIt()

    # Parser
    def parse(self):
        if not self.healthjson or len(self.healthjson) < 1:
            raise Exception("Health wrongly parsed.")
        if self.healthjson['HealthData']['@locale'] != "fr_FR":
            print("\033[93mWARNING\033[00m")
            print("La langue de l'export n'est pas le Français.")
            print("Certaines fonctionnalités, tout comme l'export final peuvent ne pas totalement fonctionner.")


        if 'body' not in self.formated:
            self.formated['body'] = {
                'bloodtype': self.healthjson['HealthData']['Me']['@HKCharacteristicTypeIdentifierBloodType'],
                'birth': self.healthjson['HealthData']['Me']['@HKCharacteristicTypeIdentifierDateOfBirth'],
                'sexe': self.healthjson['HealthData']['Me']['@HKCharacteristicTypeIdentifierBiologicalSex']
            }
            if self.formated['body']['sexe'] == "HKBiologicalSexMale":
                self.formated['body']['sexe'] = "male"
            elif self.formated['body']['sexe'] == "HKBiologicalSexFemale":
                self.formated['body']['sexe'] = "female"
        print("Analysing data exported on", self.healthjson['HealthData']['ExportDate']['@value'])
        print("")
        print("Blood Type:", self.formated['body']['bloodtype'])
        print("Birth date:", self.formated['body']['birth'])
        print("Sexe:      ", self.formated['body']['sexe'])
        print("")

        self.parseRecords()
    def parseRecords(self):
        count: int = 0

        if 'records' not in self.formated:
            self.formated['records'] = {}
        self.recordlen = len(self.healthjson['HealthData']['Record'])
        for record in self.healthjson['HealthData']['Record']:
            count += 1
            print(str(int(count / self.recordlen * 100)) + "% [" + str(count) + "/" + str(self.recordlen) + "]", end="\r")


            # Heart
            if record['@type'] == "HKQuantityTypeIdentifierHeartRate":
                self.parseBasics(record, "Heart", "Heartrate")
            elif record['@type'] == "HKQuantityTypeIdentifierBloodPressureSystolic":
                self.parseBasics(record, "Heart", "BloodPressureSystolic")
            elif record['@type'] == "HKQuantityTypeIdentifierBloodPressureDiastolic":
                self.parseBasics(record, "Heart", "BloodPressureDiastolic")
            elif record['@type'] == "HKQuantityTypeIdentifierRestingHeartRate":
                self.parseBasics(record, "Heart", "RestingHeartRate")


            # Nutrition
            elif record['@type'] == "HKQuantityTypeIdentifierDietaryWater":
                self.parseBasics(record, "Nutrition", "Water")
            elif record['@type'] == "HKQuantityTypeIdentifierDietaryFatTotal":
                self.parseBasics(record, "Nutrition", "Fat")
            elif record['@type'] == "HKQuantityTypeIdentifierDietaryFatPolyunsaturated":
                self.parseBasics(record, "Nutrition", "FatPolyunsaturated")
            elif record['@type'] == "HKQuantityTypeIdentifierDietaryFatMonounsaturated":
                self.parseBasics(record, "Nutrition", "FatMonounsaturated")
            elif record['@type'] == "HKQuantityTypeIdentifierDietaryFatSaturated":
                self.parseBasics(record, "Nutrition", "FatSaturated")
            elif record['@type'] == "HKQuantityTypeIdentifierDietaryCholesterol":
                self.parseBasics(record, "Nutrition", "Cholesterol")
            elif record['@type'] == "HKQuantityTypeIdentifierDietarySodium":
                self.parseBasics(record, "Nutrition", "Sodium")
            elif record['@type'] == "HKQuantityTypeIdentifierDietaryCarbohydrates":
                self.parseBasics(record, "Nutrition", "Carbohydrates")
            elif record['@type'] == "HKQuantityTypeIdentifierDietaryFiber":
                self.parseBasics(record, "Nutrition", "Fiber")
            elif record['@type'] == "HKQuantityTypeIdentifierDietarySugar":
                self.parseBasics(record, "Nutrition", "Sugar")
            elif record['@type'] == "HKQuantityTypeIdentifierDietaryEnergyConsumed":
                self.parseBasics(record, "Nutrition", "EnergyConsumed") # J'sais pas ce que c'est, mais semble interessant
            elif record['@type'] == "HKQuantityTypeIdentifierDietaryProtein":
                self.parseBasics(record, "Nutrition", "Protein")
            elif record['@type'] == "HKQuantityTypeIdentifierDietaryVitaminA":
                self.parseBasics(record, "Nutrition", "VitaminA")
            elif record['@type'] == "HKQuantityTypeIdentifierDietaryVitaminB6":
                self.parseBasics(record, "Nutrition", "VitaminB6")
            elif record['@type'] == "HKQuantityTypeIdentifierDietaryVitaminB12":
                self.parseBasics(record, "Nutrition", "VitaminB12")
            elif record['@type'] == "HKQuantityTypeIdentifierDietaryVitaminC":
                self.parseBasics(record, "Nutrition", "VitaminC")
            elif record['@type'] == "HKQuantityTypeIdentifierDietaryVitaminD":
                self.parseBasics(record, "Nutrition", "VitaminD")
            elif record['@type'] == "HKQuantityTypeIdentifierDietaryVitaminE":
                self.parseBasics(record, "Nutrition", "VitaminE")
            elif record['@type'] == "HKQuantityTypeIdentifierDietaryVitaminK":
                self.parseBasics(record, "Nutrition", "VitaminK")
            elif record['@type'] == "HKQuantityTypeIdentifierDietaryCalcium":
                self.parseBasics(record, "Nutrition", "Calcium")
            elif record['@type'] == "HKQuantityTypeIdentifierDietaryIron":
                self.parseBasics(record, "Nutrition", "Iron")
            elif record['@type'] == "HKQuantityTypeIdentifierDietaryThiamin":
                self.parseBasics(record, "Nutrition", "Thiamin")
            elif record['@type'] == "HKQuantityTypeIdentifierDietaryRiboflavin":
                self.parseBasics(record, "Nutrition", "Riboflavin")
            elif record['@type'] == "HKQuantityTypeIdentifierDietaryNiacin":
                self.parseBasics(record, "Nutrition", "Niacin")
            elif record['@type'] == "HKQuantityTypeIdentifierDietaryFolate":
                self.parseBasics(record, "Nutrition", "Folate")
            elif record['@type'] == "HKQuantityTypeIdentifierDietaryBiotin":
                self.parseBasics(record, "Nutrition", "Biotin")
            elif record['@type'] == "HKQuantityTypeIdentifierDietaryPantothenicAcid":
                self.parseBasics(record, "Nutrition", "PantothenicAcid")
            elif record['@type'] == "HKQuantityTypeIdentifierDietaryPhosphorus":
                self.parseBasics(record, "Nutrition", "Phosphorus")
            elif record['@type'] == "HKQuantityTypeIdentifierDietaryIodine":
                self.parseBasics(record, "Nutrition", "Iodine")
            elif record['@type'] == "HKQuantityTypeIdentifierDietaryMagnesium":
                self.parseBasics(record, "Nutrition", "Magnesium")
            elif record['@type'] == "HKQuantityTypeIdentifierDietaryZinc":
                self.parseBasics(record, "Nutrition", "Zinc")
            elif record['@type'] == "HKQuantityTypeIdentifierDietarySelenium":
                self.parseBasics(record, "Nutrition", "Selenium")
            elif record['@type'] == "HKQuantityTypeIdentifierDietaryCopper":
                self.parseBasics(record, "Nutrition", "Copper")
            elif record['@type'] == "HKQuantityTypeIdentifierDietaryManganese":
                self.parseBasics(record, "Nutrition", "Manganese")
            elif record['@type'] == "HKQuantityTypeIdentifierDietaryChloride":
                self.parseBasics(record, "Nutrition", "Chloride")
            elif record['@type'] == "HKQuantityTypeIdentifierDietaryPotassium":
                self.parseBasics(record, "Nutrition", "Potassium")


            # Sleep Analysis
            elif record['@type'] == "HKCategoryTypeIdentifierSleepAnalysis":
                self.parseSleep(record)


            # Body size
            elif record['@type'] == "HKQuantityTypeIdentifierBodyMass":
                self.parseBasics(record, "BodyMensurations", "Mass")
            elif record['@type'] == "HKQuantityTypeIdentifierBodyFatPercentage":
                self.parseBasics(record, "BodyMensurations", "FatPercentage")
            elif record['@type'] == "HKQuantityTypeIdentifierLeanBodyMass":
                self.parseBasics(record, "BodyMensurations", "LeanBodyMass") # Indice de masse maigre
            elif record['@type'] == "HKQuantityTypeIdentifierBodyMassIndex":
                self.parseBasics(record, "BodyMensurations", "IMC")
            elif record['@type'] == "HKQuantityTypeIdentifierHeight":
                self.parseBasics(record, "BodyMensurations", "Height")


            # Steps
            elif record['@type'] == "HKQuantityTypeIdentifierStepCount":
                self.parseBasics(record, "Steps", "StepCount")
            elif record['@type'] == "HKQuantityTypeIdentifierDistanceWalkingRunning":
                self.parseBasics(record, "Steps", "DistanceWalkingRunning")
            elif record['@type'] == "HKQuantityTypeIdentifierFlightsClimbed":
                self.parseBasics(record, "Steps", "FloorsClimbed")
            elif record['@type'] == "HKQuantityTypeIdentifierWalkingDoubleSupportPercentage":
                self.parseBasics(record, "Steps", "WalkingDoubleSupportPercentage")
            elif record['@type'] == "HKQuantityTypeIdentifierWalkingSpeed":
                self.parseBasics(record, "Steps", "WalkingDoubleSupportPercentage")
            elif record['@type'] == "HKQuantityTypeIdentifierWalkingStepLength":
                self.parseBasics(record, "Steps", "WalkingStepLength")
            elif record['@type'] == "HKQuantityTypeIdentifierWalkingAsymmetryPercentage":
                self.parseBasics(record, "Steps", "WalkingAsymmetryPercentage")
            elif record['@type'] == "HKQuantityTypeIdentifierAppleWalkingSteadiness":
                self.parseBasics(record, "Steps", "WalkingSteadiness")


            # Energy
            elif record['@type'] == "HKQuantityTypeIdentifierBasalEnergyBurned":
                self.parseBasics(record, "Energy", "BasalEnergyBurned") # Energie brulé au repos
            elif record['@type'] == "HKQuantityTypeIdentifierActiveEnergyBurned":
                self.parseBasics(record, "Energy", "ActiveEnergyBurned")
            elif record['@type'] == "HKQuantityTypeIdentifierDistanceCycling":
                self.parseBasics(record, "Energy", "ActiveEnergyBurned")


            # Audio
            elif record['@type'] == "HKQuantityTypeIdentifierHeadphoneAudioExposure":
                self.parseBasics(record, "Audio", "HeadphoneAudioExposure")


            # Unknown
            else:
                print(record)
                if "unknown" not in self.formated:
                    self.formated['unknown'] = {}
                if "HKType" not in self.formated['unknown']:
                    self.formated['unknown']['HKType'] = []
                self.formated['unknown']['HKType'].append(record['@type'])
                print("")

        print(str(int(count / self.recordlen * 100)) + "% " + str(count) + " data line parsed.")

    # Side data
    def dumpSource(self, source: str):
        if 'sources' not in self.formated:
            self.formated['sources'] = []
        if source not in self.formated['sources']:
            self.formated['sources'].append(source)
    def dumpUnit(self, unit: str):
        if 'unit' not in self.formated:
            self.formated['unit'] = []
        if unit not in self.formated['unit']:
            self.formated['unit'].append(unit)
    def dumpMetadata(self, data: list):
        key: str = None
        subkey: str = None
        tmpmetadata: dict = {}

        for elem in data['MetadataEntry']:
            if elem['@key'] == 'Repas':
                key = "Eaten"
                subkey = elem['@value']
            elif elem['@key'] == "HKFoodType":
                key = "Eaten"
                if subkey is None:
                    subkey = elem['@value']
                tmpmetadata = {
                    'ate': elem['@value'],
                    'fat': 0
                }

        try:
            if key is not None and key not in self.formated:
                self.formated[key] = {} if subkey is not None else []
            if subkey is not None and subkey not in self.formated[key]:
                self.formated[key][subkey] = {}
            if key is not None:
                if subkey is not None:
                    self.formated[key][subkey].append(tmpmetadata)
                else:
                    self.formated[key].append(tmpmetadata)
        except Exception as e:
            # print("Error a gérer plus tard avec les parses de metadata:")
            # print(e)
            pass

    # Basic parse
    def parseBasics(self, row: dict, category: str, ident: str):
        tmpformat: dict = {}

        if category not in self.formated['records']:
            self.formated['records'][category] = {ident: []}
        elif ident not in self.formated['records'][category]:
            self.formated['records'][category][ident] = []

        tmpformat = {
            'dates': {
                'created': row['@creationDate'].replace(" +", ".000+").replace(" ", "T"),
                'start': row['@startDate'].replace(" +", ".000+").replace(" ", "T"),
                'end': row['@endDate'].replace(" +", ".000+").replace(" ", "T")
            },
            'unit': row['@unit'],
            'value': row['@value'],
            'source': {
                'name': row['@sourceName'],
                'version': row['@sourceVersion'],
            },
        }
        if row['@sourceName'] == "Santé":
            if 'MetadataEntry' in row and '@value' in row['MetadataEntry']:
                tmpformat['isUser'] = row['MetadataEntry']['@value'] == 1
        if 'MetadataEntry' in row and type(row['MetadataEntry']) == list:
            self.dumpMetadata(row)

        self.dumpSource(row['@sourceName'])
        self.dumpUnit(row['@unit'])
        self.formated['records'][category][ident].append(tmpformat)
    def parseSleep(self, row: dict):
        category: str = "Sleep"
        ident: str = None
        tmpformat: dict = {}

        if '@value' in row and row['@value'] == "HKCategoryValueSleepAnalysisInBed":
            ident = "AnalysisInBed"
        if category not in self.formated['records']:
            self.formated['records'][category] = {ident: []}
        elif ident not in self.formated['records'][category]:
            self.formated['records'][category][ident] = []

        tmpformat = {
            'dates': {
                'created': row['@creationDate'].replace(" +", ".000+").replace(" ", "T"),
                'start': row['@startDate'].replace(" +", ".000+").replace(" ", "T"),
                'end': row['@endDate'].replace(" +", ".000+").replace(" ", "T")
            },
            'source': {
                'name': row['@sourceName'],
                'version': row['@sourceVersion'],
            },
        }
        if row['@sourceName'] == "Santé":
            if 'MetadataEntry' in row and '@value' in row['MetadataEntry']:
                tmpformat['isUser'] = row['MetadataEntry']['@value'] == 1
        if 'MetadataEntry' in row and type(row['MetadataEntry']) == list:
            self.dumpMetadata(row)

        self.dumpSource(row['@sourceName'])
        self.formated['records'][category][ident].append(tmpformat)

    # Logs
    def logIt(self):
        path: str = "./apple-parsed-export"

        if os.path.exists(path) and not "--force" in sys.argv:
            print("\033[93mWARNING\033[00m Output path already exists; try --force to overwrite it.")
        Utils.saveinFile(path, self.formated)


if __name__ == "__main__":
    HealthKitParser("./apple_health_export")

