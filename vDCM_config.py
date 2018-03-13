# This parses a vDCM config csv..
import csv
import sys
import pprint

def main():
	
	if len(sys.argv) < 2:
		print("usage: vDCMconfig.py [config file name] ")  
		return
	f = open(sys.argv[1], 'rt')
	
	reader = csv.reader(f,dialect='excel', delimiter=';')
	#sreader = sorted(reader, key= lambda item : item[12])
	
	first_rr = True
	
	for row in reader:
	
		if row[0] == "routing" and len(row) == 22:
			if first_rr:
				first_rr = False
				print("{0:9}\t{1:1}\t{2:9}\t{3:1}\t{4:1}\t{5}".format("Input","Port", "Output","Port","Bitrate","Callsign")) 
				continue
			else:
				process_routing_rec(row)
		else:
			continue
	f.close()

def process_routing_rec(row):
	#p = pprint.PrettyPrinter(indent=3)
	#p.pprint(row)
	print( "{0}\t{1}\t{2}\t{3}\t{4}\t{5}".format(row[5],row[6],row[14],row[15],row[16],row[20]))

		
if __name__ == '__main__':
	main()
