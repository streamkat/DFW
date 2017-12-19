

import sys
import time
import pycurl
import pprint
from io import BytesIO
from mpegdash.parser import MPEGDASHParser
import pycurl
from io import BytesIO


gCount = 0
gSegments = { 'video': [], 'audio': [], 'text': []}

def main():

		#pp = pprint.PrettyPrinter(indent=3)
		url = sys.argv[1]
		url = url.rstrip()
		process_mpd(url)
		#pp.pprint(gSegments)
		map(get_header,gSegments['video'])
		map(get_header,gSegments['audio'])
		map(get_header,gSegments['text'])
		
		

def process_mpd(url):
	global gSegments
	base_url = url.rstrip('manifest.mpd')
	
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

					#print("Type: {0}".format(mtype))
					#pp.pprint(list)
					
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

def get_header(url):
 
	print("GET {0}".format(url))
	c = pycurl.Curl()
	# set the URL
	c.setopt(c.URL, url) 
	c.setopt(c.USERAGENT, 'My big fat segment crawler -- kt456@att.com 770-617-4679')
	# Set our header function.
	c.setopt(c.HEADERFUNCTION, header_function)
	# set header only
	c.setopt(c.NOBODY, True)
	#c.setopt(c.WRITEDATA, buffer)
	c.perform()
	c.close()
	#count = count + 1
	#body = buffer.getvalue()
	#print(body)
	#print gCount
	gCount = 0
	
def get_segment(url): 

	buffer = BytesIO()
	c = pycurl.Curl()
	# set the URL
	c.setopt(c.URL, url) 
	c.setopt(c.USERAGENT, 'My big fat segment crawler -- kt456y@att.com 770-617-4679')
	# Set our header function.
	c.setopt(c.HEADERFUNCTION, header_function)
	c.setopt(c.WRITEDATA, buffer)
	c.perform()
	c.close()
	#count = count + 1
	body = buffer.getvalue()
	return
	
def header_function(header_line):
  # HTTP standard specifies that headers are encoded in iso-8859-1.
  # On Python 2, decoding step can be skipped.
  # On Python 3, decoding step is required.
  global gCount
   
  gCount = gCount + 1
    
  header_line = header_line.decode('iso-8859-1')  
  header_line = header_line.replace('\r', '');    # remove '\r'
  header_line = header_line.replace('\n', '');    # remove '\n'
  if gCount == 1:
	if header_line != "HTTP/1.1 200 OK":
		print( "ERROR: {0}".format(header_line))
		
  print(header_line)

  # Header lines include the first status line (HTTP/1.x ...).
  # We are going to ignore all lines that don't have a colon in them.
  # This will botch headers that are split on multiple lines...
  if ':' not in header_line:
    return	
	


if __name__ == '__main__':
	main()