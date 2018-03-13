#This script  takes a command line argument that is the name of a text file containing a list of m3u8 manifest urls
#The script will parse each manifest and its child manifests and perform a GET request for every video and audio segment
#The output is the header result of each GET, if anything other than 200 is returned "ERROR:" is prepended to the result
# Usage: hls_seg_check.py <list of urls file> > your.log
#Upon completion grep ERROR" your.log to check for errors...

# Keith Taylor -- DirecTV systems engineering and architecture group

import sys
import time
import m3u8
import pycurl
from io import BytesIO

gCount = 0

def main(): 
	global gCount
	delaySecs = 6
	if len(sys.argv) < 2:
		print( "Usage: hls_seg_check.py [list_urls_txt_file] [delay_in _seconds](optional)")
		return
	if len(sys.argv) == 3:
		delaySecs = float(sys.argv[2])
	with open(sys.argv[1]) as f:
		for url in f:
			url = url.rstrip()
			print(url)
			base_path = url.rstrip("index.m3u8") 
			m3u8_obj = m3u8.load(url)
			for v_playlist in m3u8_obj.playlists:
				print("Bitrate:{0}    Playlist      {1}".format( v_playlist.stream_info.bandwidth, v_playlist.uri))
				fm3u8 = base_path + v_playlist.uri
				fm_obj = m3u8.load(fm3u8)
				time.sleep(delaySecs)
				seg_count = 0
				for s in  fm_obj.segments:
					seg_url = base_path + s.uri 
					print("GET {0}".format(seg_url))
					get_header(seg_url)
					#get_segment(seg_url)
					#if seg_count == 10:
					#	break
					seg_count = seg_count + 1
					gCount = 0						
							
		
def get_header(url): 
 
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
	
def get_segment(url): 

	buffer = BytesIO()
	c = pycurl.Curl()
	# set the URL
	c.setopt(c.URL, url) 
	c.setopt(c.USERAGENT, 'My big fat VOD adventure crawler -- kt456@att.com 770-617-4679')
	# Set our header function.
	c.setopt(c.HEADERFUNCTION, header_function)
	# set header only
	#c.setopt(c.NOBODY, True)
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