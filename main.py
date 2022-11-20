import os

from bs4 import BeautifulSoup
import zipfile
from pprint import pprint
import csv
import matplotlib.pyplot as plt

if __name__ == '__main__':
    print("Start")

    mainPath = "/home/flippi/Desktop/Saison_22_23"
    # mainPath = input("Input data path: ")
    # year = input("Input season year: ")
    year = "22_23"
    print(mainPath)

    dataPath = os.path.join(mainPath, 'data')
    os.makedirs(dataPath, exist_ok=True)
    files = os.listdir(mainPath)
    pprint(files)

    for file in files:
        print("processing file: " + file)
        if not file.endswith('.zip'):
            print('ignored ' + file)
            continue
        with zipfile.ZipFile(os.path.join(mainPath, file), 'r') as zip_ref:
            print('extracted ' + file)
            zip_ref.extractall(os.path.join(dataPath))

    dataFiles = os.listdir(dataPath)

    # pprint(dataFiles)

    for file in dataFiles:
        if not file.endswith(".chu"):
            os.remove(os.path.join(dataPath, file))

    pprint(os.listdir(dataPath))

    elimList = []
    teams = {}

    for file in os.listdir(dataPath):
        with open(os.path.join(dataPath, file), 'r') as f:
            content = f.read()
        unique_elim = []
        soup = BeautifulSoup(content, "xml")
        unique_name = soup.find('name').text

        chuTeams = soup.find_all("abbreviation")

        for chuTeam in chuTeams:
            if chuTeam.text not in teams:
                teams[chuTeam.text] = 0

        rides = soup.find_all('Ride')

        for ride in rides:
            sample = ride.findChild('Result', {"state": "1"})
            if sample is not None:
                unique_elim.append(ride)

        for elim in unique_elim:
            riderNo = elim.get("rider")
            riderNo = riderNo.strip()
            print(riderNo)
            eRider = soup.find("Rider", {"bootNo": riderNo})
            ridersTeam = eRider.parent.parent.abbreviation.text
            print(ridersTeam)

            teams[ridersTeam] += 1

        pprint(unique_elim)

        print(unique_name + "\tElims: " + str(len(unique_elim)))

        elims = (unique_name, len(unique_elim))
        elimList.append(elims)

    pprint(elimList)
    pprint(teams)

    # team_names, team_values = zip(*teams.items())
    # plt.figure(figsize=(len(teams)/2, 10))
    # plt.bar(team_names, team_values)
    # plt.xticks(rotation='vertical')
    # plt.show()

    exportName = year + "-elimsPerCHU.csv"
    exportPath = os.path.join(mainPath, exportName)

    with open(exportPath, 'w', newline='\n') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for item in elimList:
            writer.writerow(item)

    exportName = year + "-elimsPerTeam.csv"
    exportPath = os.path.join(mainPath, exportName)

    with open(exportPath, 'w', newline='\n') as csvfile:
        fields = ['Team', 'Eliminations']
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerows(teams.items())
