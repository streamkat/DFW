
import sys
import m3u8
import pycurl

def main(): 
	count = 0
	with open(sys.argv[1]) as f:
		for url in f:
			url = url.rstrip()
			print(url)
			base_path = url.rstrip("index.m3u8") 
			m3u8_obj = m3u8.load(url)
			for iframe_playlist in m3u8_obj.iframe_playlists:
				print("{0} {1}".format( iframe_playlist.iframe_stream_info.bandwidth, iframe_playlist.uri))
				ifm3u8 = base_path + iframe_playlist.uri
				iFrame_obj = m3u8.load(ifm3u8)
				for s in  iFrame_obj.segments:
					seg_url = base_path + s.uri 
					print("GET {0}".format(seg_url))
					get_header(seg_url)
		
		
		
def get_header(url): 
 
	c = pycurl.Curl()
	# set the URL
	c.setopt(c.URL, url) 
	
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

 
def header_function(header_line):
  # HTTP standard specifies that headers are encoded in iso-8859-1.
  # On Python 2, decoding step can be skipped.
  # On Python 3, decoding step is required.
  header_line = header_line.decode('iso-8859-1')  
  header_line = header_line.replace('\r', '');    # remove '\r'
  header_line = header_line.replace('\n', '');    # remove '\n'
  print(header_line)

  # Header lines include the first status line (HTTP/1.x ...).
  # We are going to ignore all lines that don't have a colon in them.
  # This will botch headers that are split on multiple lines...
  if ':' not in header_line:
    return
if __name__ == '__main__':
	main()