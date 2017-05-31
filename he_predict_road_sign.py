from numpy import genfromtxt, concatenate
from sklearn import svm
import csv


training_data_file = "train.csv"
test_data_file = "test.csv"
output_file = "output.csv"

directionsMap = {"Front": 0, "Left": 1, "Rear": 2, "Right": 3 }
directions = ["Front", "Left", "Rear", "Right"] # For reverse
# Preprocess data
def getLabels(arrayDirections):
	res = [directions[ele] for ele in arrayDirections]
	return res

def convertDirection(direction):
	return directionsMap[direction]

train_csv_tups = genfromtxt(training_data_file, \
				delimiter=',', \
				dtype=None, \
				skip_header=1, \
				usecols=(1, 2, 3, 6), \
				converters={1: convertDirection, 6: convertDirection})
# Discard height/width since ratio is present

train_d = train_csv_tups.tolist()
features_train = [list(x)[0:3] for x in train_d]
labels_train = [list(x)[3] for x in train_d]

test_csv_tups = genfromtxt(test_data_file, \
				delimiter=",", \
				dtype=None, \
				skip_header=1, \
				usecols=(0, 1, 2, 3),\
				converters={1:convertDirection})
				
test_d = test_csv_tups.tolist()
features_test = [list(x)[1:] for x in test_d]
ids = [list(x)[0] for x in test_d]

# Train classifier and predict probabilities
classifier = svm.SVC(probability=True, kernel='linear')

print("Training...")
classifier.fit(features_train, labels_train)
print("Finished training.")

print("Predicting...")
prediction = classifier.predict_proba(features_test)
print("Finished predicting.")

output = prediction.tolist()
for i in range(len(prediction)):
	output[i].insert(0, ids[i])
	print(output[i])

with open(output_file, 'wb') as fp:
	w = csv.writer(fp)
	header = ["Id"] + getLabels(classifier.classes_)
	w.writerow(header)
	w.writerows(output)

