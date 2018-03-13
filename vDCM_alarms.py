# This parses a vDCM alarms log to reasonably readable output, tab delimited.
import csv
import sys
#import pprint

def main():

	f = open(sys.argv[1], 'rt')
	#p = pprint.PrettyPrinter(indent=3)
	reader = csv.reader(f,dialect='excel')
	#sreader = sorted(reader, key= lambda item : item[12])
	
	ch_count = 0
	for row in reader:
		#print len(row)
		if len(row) != 21:
			continue
		dtime = row[5].rstrip("\"")
		dtime = dtime.lstrip("\"")
		dta = dtime.split("T")
		ymd = dta[0].lstrip("\"time: \"")	
		timestamp = dta[1]
		timestamp = timestamp.rstrip("-0800")
		
		gp = row[12].lstrip("TS " )
		gp = gp.rstrip("\"")
		gpa = gp.split(":")
		grp = gpa[0]
		prt = gpa[1]
		
		sa = row[20].split(";")
		ssm_src = sa[1]
		ssm_src = ssm_src.lstrip("Source IP=")
		ssm_src = ssm_src.rstrip("=")
		
		errmsg = row[17].lstrip("\"msg\": \"")
		errmsg = errmsg.rstrip("\"")
		
		alarmstat = row[19].lstrip("\"alarmstatus\": \"")
		alarmstat = alarmstat.rstrip("\"")
		
		print("{0}\t{1:16}\t{2:16}\t{3}\t{4:25}\t{5}\t{6}".format(ymd,timestamp,grp,prt,errmsg,alarmstat,ssm_src))
	f.close()
	  
		
if __name__ == '__main__':
	main()
