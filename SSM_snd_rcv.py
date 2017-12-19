#! /usr/bin/python

import getopt
import socket
import sys

if not hasattr(socket, 'IP_MULTICAST_TTL'):
  setattr(socket, 'IP_MULTICAST_TTL', 33)
if not hasattr(socket, 'IP_ADD_SOURCE_MEMBERSHIP'):
  setattr(socket, 'IP_ADD_SOURCE_MEMBERSHIP', 39)

if sys.argv[1] == 'send':
  opts, args = getopt.getopt(sys.argv[2:], 't:s:g:p:')
  opts = dict(opts)

  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
  if '-t' in opts:
    s.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_TTL, chr(int(opts['-t'])))
  if '-s' in opts:
    s.bind((opts['-s'], 0))
  s.connect((opts['-g'], int(opts['-p'])))
  print 'READY.'
  while True:
    s.send(sys.stdin.readline())

elif sys.argv[1] == 'recv':
  opts, args = getopt.getopt(sys.argv[2:], 'g:i:s:p:')
  opts = dict(opts)
  opts.setdefault('-i', '0.0.0.0')

  imr = (socket.inet_pton(socket.AF_INET, opts['-g']) +
         socket.inet_pton(socket.AF_INET, opts['-i']) +
         socket.inet_pton(socket.AF_INET, opts['-s']))

  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
  s.setsockopt(socket.SOL_IP, socket.IP_ADD_SOURCE_MEMBERSHIP, imr)
  s.bind((opts['-g'], int(opts['-p'])))
  print 'READY.'
  while True:
    print repr(s.recvfrom(4096))
