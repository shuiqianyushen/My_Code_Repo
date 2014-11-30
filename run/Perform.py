from threading import Thread, Condition
import sys
import yaml
from PyQt4 import QtCore, QtGui
import subprocess
import os

path_name=os.path.abspath('.')
path_cmd=os.path.join(path_name,'cmd_generator')
sys.path.append(path_cmd)

import cmd_gene
Run_Flag=1
if Run_Flag:
    f=open('./config/config.yml','r')
    config_info=yaml.load(f)
    ide_list=config_info['ide_list']
    app_list=config_info['app_list']
    build_list=config_info['build_list']
    board_list=config_info['board_list']
    lib_list=config_info['lib_list']
    f.close()

    f=open('./config/Path.yml','r')
    path_config=yaml.load(f)
    main_path=path_config['main_path']
    f.close()
    conf_list=["Release","Debug"]
    print "\n Library building!!!, Don't close\n"
    for lib in lib_list:
        for board in board_list:
            for target in conf_list:

                for ide in ide_list:

                    f=open('./config/pre_build_status.yml','r')
                    pre_build_status=yaml.load(f)
                    f.close()
                    if '1'==pre_build_status[lib][ide][target][board]:
                        print '%s %s %s have builded' %(ide,board,target)
                    else:
                        f=open('./config/pre_build_status.yml','w+')
                        pre_build_status[lib][ide][target][board]='1'
                        yaml.dump(pre_build_status,f)
                        f.close()
                        lib_cmd=cmd_gene.build_lib_cmd_gene(ide,target,board,lib)
                        print lib_cmd
                        print 'Begain building','\n'
                        #os.system(lib_cmd)
                        run_cmd=subprocess.Popen(args=lib_cmd,shell=True)
                        run_cmd.wait()
                        if 0==run_cmd.returncode:
                            f=open('./config/pre_build_status.yml','w+')
                            pre_build_status[lib][ide][target][board]='1'
                            yaml.dump(pre_build_status,f)
                            f.close()

    if 2==len(build_list):
        print "\n Demo building!!!,Don't close it \n"
        #build demos
        for i in range(0,len(app_list)):
            for lib_num in range(0,len(board_list)):

                for j in range(2):
                    for m in range(0,len(ide_list)):
                        cmd_list=[]
                        cmd_list=cmd_gene.build_app_cmd_gene(ide_list[m],conf_list[j],app_list[i],board_list[lib_num])
                        for n in range(0,len(cmd_list)):
                            os.system(cmd_list[n])
    print "\n============================Build have completed!!!====================\n"
