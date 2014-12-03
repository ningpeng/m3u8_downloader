#!/usr/bin/python

import m3u8
from urllib import urlopen
from sys import argv 
import time


if len(argv) <4 :
	print "usage :%s <m3u8_url> <saved_tsfile> <duration>" , argv[0]
	quit()

ts_file =  open(argv[2], "wb")

retrive_seq = -1 
Err_flag = False

duration = int(argv[3])
if duration <= 0:
	duration = 3600*72
end_time = time.time() + duration


while time.time() < end_time and not Err_flag :

	m3u8_obj = m3u8.load(argv[1])

	new_seg_flag = False
	print time.strftime('%Y-%m-%d %H:%M:%S ',time.localtime(time.time())) , "#EXT-X-MEDIA-SEQUENCE:", m3u8_obj.media_sequence
	
	seg_seq = m3u8_obj.media_sequence

	for seg in  m3u8_obj.segments:
	
		if m3u8.is_url(seg.uri) :
			segurl = seg.uri
		else :
			segurl =  m3u8.model._urijoin( seg.base_uri ,  seg.uri )
	

		if seg_seq > retrive_seq :
			if retrive_seq>=0 and seg_seq<>retrive_seq+1 :
				print "WARN: SEQ not continue!!!! %d - %d" , retrive_seq , seg_seq 

			retrive_seq = seg_seq		
			new_seg_flag = True

			#print segurl

			start_ts = time.time()
			
			resp = urlopen(segurl)
			if resp.getcode()!=200 :
				print "Error HTTP resp code:" , resp.getcode(), segurl
	        		Err_flag = True
				break	

			doc = resp.read()
			resp.close()

			end_ts  = time.time()
			size = len(doc)
                	dur = end_ts-start_ts
	
			if dur > 8 :
                        	print "Error TOO SLOW!!!!! " ,  dur, size , size*8/dur/1024,  " - ", segurl 
                	else:
                    		print dur, size , size*8/dur/1024,  " - ", segurl

			ts_file.write(doc)     
		
		seg_seq = seg_seq + 1
		
	if m3u8_obj.is_endlist:
		break;
	elif not new_seg_flag :
		time.sleep(5) 
	 	print "sleep 5s..." 


ts_file.close()
