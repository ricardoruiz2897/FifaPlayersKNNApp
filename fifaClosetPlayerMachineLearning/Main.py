import FifaMachineLearning
from joblib import load

fifaML = FifaMachineLearning.FifaMachineLearning(10, "gk", True)
print(fifaML.Closest(192119))

#fifaML.SaveModel(fileName="MLModels/knn_player_model_10.joblib")
#print("Model Saved")

#MLmodel = load("MLModels/knn_player_model_10.joblib")


'''
import pandas as pd
import gcsfs


fs = gcsfs.GCSFileSystem(project='maps-geocoding-1574279493983')
with fs.open('ricardoruiz-example-bucket-1/players_data.csv') as f:
    df = pd.read_csv(f)

print(list(df.columns))
'''