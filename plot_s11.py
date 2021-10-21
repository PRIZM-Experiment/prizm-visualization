from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import glob, os
import argparse

def plot_s11(file_directory, output):
	"""
	Makes a joy division/Alan Rogers Style plot of S11 measurements as they are accumulated over time.


	"""
	seperation_scale = 0.5

	waterfall_ew = load_all_data(file_directory, polarisation="EW")
	waterfall_ns = load_all_data(file_directory, polarisation="NS")
	measurement_dates = waterfall_ew.columns.values[1:]
	n_measurements = len(measurement_dates)

	fig, (ax1, ax2) = plt.subplots(figsize =(10,5) ,ncols=2, sharey=True)

	ax1.set_title("EW")
	ax2.set_title("NS")

	#Compute scaled min/max of data that determines the offset between each S11 measurement.
	dynamic_range = seperation_scale * abs(waterfall_ew.iloc[:, 1:].max() - waterfall_ew.iloc[:, 1:].min()).mean()

	for i in range(n_measurements):
		sns.lineplot(x=waterfall_ew['Freq. [Hz]']/1e6, y=waterfall_ew.iloc[:, i + 1] + i * dynamic_range, ax=ax1)
		sns.lineplot(x=waterfall_ns['Freq. [Hz]']/1e6, y=waterfall_ns.iloc[:, i + 1] + i * dynamic_range, ax=ax2)

	ax2.set_yticks(np.arange(0, n_measurements) * dynamic_range)
	ax2.set_yticklabels(measurement_dates)
	ax1.set(ylabel=None)
	ax1.set_xlabel("Frequency [MHz]")
	ax2.set_xlabel("Frequency [MHz]")

	plt.savefig(output)

	return



def find_data_start(filename, lookup="\n", encoding="ISO-8859-1"):
	
	"""
	This function reads a .txt file and returns where it finds the first
	newline. It was built to scan Nivek's measurement outputs and figure
	out where the data actually starts and ignore all the metadata
	
	parameters
	-----------
	filename: str
		path to text file
	
	lookup: str
		string that marks end of metadata
	
	encoding: str
		type of encoding (utf-8, etc.)
	
	"""
	with open(filename, encoding=encoding) as myFile:
		for num, line in enumerate(myFile, 1):
			if lookup ==line:
				return num

def load_all_data(file_directory, polarisation="EW", encoding="ISO-8859-1", delimiter="\t", decimal=',' ):
	
	"""
	Takes all the data from a particular polarisation and combines all
	measurements for different dates and puts this in a pandas dataframe
	
	NOTE: this assumes every time we measure the same frequency channels
	"""
	
	#get a list of all the files for a particular polarisation and sort
	#by date
	run_path = os.getcwd()
	os.chdir(file_directory)
	file_names = sorted(glob.glob("*"+polarisation+".txt"))
	os.chdir(run_path)

	n_measurements = len(file_names)
	start = find_data_start(file_directory + file_names[0])
	test = pd.read_csv(file_directory + file_names[0], encoding=encoding, skiprows=start, delimiter=delimiter,
						   decimal=decimal)

	#Create a new pandas dataframe that will hold all measurements
	waterfall = test[['Freq. [Hz]']].copy()
	for i in range(n_measurements):
		start = find_data_start(file_directory + file_names[i])
		s11_data = pd.read_csv(file_directory + file_names[i] , encoding=encoding, skiprows=start, delimiter=delimiter,
									decimal=decimal)

		#get date by reading the first 10 chars from filename string
		date = file_names[i][:10]
		try:
			waterfall[date] = s11_data["Magnitude [dB]"].values
		except Exception as e:
			print(e)
			print("Couldn't process",file_names[i])

	return waterfall
	

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Plot all S11 measurements')
	parser.add_argument('-input', dest='path', type=str, help='folder path as str, i.e "/home/data" ', required=True)
	parser.add_argument('-output', dest='output', type=str, help='output file path, extension will define the output '
																 'format, "home/analysis/result.pdf" ', required=True)

	args = parser.parse_args()
	plot_s11(args.path,args.output)