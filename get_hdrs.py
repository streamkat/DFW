import os
import pycurl
import sys
#from StringIO import StringIO




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
	count = count + 1
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
