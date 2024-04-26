import pandas as pd
from helpers import datachart

class CostPerProject(datachart.datachart):
    
    def __init__(self):
        self.title = "Cost per Project"
        self.x = "Project"
        self.xTitle = "Project"
        self.y = "Cost"
        self.yTitle = "Cost"
        self.dataframe = getOverallProjectCostsDataframe()
    

class CostPerProjectPerTeam(datachart.datachart):
    teams = ""

    def __init__(self):
        self.dataframe, self.teams = getProjectCostPerTeamAndTeamNames()
        self.x = 'Project'
        self.xTitle = 'Project'
        self.y = 'Cost'
        self.yTitle = 'Cost'

    def getTeams(self):
        return self.teams
    
    def getDataframe(self, team):
        dataframe = self.dataframe
        return dataframe[dataframe['Space Name'] == team]


def getProjectCostPerTeamAndTeamNames():
    mergedProjectCostData = getMergedProjectCostDataframe()
    projectCostPerDepartment = mergedProjectCostData.groupby(['Space Name', 'PROJECT CATEGORIES (FOR FINANCE)'])['Cost per Task'].sum().reset_index()
    projectCostPerDepartment = projectCostPerDepartment.sort_values(by=['Space Name', 'Cost per Task'], ascending=[True, False])
    projectCostPerDepartment.rename(columns={'PROJECT CATEGORIES (FOR FINANCE)': 'Project', 'Cost per Task': 'Cost'}, inplace=True)
    teams = projectCostPerDepartment['Space Name'].unique()
    return projectCostPerDepartment, teams

def getOverallProjectCostsDataframe():
    mergedProjectCostData = getMergedProjectCostDataframe()
    projectCostsDataframe = mergedProjectCostData.groupby('PROJECT CATEGORIES (FOR FINANCE)')
    projectCostsDataframe = projectCostsDataframe['Cost per Task'].sum()
    projectCostsDataframe = projectCostsDataframe.reset_index()
    projectCostsDataframe = projectCostsDataframe.sort_values(by='Cost per Task', ascending=False)
    projectCostsDataframe.rename(columns={'PROJECT CATEGORIES (FOR FINANCE)': 'Project', 'Cost per Task': 'Cost'}, inplace=True)
    return projectCostsDataframe

def getMergedProjectCostDataframe():
    hourRegistrationData = getHourRegistrationDataframe()
    userData = getUserDataframe()
    mergedProjectCostDataframe = pd.merge(hourRegistrationData, userData[['User ID', 'Hourly Cost']], on='User ID', how='inner')
    mergedProjectCostDataframe['Cost per Task'] = mergedProjectCostDataframe['Hourly Cost'] * mergedProjectCostDataframe['Time Tracked Hours']
    mergedProjectCostDataframe['Cost per Task'] = mergedProjectCostDataframe['Cost per Task'].round(2)
    return mergedProjectCostDataframe

def getHourRegistrationDataframe():
    hourRegistrationData = pd.read_excel('./hour_registration_data.xlsx', sheet_name='data')
    hourRegistrationData['Start'] = pd.to_datetime(hourRegistrationData['Start'])
    hourRegistrationData['Stop'] = pd.to_datetime(hourRegistrationData['Stop'])
    hourRegistrationData['Due Date'] = pd.to_datetime(hourRegistrationData['Due Date'])
    hourRegistrationData['Start Date'] = pd.to_datetime(hourRegistrationData['Start Date'])
    hourRegistrationData['Date Created'] = pd.to_datetime(hourRegistrationData['Date Created'])
    hourRegistrationData['Time Tracked Hours'] = hourRegistrationData['Time Tracked'] / (1000 * 60 * 60)  # Converts from ms to hours
    return hourRegistrationData

def getUserDataframe():
    userData = pd.read_excel('./users.xlsx', sheet_name='data')
    userData['Hourly Cost'] = userData['Labor Cost per Month'] / (21*7.5) # Avg work days multiplied by 7.5 work hours -> Logic here can be improved, but leaving it here for testing
    return userData