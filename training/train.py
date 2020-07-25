import pandas as pd
import training.model as model

features = pd.read_csv('./../resources/MSFTfeatures.csv')
labels = pd.read_csv('./../resources/MSFTlabels.csv')

print(features.tail())
print(labels.tail())

model = model.Model(features, labels)
model.train()
model.comparePredictions()