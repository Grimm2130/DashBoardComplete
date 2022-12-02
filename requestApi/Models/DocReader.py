import pandas as pd
# Read in the csv

class DocReader():
    '''A class that reads in the passed into the constructor, allows for pandas functionality'''
    # instantiate a class for the file Item
    def __init__(self, dataFile):
        self.dataFile = dataFile
        self.data = pd.read_csv(dataFile)
    # Store a pd Dataframe of the file Items
    def getData(self):
        '''Return a pandas dataframe of the read file'''
        return self.data
    def __len__(self):
        rowNum = self.data[self.data.columns[0]].count()
        colNum = len(self.data.columns)
        '''Retunr the number of items in the list'''
        return f"Row count: {rowNum} & Column count: {colNum}"
    def getAttributes(self):
        return list(self.data.columns)
    def getItems(self, attribute):
        # Check the state of the arrtubute passed
        if(type(attribute) == str ):
            #return values at that column
            return list(self.data[attribute].unique())
        elif(type(attribute) == int):
            return list( self.data[ self.data.columns[attribute] ].unique() )
    # todo




