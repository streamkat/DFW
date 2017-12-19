


import sys
import time
import pycurl
import inspect
import pprint

from io import BytesIO
from mpegdash.parser import MPEGDASHParser

def main():
	pp = pprint.PrettyPrinter(indent=3)
	mpd_url = sys.argv[1]
	mpd = MPEGDASHParser.parse(mpd_url)
	#for name, data in inspect.getmembers(MPEGDASHParser):
	#	if name == '__builtins__':
	#		continue
	#	print '%s :' % name, repr(data)
	
	print "MPD:"
	pp.pprint( mpd.__dict__)
	pObj = mpd.periods
	pp.pprint(pObj[0].__dict__)
	asets = pObj[0].adaptation_sets
	
	print("\n\n{0} Adaptation Sets :\n").format(len(asets)) 
	
	#pp.pprint( asets[0].__dict__)
	#pp.pprint(asets[0].representations[0].__dict__)
	
	for aset in asets:
		print "\nAdaptation Set:"
		pp.pprint( aset.__dict__)
		reps = aset.representations
		sts = aset.segment_templates
		cps = aset.content_protections
		ies = aset.inband_event_streams
		if ies:
			print "\nInband event:"
			for ie in ies:
				print("	scheme_id_uri:{0} value: {1} id: {2}".format(ie.scheme_id_uri, ie.value, ie.id))  
		if cps:
			print "\nContent protection Info:"
			for cp in cps:
				print(" 	uri:{0} value:{1} id:{2}".format(cp.scheme_id_uri,cp.value, cp.id))
		for r in reps:
			print "\nBitrate Representation"
			pp.pprint(r.__dict__) 
		for st in sts:
			print "\nSegment Template"
			pp.pprint(st.__dict__)
			stls = st.segment_timelines
			for stl in stls:
				print "\ntimeline"
				for tl in stl.Ss:
					print("t ={0}, d = {1}  r = {2}".format(tl.t, tl.d, tl.r))
				
				
			#for name, data in inspect.getmembers(stl):
			#	if name == '__builtins__':
			#		 continue
			#	print(" {0} : {1}".format(name,data))
	
	
if __name__ == '__main__':
	main()