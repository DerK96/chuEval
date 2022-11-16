import os

from bs4 import BeautifulSoup
import zipfile
from pprint import pprint
import csv

if __name__ == '__main__':
    print("Start")

    # mainPath = "/home/flippi/Desktop/testSeason"
    mainPath = input("Input data path: ")
    year = input("Input season year: ")
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

    for file in os.listdir(dataPath):
        with open(os.path.join(dataPath, file),'r') as f:
            content = f.read()

        soup = BeautifulSoup(content, "xml")
        unique_name = soup.find('name').text

        unique_elim = soup.find_all('Result', {"state": "1"})

        print(unique_name)
        print(len(unique_elim))

        elims = (unique_name, len(unique_elim))
        elimList.append(elims)

    pprint(elimList)

    exportName = year + "-elims.csv"
    exportPath = os.path.join(mainPath, exportName)

    with open(exportPath, 'w', newline='\n') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for item in elimList:
            writer.writerow(item)
