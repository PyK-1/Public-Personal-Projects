import matplotlib.pyplot as plt
import csv
import numpy as np
import statistics
from datetime import datetime, timedelta
MENU = """
        1 - All Networks Market Share by Region (Line Chart)
        2 - Percent of Market Share by Region (Pie Chart)
        3 - Network Market Share in Regions (Line Chart)
        4 - Total Market Share of all Social Networks in a Selected Region (Scatterplot)
        5 - Quit
       """

REGIONS = {"br": "Brazil",
           "fr": "France",
           "gb": "Great Britain",
           "in": "India",
           "cn": "China",
           "us": "United States" }

NETWORKS = {"fac": "Facebook",
            "ins": "Instagram",
            "lin": "LinkedIn",
            "pin": "Pinterest",
            "twi": "Twitter",
            "you": "YouTube"}


#########################################################  
## helpers 
######################################################### 

def region_select(multiple):
    if multiple:
        print(f"Region Codes: {REGIONS.keys()}")
        regionCode = input("Enter desired regions: ").lower()
        return regionCode
    else:
        print(f"Region Codes: {REGIONS.keys()}")
        regionCode = input("Enter desired region: ").lower()
        return regionCode

    pass

def network_select(multiple):
    if multiple:
        print(f"Network Codes: {NETWORKS.keys()}")
        networkCode = input("Enter desired networks: ").lower()
        return NETWORKS[networkCode]
    else:
        print(f"Network Codes: {NETWORKS.keys()}")
        network_code = input("Enter desired network: ").lower()
        return NETWORKS[network_code]

    pass

def read_data(region, networks):
    # return data from the region in a dictionary
    fileName = "data/social_media-" + region + "-daily-20200801-20201104.csv"
    region_data = {}
    print(f"Opening  {fileName}")
    date_list = []

    for network in networks:
        region_data[network]= []

    with open (fileName, 'r') as csv_file:
        data = csv.DictReader(csv_file)

        for row in data:
            for network in networks:
                region_data[network].append(float(row[network]))
            date_list.append(datetime.strptime(row["Date"], "%Y-%m-%d"))
        region_data["Date"] = date_list

    csv_file.close()

    return region_data
    
     
#########################################################  
## charts 
#########################################################          
def linechart(data, title, series_names):
    date = data["Date"]

    for a in series_names:
        plt.plot(date, data[a], label=a)

    plt.xlabel("Date")
    plt.ylabel("Market Share")
    plt.legend(loc="best")

    nDates = len(date)
    xTicks = np.arange(1, nDates, nDates // 4)
    xTicksLabels = [date[i] for i in xTicks]

    plt.xlabel(xTicksLabels)
    plt.xticks(rotation=45)
    plt.title(title)

    plt.legend()
    plt.show()

    pass

def piechart(data, title, series_names):
    singleDayData = []
    for a in series_names:
        singleDayData.append(data[a][0])

    plt.pie(singleDayData, labels=series_names,explode=(0,0,0,0.2,0,0), autopct='%1.1f%%')
    plt.title(title)
    plt.show()

    pass

def scatterplot(data, title, series_names):
    date = data["Date"]
    fig, ax = plt.subplots()

    for a in series_names:
        plt.scatter(date, data[a], label=a)

    nDates = len(date)
    xTicks = np.arange(1, nDates, nDates // 4)
    xTicksLabels = [date[i] for i in xTicks]
    plt.xlabel(xTicksLabels)

    plt.xticks(rotation=45)
    plt.legend(loc="best")

    ax.set_xlabel('Market Share Range')
    plt.title(title)

    plt.show()

    pass

#########################################################  
## menu options 
######################################################### 
            
def option1():
    print("1 - All Networks Market Share by Region (Line Chart)")
    region = region_select(False) #only select one
    region_data = read_data(region, NETWORKS.values())
    region_name = REGIONS[region]
    title = f"Social Media Market Share: {region_name}"
    linechart(region_data, title, NETWORKS.values())
      
def option2():
    print("2 - Percent of Market Share by Region (Pie Chart)")
    region = region_select(False)
    regionData = read_data(region, NETWORKS.values())
    regionName = REGIONS[region]
    title = f"Social Media Market Share: {regionName}"
    piechart(regionData, title, NETWORKS.values())
    pass
    
def option3():
    print("3 - Network Market Share in Regions (Line Chart)")
    region = region_select(True)
    regionList = region.split()

    networkSelection = network_select(False)
    network = [networkSelection]
    newData = {}

    for region in regionList:
        regionData = read_data(region, network)
        newKey = REGIONS[region]
        oldKey = networkSelection
        regionData[newKey] = regionData.pop(oldKey)
        newData[newKey] = regionData[newKey]
        newData["Date"] = regionData["Date"]

    fullRegionNames = []
    for region in regionList:
        fullRegionNames.append(REGIONS[region])

    finalStr = ",".join(fullRegionNames)
    title = f"{networkSelection} Market Share: {finalStr}"
    linechart(newData, title, fullRegionNames)

    pass
        
def option4():
    print("4 - Total Market Share of all Social Networks in a Selected Region (Scatterplot)")
    region = region_select(False)
    region_data = read_data(region, NETWORKS.values())
    region_name = REGIONS[region]
    title = f"Networks Market Share: {region_name}"
    scatterplot(region_data, title, NETWORKS.values())

    pass

def main():
    
    done = False
    while not done:
        print(MENU)
        choice = input("Enter your choice: ")
        
        if choice == "1":
            option1()
        elif choice == "2":
            option2()
        elif choice == "3":
            option3()
        elif choice == "4":
            option4()
        elif choice == "5":
            done = True
        else:   
            print("Invalid choice. Please try again.")
main()
