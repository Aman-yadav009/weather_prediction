import serial
import time
import joblib 
#from csv import reader
from math import sqrt
from math import exp
from math import pi
import string

def predict(summaries, row):
	probabilities = calculate_class_probabilities(summaries, row)
	best_label, best_prob = None, -1
	for class_value, probability in probabilities.items():
		if best_label is None or probability > best_prob:
			best_prob = probability
			best_label = class_value
	return best_label

def calculate_class_probabilities(summaries, row):
	total_rows = sum([summaries[label][0][2] for label in summaries])
	probabilities = dict()
	for class_value, class_summaries in summaries.items():
		probabilities[class_value] = summaries[class_value][0][2]/float(total_rows)
		for i in range(len(class_summaries)):
			mean, stdev, _ = class_summaries[i]
			probabilities[class_value] *= calculate_probability(row[i], mean, stdev)
	return probabilities

# Calculate the mean of a list of numbers
def mean(numbers):
	return sum(numbers)/float(len(numbers))

# Calculate the standard deviation of a list of numbers
def stdev(numbers):
	avg = mean(numbers)
	if(float(len(numbers)-1) <= 0):
		return 0
	variance = sum([(x-avg)**2 for x in numbers]) / float(len(numbers)-1)
	return sqrt(variance)
def calculate_probability(x, mean, stdev):
	if(stdev == 0):
		return 0
	exponent = exp(-((x-mean)**2 / (2 * stdev**2 )))
	return (1 / (sqrt(2 * pi) * stdev)) * exponent
# Save the model as a pickle in a file 
#joblib.dump(knn, 'filename.pkl') 
  
# Load the model from the file 
model = joblib.load('weather.pkl')  
  
# Use the loaded model to make predictions 
#row = [8.28888888888889,0.83,1016.41]
# predict the label
#label = predict(model, row)
#print('Data=%s, Predicted: %s' % (row, label))


arduino = serial.Serial("/dev/ttyUSB0", 115200)
arduino.write('w'.encode())
b = arduino.readline()
str_rn = b.decode()
str1 = str_rn.rstrip()
my_list = []
my_list_f = []
my_list = str1.split()
for i in range(len(my_list)):
	my_list_f.append(float(my_list[i]))
#print (my_list_f)
t_w = []
t_w.append(my_list_f[2])
t_w.append(my_list_f[1])
t_w.append(my_list_f[0])
print(t_w)
label = predict(model, t_w)
print('Data=%s, Predicted: %s' % (t_w, label))