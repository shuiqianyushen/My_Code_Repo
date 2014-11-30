import re,sys,os
demo_board_name={

	'K64F12':		['twrk64f120m' ,'frdmk64f120m' ],
	'K22F51212':	['twrk22f120m','frdmk22f120m' ],
    'K22F12810':	['twrk22f120m128r' ,],
    'K22F25612':	['twrk22f120m256r',],
    
    'KV31F51212':	['twrkv31f120m',],
    'KV31F12810':	['twrkv31f120m128r',],    
    'KV31F25612':	['twrkv31f120m256r',],    
    'K24F25612':	['twrk24f120m',],         
    'KL03Z4':		['frdmkl03z48m',],
    'KV30F12810':	['twrkv30f100m','twrkv30f100mk02','twrkv30f100mk0264'],
    'KL43Z4': 		['twrkl43z48m','frdmkl43z48m'],
    'K02F12810':	['frdmk22f120mk02','twrk22f120mk02'],
    'KV30F12810':	['twrkv31f120mkv30',]}
lib_list=demo_board_name.keys()

print lib_list

filed_dp_log=open('iarbuild.log','r')
if(filed_dp_log!=-1):
	print 'open success!'
lines_list=filed_dp_log.readlines()
for line in lines_list:
    for pattern in lib_list:
        match=re.match(pattern,line)
        if match!=None:
            print line



'''file_list=[]
for i in range(5):
	list_str=filed_dp_log.readline()
	list_str=list_str.strip()
	print list_str
	match=re.search(lib_list[0],list_str)
	if match!=None:
		print match.group(0)
	file_list.append(list_str)
print file_list'''