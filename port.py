#========== IMPORT ==========#

import csv
import pickle

#========== DATA FUNCTIONS ==========#

def import_csv(url, bridge):
    file = open(url, "r")
    csvreader = csv.reader(file)
    for rec in csvreader:
        bridge.add_house(rec[0], rec[1], rec[2], rec[3])
    file.close()

def export_csv(url, bridge):
    file = open(url, "w")
    csvwriter = csv.writer(file)
    csvwriter.writerows(bridge.get_houses())
    file.close()

#========== SETTINGS FUNCTIONS ==========#

def save_settings(fluc, chg, pay):
    file = open("./settings.dat", "wb")
    pickle.dump([fluc, chg, pay], file)
    file.close()

def load_settings():
    file = open("./settings.dat", "rb")
    settings = pickle.load(file)
    file.close()
    return settings
