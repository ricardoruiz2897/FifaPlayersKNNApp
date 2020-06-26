
from joblib import  load, dump
import gcsfs

import pandas as pd
from sklearn.neighbors import NearestNeighbors

import ssl

class FifaMachineLearning:

    def __init__(self, n_neighbors = 1, type = "player", ignore_nationality = False):
        try:

            #Certificate so we can access files
            ssl._create_default_https_context = ssl._create_unverified_context
            fs = gcsfs.GCSFileSystem(project='maps-geocoding-1574279493983')

            if type == "player":

                with fs.open('ricardoruiz-example-bucket-1/players_data.csv') as f:
                    self.data = pd.read_csv(f)

            elif type == "gk" :
                with fs.open('ricardoruiz-example-bucket-1/gk_data.csv') as f:
                    self.data = pd.read_csv(f)

            else:
                self.data = None
                self.message = "Error in player type!"

            #List of ids
            self.ids = list(self.data['id'])

            #Returns numpy array object redy for prediction.
            self.processed = self.__Process(ignore_nationality)

            #Creates the Model
            self.model = self.__CreateModel(n_neighbors)

            #No errors
            self.message = "Model Created"

        except FileExistsError:
            self.zero = list()
            self.message = "File Not Found!"

    #Returns ids, given the obtained indexes from the predictive model
    def __processResults(self, results):
        players = []
        for i in range(1, len(results[0])):
            players.append(self.ids[results[0][i]])
        return players

    #Gets data ready for prediction
    def __Process(self, ignore_nationality):
        remove = ['Unnamed: 0', 'id']

        if ignore_nationality:
            remove = remove + self.__getCountries()

        processing = self.data.drop(columns=remove)

        return processing.to_numpy()

    #Type should be player or gk
    def __CreateModel(self, n):
        # Instance of neighbors classifier. (One more neighbor because the first will be the input)
        model = NearestNeighbors(n_neighbors=n+1)

        # Create model
        model.fit(self.processed)

        return model

    def SaveModel(self, fileName):
        dump(self.model, fileName)
        return

    #This function predicts the closest n given id
    def Closest(self, id, MLmodel = None):

        #Index of id
        index = self.ids.index(id)

        #Get the data of player we want to find.
        predict_vector = self.processed[index:index+1]

        if MLmodel == None:
            #Get knn result
            res = self.model.kneighbors(predict_vector, return_distance=False)
        else:
            res = MLmodel.kneighbors(predict_vector, return_distance=False)

        #Return result as list.
        return self.__processResults(res.tolist())

    def __getCountries(self):
        countries =  ['Afghanistan', 'Albania', 'Algeria', 'Angola', 'Antigua & Barbuda',
                'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bolivia',
                'Bosnia Herzegovina', 'Brazil', 'Brunei Darussalam', 'Bulgaria',
                'Burkina Faso', 'Burundi', 'Cameroon', 'Canada', 'Cape Verde', 'Central African Rep.', 'Chad', 'Chile', 'China PR', 'Colombia', 'Comoros', 'Congo',
                'Costa Rica', 'Croatia', 'Cuba', 'Curacao', 'Cyprus', 'Czech Republic', 'Denmark',
                'Dominican Republic', 'DR Congo', 'Ecuador', 'Egypt', 'El Salvador', 'England', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia',
                'Faroe Islands', 'Fiji', 'Finland', 'France', 'FYR Macedonia', 'Gabon', 'Gambia',
                'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Grenada', 'Guam', 'Guatemala', 'Guinea', 'Guinea Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hong Kong',
                'Hungary', 'Iceland', 'India', 'Iran', 'Iraq', 'Israel',
                'Italy', 'Ivory Coast', 'Jamaica', 'Japan', 'Kazakhstan', 'Kenya', 'Korea DPR',
                'Korea Republic', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 'Latvia', 'Lebanon', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania',
                'Luxembourg', 'Madagascar', 'Mali', 'Malta', 'Mauritania', 'Mauritius', 'Mexico',
                'Moldova', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Namibia', 'Netherlands', 'New Caledonia', 'New Zealand',
                'Niger', 'Nigeria', 'Northern Ireland', 'Norway', 'Oman', 'Palestine', 'Panama', 'Paraguay', 'Peru', 'Philippines', 'Poland',
                'Portugal', 'Puerto Rico', 'Qatar', 'Republic of Ireland', 'Romania', 'Russia', 'San Marino', 'São Tomé & Príncipe', 'Saudi Arabia',
                'Scotland', 'Senegal', 'Serbia', 'Sierra Leone',
                'Slovakia', 'Slovenia', 'Somalia',
                'South Africa', 'Spain', 'Sri Lanka',
                'St Kitts Nevis', 'St Lucia', 'Sudan', 'Suriname', 'Swaziland', 'Sweden', 'Switzerland', 'Syria', 'Tanzania',
                'Thailand', 'Togo', 'Trinidad & Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Uganda', 'Ukraine', 'United States',
                'Uruguay', 'Uzbekistan', 'Venezuela', 'Vietnam', 'Wales', 'Zambia', 'Zimbabwe']

        countries = [x.lower() for x in countries]
        countries = [x.replace(" ", ".") for x in countries]

        return countries