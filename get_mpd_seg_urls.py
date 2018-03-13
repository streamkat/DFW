# Keith Taylor -- DirecTV systems engineering and architecture group
# Usage: mpd_seg_check.py <Your DASH mpd url>

import sys
import time

import pprint
from io import BytesIO
from mpegdash.parser import MPEGDASHParser


gCount = 0
gSegments = { 'video': [], 'audio': [], 'text': []}

def main():

		
		url = sys.argv[1]
		url = url.rstrip()
		process_mpd(url)
		#pp.pprint(gSegments)
		#map(get_header,gSegments['video'])
		#map(get_header,gSegments['audio'])
		#map(get_header,gSegments['text'])
		
		

def process_mpd(url):
	global gSegments
	base_url = url.rstrip('manifest.mpd')
	pp = pprint.PrettyPrinter(indent=3)
	mpd = MPEGDASHParser.parse(url)
	Periods = mpd.periods
	for period in Periods:
		ad_sets = period.adaptation_sets
		for ad_set in ad_sets:
			mime_strs = ad_set.mime_type.split('/')
			mtype = mime_strs[0]
			if mtype == 'video':
				ext = 'm4v'
			elif mtype == 'audio':
				ext = 'm4a'
			elif mtype == 'text':
				ext = 'vtt'
					
			reps = ad_set.representations
			seg_templates = ad_set.segment_templates
			repr_ids = []
			for r in reps:
				repr_ids.append(r.id)
			for rid in repr_ids:	
				for st in seg_templates:					
					list = gen_playlist(st, r.id, ext, base_url)
					if mtype == 'video':
						gSegments['video'].extend(list)
					elif mtype == 'audio':
						gSegments['audio'].extend(list)
					elif mtype == 'text':
						gSegments['text'].extend(list)

					print("Type: {0}".format(mtype))
					pp.pprint(list)
					
					#time.sleep(2)
					#for seg in list:
					#	print("GET {0}".format(seg))
					#	get_header(seg)
								

def gen_playlist(seg_template, repr_id, as_ext, base_url):

	seg_list =[]
	stls = seg_template.segment_timelines
	for stl in stls:
		for tl in stl.Ss:
			timeline = 0
			timeline = tl.t + timeline
			seg_name = base_url + repr_id + "_Segment-" + str(timeline) +'.'+ as_ext
			seg_list.append(seg_name)
			if tl.r:
				i=1
				while( i <= tl.r): 
					timeline = timeline + tl.d
					seg_name = base_url + repr_id + "_Segment-" + str(timeline) + '.'+ as_ext
					seg_list.append(seg_name)
					i = i+1
						
	return seg_list	




if __name__ == '__main__':
	main()