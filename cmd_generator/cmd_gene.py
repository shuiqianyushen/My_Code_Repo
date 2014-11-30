import sys,os,re
import yaml
#gene all tools build cmd

#because when the build command of uv4 is running, it will jump to project dir, so the log_file route must be given as abspath
uv4_log=os.path.abspath('.')+'//log//uv4build.log'
kds_log=' >> '+os.path.abspath('.')+'//log//kdsbuild.log'
armgcc_log='mingw32-make -j4 >> '+os.path.abspath('.')+'//log//armgccbuild.log'
atl_log=' >> '+os.path.abspath('.')+'//log//atlbuild.log'


#read the "./config/config.yml and get the lib to be builded!"
log_out_dict={'iar':' >> log//iarbuild.log','uv4':uv4_log,'kds':kds_log,'atl':atl_log,'armgcc':armgcc_log}


def build_lib_cmd_gene(ide_name,config,board_name,lib_name):
	#kds env variables
	#arm_path=
	f=open('./config/Path.yml','r')
	path_config=yaml.load(f)
	iar_path=path_config['iar']
	#iar_path=iar_path.replace("\\","//")
	kds_path=path_config['kds']
	kds_build = kds_path + "///eclipse///eclipsec.exe"
	kds_path=kds_path.replace("\\","//")
	kds_build=kds_build.replace("\\","//")
	#atl env variables
	atl_path=path_config['atl']
	atl_build=atl_path+"//ide//TrueSTUDIOc.exe"
	atl_build=atl_build.replace("\\","//")
	atl_path=atl_path.replace("\\","//")

	uv4_path=path_config['uv4']
	main_path=path_config['main_path']
	
	f.close()
	if ide_name=='iar':
		tmp_cmd="set path=%s; & " %(iar_path)+"iarbuild"+" "+main_path+"//lib//"+lib_name+"//"+ide_name+"//"+board_name+"//"+lib_name+".ewp"+" "+"-build"+" "+config+" "+"-log warnings"#+log_out_dict[ide_name]
		cmd=tmp_cmd.replace("\\","//")
		return cmd
	elif ide_name=='uv4':
		tmp_cmd="set path=%s; & " %(uv4_path)+"uv4"+ " -b "+main_path+"//lib//"+lib_name+"//"+"mdk"+"//"+board_name+"//"+lib_name+".uvproj"+" -j0 "+ " -o " + log_out_dict[ide_name]  + " -t " + "\"%s %s\"" % (lib_name,config)
		#
		cmd=tmp_cmd.replace("\\","//")
		
		return cmd
	elif ide_name=='kds':
		project_name="ksdk_platform_lib_"+board_name
		app_dir=main_path+"//lib//"+lib_name+"//"+ide_name+"//"+board_name
		tmp_ws="C:\Users\\"+"Kds//"+"\\workspace.kds"
		cmd = "set path=%s/bin;%s/toolchain/bin;" % (kds_path,kds_path) + "%SystemRoot%\system32;%SystemRoot% && " + "\"" + kds_build + "\" --launcher.suppressErrors -nosplash -application \"org.eclipse.cdt.managedbuilder.core.headlessbuild\" -cleanBuild \"" + project_name +"/" + config + "\" -import \"/" +  app_dir.replace('/','\\') +  "\" -data " + "\"" + tmp_ws + "\""
		
		return cmd
	elif ide_name=='atl':
		project_name="ksdk_platform_lib_"+board_name
		app_dir=main_path+"//lib//"+lib_name+"//"+ide_name+"//"+board_name
		tmp_ws='C:\Users\\Atl'+'\\TrueSTUDIO\ARM_workspace'
		cmd = "set path=%s/Tools;%s/ARMTools/bin;" % (atl_path,atl_path) + "%SystemRoot%\system32;%SystemRoot% && " + "\"" + atl_build + "\" --launcher.suppressErrors -nosplash -application \"org.eclipse.cdt.managedbuilder.core.headlessbuild\" -cleanBuild \"" + project_name +"/" + config + "\" -import \"/" +  app_dir.replace('/','\\') +  "\" -data " + "\"" + tmp_ws + "\""
		
		return cmd
	elif config=="Release":
		tmp_cmd='cd '+main_path+"//lib//"+lib_name+"//"+ide_name+'gcc'+"//"+board_name+" & build_all.bat"
		dele_pause_project=main_path+"//lib//"+lib_name+"//"+ide_name+'gcc'+"//"+board_name+"//build_all.bat"
		content = open(dele_pause_project).read().replace("pause","")
		#content=content.replace('mingw32-make -j4',armgcc_log)
		f = open(dele_pause_project,'w')
		f.write(content)
		f.close()
		cmd=tmp_cmd.replace("\\","//")
		
		return cmd
	else:
		dele_pause_project=main_path+"//lib//"+lib_name+"//"+ide_name+'gcc'+"//"+board_name+"//build_all.bat"
		content = open(dele_pause_project).read().replace("pause","")
		#content=content.replace(armgcc_log,'mingw32-make -j4')
		f = open(dele_pause_project,'w')
		f.write(content)
		f.close()
		f = open(dele_pause_project,'a')
		f.write('pause')
		f.close()
		cmd="echo reset "+board_name+" success"
		return cmd
def build_app_cmd_gene(ide_name,config,app_name,lib_name):
	f=open('./config/Path.yml','r')
	path_config=yaml.load(f)
	iar_path=path_config['iar']
	#iar_path=iar_path.replace("\\","//")
	kds_path=path_config['kds']
	#atl env variables
	atl_path=path_config['atl']
	atl_build=atl_path+"//ide//TrueSTUDIOc.exe"
	uv4_path=path_config['uv4']
	main_path=path_config['main_path']
	kds_build = kds_path + "//eclipse//eclipsec.exe"
	f.close()
	Flag=0
	judge_list=[]
	app_ide_path=main_path+"//demos//"+app_name
	judge_list=os.listdir(app_ide_path)
	#judge_list=judge_list.remove('src')
	for i in range(0,len(judge_list)):
		if judge_list[i]=='iar' or judge_list[i]=='uv4' or judge_list[i]=='kds' or judge_list[i]=='atl' or judge_list[i]=='armgcc':
			Flag=1
	if Flag:
		
		app_board_path=main_path+"//demos//"+app_name+'//iar'
		ide_list=os.listdir(app_ide_path)
		ide_list.remove('src')
		#get demos_to_board_map value
		pre_board_list_1=os.listdir(app_board_path)
		
		#get lib_to_board_map value
		f=open('./config/lib_board_map.yml')
		lib_board_map=yaml.load(f)
		f.close()
		board_list=[]
		pre_board_list_2=lib_board_map[lib_name]
		for pb1_num in range(0,len(pre_board_list_1)):
			for pb2_num in range(0,len(pre_board_list_2)):
				if pre_board_list_1[pb1_num]==pre_board_list_2[pb2_num]:
					board_list.append(pre_board_list_1[pb1_num])

		if ide_name=='iar':
			cmd_list=[]
			for i in range(0,len(board_list)):

				tmp_cmd="set path=%s; & " %(iar_path)+"iarbuild"+" "+main_path+"//demos//"+app_name+"//"+ide_name+"//"+board_list[i]+"//"+app_name+".ewp"+" "+"-build"+" "+config+" "+"-log warnings"#+log_out_dict[ide_name]
				cmd_list.append(tmp_cmd.replace("\\","//"))


		elif ide_name=='uv4':
			cmd_list=[]
			for i in range(0,len(board_list)):
				#change configuration make uv4 to create hex file
				app_path=main_path+"//demos//"+app_name+"//"+"mdk//"+board_list[i]+"//"+app_name+".uvproj"
				content = open(app_path).read().replace('<CreateHexFile>0</CreateHexFile>','<CreateHexFile>1</CreateHexFile>')
				f = open(app_path,'w+')
				f.write(content)
				f.close()
				tmp_cmd="set path=%s; & " %(uv4_path)+"uv4"+ " -b "+main_path+"//demos//"+app_name+"//"+"mdk//"+board_list[i]+"//"+app_name+".uvproj"+ " -j0 "+  " -t " + "\"%s %s\"" % (app_name,config)
				#" -o " + log_out_dict[ide_name] 
				cmd_list.append(tmp_cmd.replace("\\","//"))
			

		elif ide_name=='kds':
			cmd_list=[]
			for i in range(0,len(board_list)):
				project_name=app_name+"_"+board_list[i]

				app_dir=main_path+"//demos//"+app_name+"//"+ide_name+"//"+board_list[i]
				tmp_ws="C:\Users\\"+"//Kds"+"\\workspace.kds"
				cmd = "set path=%s/bin;%s/toolchain/bin;" % (kds_path,kds_path) + "%SystemRoot%\system32;%SystemRoot% && " + "\"" + kds_build + "\" --launcher.suppressErrors -nosplash -application \"org.eclipse.cdt.managedbuilder.core.headlessbuild\" -cleanBuild \"" + project_name +"/" + config + "\" -import \"/" +  app_dir.replace('/','\\') +  "\" -data " + "\"" + tmp_ws + "\""
				cmd_list.append(cmd)

		elif ide_name=='atl':
			cmd_list=[]
			for i in range(0,len(board_list)):
				project_name=app_name+"_"+board_list[i]
				app_dir=main_path+"//demos//"+app_name+"//"+ide_name+"//"+board_list[i]
				tmp_ws='C:\Users\Atl\\'+'TrueSTUDIO\ARM_workspace'
				cmd = "set path=%s/Tools;%s/ARMTools/bin;" % (atl_path,atl_path) + "%SystemRoot%\system32;%SystemRoot% && " + "\"" + atl_build + "\" --launcher.suppressErrors -nosplash -application \"org.eclipse.cdt.managedbuilder.core.headlessbuild\" -cleanBuild \"" + project_name +"/" + config + "\" -import \"/" +  app_dir.replace('/','\\') +  "\" -data " + "\"" + tmp_ws + "\""
				cmd_list.append(cmd)

		elif config=="Release":
			cmd_list=[]
			for i in range(0,len(board_list)):
				tmp_cmd='cd '+main_path+"//demos//"+app_name+"//"+ide_name+'gcc'+"//"+board_list[i]+" && build_all.bat"
				dele_pause_project=main_path+"//demos//"+app_name+"//"+ide_name+'gcc'+"//"+board_list[i]+"//build_all.bat"
				content = open(dele_pause_project).read().replace("pause","")
				#content=content.replace('mingw32-make -j4',armgcc_log)
				f = open(dele_pause_project,'w')
				f.write(content)
				f.close()
				cmd_list.append(tmp_cmd.replace("\\","//"))
				cmd_list.append(tmp_cmd.replace("\\","//"))
			

		else:
			cmd_list=[]
			for i in range(0,len(board_list)):
				dele_pause_project=main_path+"//demos//"+app_name+"//"+ide_name+'gcc'+"//"+board_list[i]+"//build_all.bat"
				#content = open(dele_pause_project).read().replace("pause","")
				#content=content.replace(armgcc_log,'mingw32-make -j4')
				#f = open(dele_pause_project,'w')
				#f.write(content)
				#f.close()
				f = open(dele_pause_project,'a')
				f.write('pause')
				f.close()
				cmd="echo reset"+board_list[i]+" success"
				cmd_list.append(cmd)

	else:
		cmd_list=[]
		
		pre_app_project_path=main_path+"//demos//"+app_name
		mid_app_list=os.listdir(pre_app_project_path)
		mid_app_list.remove('src')
		for i in range(0,len(mid_app_list)):
			#get demo_to_board_map value
			app_ide_path=pre_app_project_path+"//"+mid_app_list[i]
			ide_list=os.listdir(app_ide_path)
			app_project_path=pre_app_project_path+"//"+mid_app_list[i]+"//iar"
			
			pre_board_list_1=os.listdir(app_project_path)
			#get lib_to_board_map value
			f=open('./config/lib_board_map.yml')
			lib_board_map=yaml.load(f)
			f.close()
			board_list=[]
			pre_board_list_2=lib_board_map[lib_name]
			for pb1_num in range(0,len(pre_board_list_1)):
				for pb2_num in range(0,len(pre_board_list_2)):
					if pre_board_list_1[pb1_num]==pre_board_list_2[pb2_num]:
						board_list.append(pre_board_list_1[pb1_num])

			if ide_name=='iar':

				app_path='example'
				for j in range(0,len(board_list)):

					get_app_name_path=main_path+"//demos//"+app_name+"//"+mid_app_list[i]+"//"+ide_name+"//"+board_list[j]+"//"
					file_list=os.listdir(get_app_name_path)
					for num in range(0,len(file_list)):
						if re.search(r'ewd',file_list[num]):
							app_path=main_path+"//demos//"+app_name+"//"+mid_app_list[i]+"//"+ide_name+"//"+board_list[j]+"//"+file_list[num]
					
					tmp_cmd="set path=%s; & " %(iar_path)+"iarbuild"+" "+app_path+" "+"-build"+" "+config+" "+"-log warnings"
					cmd_list.append(tmp_cmd.replace("\\","//"))
					#+log_out_dict[ide_name]
		
			elif ide_name=='uv4':

				for j in range(0,len(board_list)):
					get_app_name_path=main_path+"//demos//"+app_name+"//"+mid_app_list[i]+"//"+"mdk"+"//"+board_list[j]+"//"
					file_list=os.listdir(get_app_name_path)
					for num in range(0,len(file_list)):
						if re.search(r'.uvproj',file_list[num]):
							app_path=main_path+"//demos//"+app_name+"//"+mid_app_list[i]+"//"+"mdk"+"//"+board_list[j]+"//"+file_list[num]
					
							content = open(app_path).read().replace('<CreateHexFile>0</CreateHexFile>','<CreateHexFile>1</CreateHexFile>')
			            	f = open(app_path,'w+')
			            	f.write(content)
			            	f.close()
					tmp_cmd="set path=%s; & " %(uv4_path)+"uv4"+ " -b "+app_path+ " -j0 "+  " -t " + "\"%s %s\"" % (app_name,config)
					#" -o " + log_out_dict[ide_name] 
					cmd_list.append(tmp_cmd.replace("\\","//"))
				
			elif ide_name=='kds':

				for  j in range(0,len(board_list)):
					project_name=app_name+"_"+board_list[j]

					app_dir=main_path+"//demos//"+app_name+"//"+mid_app_list[i]+"//"+ide_name+"//"+board_list[j]
					tmp_ws="C:\Users\\"+"//Kds"++"\\workspace.kds"
					cmd = "set path=%s/bin;%s/toolchain/bin;" % (kds_path,kds_path) + "%SystemRoot%\system32;%SystemRoot% && " + "\"" + kds_build + "\" --launcher.suppressErrors -nosplash -application \"org.eclipse.cdt.managedbuilder.core.headlessbuild\" -cleanBuild \"" + project_name +"/" + config + "\" -import \"/" +  app_dir.replace('/','\\') +  "\" -data " + "\"" + tmp_ws + "\""
					cmd_list.append(cmd)
			
			elif ide_name=='atl':

				for j in range(0,len(board_list)):
					project_name=app_name+"_"+board_list[j]
					app_dir=main_path+"//demos//"+app_name+"//"+mid_app_list[i]+"//"+ide_name+"//"+board_list[j]
					tmp_ws='C:\Users\Atl\\'+'\\TrueSTUDIO\ARM_workspace'
					cmd = "set path=%s/Tools;%s/ARMTools/bin;" % (atl_path,atl_path) + "%SystemRoot%\system32;%SystemRoot% && " + "\"" + atl_build + "\" --launcher.suppressErrors -nosplash -application \"org.eclipse.cdt.managedbuilder.core.headlessbuild\" -cleanBuild \"" + project_name +"/" + config + "\" -import \"/" +  app_dir.replace('/','\\') +  "\" -data " + "\"" + tmp_ws + "\""
					cmd_list.append(cmd)
			
			elif config=="Release":

				for j in range(0,len(board_list)):
					tmp_cmd='cd '+main_path+"//demos//"+app_name+"//"+mid_app_list[i]+"//"+ide_name+'gcc'+"//"+board_list[j]+" && build_all.bat"
					dele_pause_project=main_path+"//demos//"+app_name+"//"+mid_app_list[i]+"//"+ide_name+'gcc'+"//"+board_list[j]+"//build_all.bat"
					content = open(dele_pause_project).read().replace("pause","")
					#content=content.replace('mingw32-make -j4',armgcc_log)
					f = open(dele_pause_project,'w')
					f.write(content)
					f.close()
					cmd_list.append(tmp_cmd.replace("\\","//"))
					cmd_list.append(tmp_cmd.replace("\\","//"))
				
			
			else:

				for j in range(0,len(board_list)):
					dele_pause_project=main_path+"//demos//"+app_name+"//"+mid_app_list[i]+"//"+ide_name+'gcc'+"//"+board_list[j]+"//build_all.bat"
					#content = open(dele_pause_project).read().replace("pause","")
					#content=content.replace(armgcc_log,'mingw32-make -j4')
					#f = open(dele_pause_project,'w')
					#f.write(content)
					#f.close()
					f = open(dele_pause_project,'a')
					f.write('pause')
					f.close()
					cmd="Reset "+mid_app_list[i]+"_"+board_list[j]+" success"
					cmd_list.append(cmd)
	return cmd_list


		





	


