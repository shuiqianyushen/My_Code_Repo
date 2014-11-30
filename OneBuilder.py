import platform
import sys,os,re
import shutil
import yaml
import subprocess,time

#from OneBuild_Ui3 import Ui_MainWindows
import OneBuildUi
from PyQt4 import QtCore, QtGui
from printlog import printlog


#add system find path
path_name=os.path.abspath('.')
path_cmd=os.path.join(path_name,'cmd_generator')
path_Perform=os.path.join(path_name,'run')
sys.path.append(path_cmd)
sys.path.append(path_Perform)

import cmd_gene

#rm last time's choice
f=open('./config/config.yml')
rm_info=yaml.load(f);
rm_info['app_list']=[]
rm_info['build_list']=[]
rm_info['lib_list']=[]
rm_info['ide_list']=[]
f.close()
f=open('./config/config.yml','w+')
yaml.dump(rm_info,f)
f.close()

#get the ide path info to display
f=open('./config/Path.yml')
Path_display=yaml.load(f)
f.close()

#rm the log when new build task come
shutil.copyfile('log//empty.log','log//iarbuild.log')
shutil.copyfile('log//empty.log','log//armgccbuild.log')
shutil.copyfile('log//empty.log','log//atlbuild.log')
shutil.copyfile('log//empty.log','log//uv4build.log')
shutil.copyfile('log//empty.log','log//kdsbuild.log')

class One_Build_class(OneBuildUi.Ui_MainWindows):
	def __init__(self,parent = None):
		super(One_Build_class,self).__init__()
		self.run_cmd_process=None
		self.stop_flag=0
		self.run_flag=1
		self.run_cmd_process_pid=0
		self.trayIcon = QtGui.QSystemTrayIcon(self)
		self.trayIcon.setIcon(QtGui.QIcon("./icon/icon.jpg"))
		self.trayIcon.show()
		self.trayIcon.activated.connect(self.trayClick)

		self.menu= QtGui.QMenuBar(self)

		self.menu.setGeometry(QtCore.QRect(0, 0, 680, 23))
		self.menu.setObjectName("help")

		self.help=self.menu.addMenu('&help')
		self.helpAct = QtGui.QAction("OneBuild use help",self)
		self.helpAct.setShortcut("Ctrl+h")
		self.helpAct.whatsThis()
		QtCore.QObject.connect(self.helpAct,QtCore.SIGNAL("triggered()"),self.open_help_file)
		self.help.addAction(self.helpAct)

		self.about=self.menu.addMenu('&about')
		self.aboutAct=QtGui.QAction("about",self)
		self.aboutAct.setShortcut("Ctrl+a")
		self.aboutAct.whatsThis()
		QtCore.QObject.connect(self.aboutAct,QtCore.SIGNAL("triggered()"),self.show_about_message)
		self.about.addAction(self.aboutAct)

		self.step=0
		self.timer = QtCore.QBasicTimer()
		self.setupUi(self)
		self.Display_path()
		self.save_progress.hide()
		QtCore.QObject.connect(self.CaseBox, QtCore.SIGNAL("activated(QString)"), self.Itemadd_app)
		QtCore.QObject.connect(self.App_list, QtCore.SIGNAL("itemDoubleClicked(QListWidgetItem*)"), self.Itemdelete_app)

		QtCore.QObject.connect(self.BoardBox, QtCore.SIGNAL("activated(QString)"), self.Itemadd_lib)
		QtCore.QObject.connect(self.Board_list, QtCore.SIGNAL("itemDoubleClicked(QListWidgetItem*)"), self.Itemdelete_lib)

		QtCore.QObject.connect(self.Save , QtCore.SIGNAL("clicked()"), self.Check_Box_Status)
		QtCore.QObject.connect(self.Run , QtCore.SIGNAL("clicked()"), self.Run_Cmd)
		QtCore.QObject.connect(self.clean_pre_build_info, QtCore.SIGNAL("clicked()"), self.Clean_build_info)
		
		QtCore.QObject.connect(self.stop, QtCore.SIGNAL("clicked()"), self.Stop_run_cmd)

	def Stop_run_cmd(self):
		if self.stop_flag:
			print "need stop"
			os.kill(-self.run_cmd_process_pid,9)
			print "kill success!!!"
		else:
			print "don't need stop!!"
	
	def Clean_build_info(self):
		clean_dict={"ide_list":[],"lib_list":[],"board_list":[]}
		clean_flag=1
		if self.Select_Atl.checkState():
			clean_dict['ide_list'].append('atl')
		if self.Select_Iar.checkState():
			clean_dict['ide_list'].append('iar')
		if self.Select_Arm.checkState():
			clean_dict['ide_list'].append('arm')
		if self.Select_Uv4.checkState():
			clean_dict['ide_list'].append('uv4')
		if self.Select_Kds.checkState():
			clean_dict['ide_list'].append('kds')
		
		if self.Select_hal.checkState():
			clean_dict['lib_list'].append('ksdk_hal_lib')
		if self.Select_mqx.checkState():
			clean_dict['lib_list'].append('ksdk_mqx_lib')
		if self.Select_platform.checkState():
			clean_dict['lib_list'].append('ksdk_platform_lib')
		if self.Select_ucosii.checkState():
			clean_dict['lib_list'].append('ksdk_ucosii_lib')
		if self.Select_ucosiii.checkState():
			clean_dict['lib_list'].append('ksdk_ucosiii_lib')
		if self.Select_startup.checkState():
			clean_dict['lib_list'].append('ksdk_startup_lib')
		if self.Select_std.checkState():
			clean_dict['lib_list'].append('ksdk_std_lib')
		if self.Select_freertos.checkState():
			clean_dict['lib_list'].append('ksdk_freertos_lib')
		
		if self.Build_board_all.checkState():
			for i in range(0,len(lib_list)):
				clean_dict['board_list'].append(lib_list[i])
		else:
			num=self.Board_list.count()
	        for i in range(0,num):
				text=self.Board_list.item(i).text()
				text=str(text)
				clean_dict['board_list'].append(text)

		if 0==len(clean_dict['lib_list']) or 0==len(clean_dict['ide_list']) or 0==len(clean_dict['board_list']):
			clean_flag=0
			msg_box = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Waring", "if you wannt to clean build info, please select lib ,ide and board!!!")
			msg_box.setWindowIcon(QtGui.QIcon("./icon/icon.jpg"))
			msg_box.exec_()
			clean_flag=0
		if clean_flag:
			f=open('./config/pre_build_status.yml')
			pre_build_info_dict=yaml.load(f)
			f.close()
			for lib in clean_dict['lib_list']:
				for ide in clean_dict['ide_list']:
					for board in clean_dict['board_list']:
						pre_build_info_dict[lib][ide]['Debug'][board]=0
						pre_build_info_dict[lib][ide]['Release'][board]=0
			f=open('./config/pre_build_status.yml','w+')
			yaml.dump(pre_build_info_dict,f)
			f.close()			
			msg_box = QtGui.QMessageBox(QtGui.QMessageBox.Information, "information", "clean pre_build information success!!!")
			msg_box.setWindowIcon(QtGui.QIcon("./icon/icon.jpg"))
			msg_box.exec_()

	def trayClick(self,reason):

		if reason==QtGui.QSystemTrayIcon.DoubleClick:

			self.showNormal()
		else:
			pass
	def show_about_message(self):

		QtGui.QMessageBox.about(self, "About One Build",
		"""<b>One Builder</b> v 0.9.0
		<p>Copyright &copy; 2014 B52468,freescale.Ltd.
		All rights reserved.
		<p>This application can be used to perform
		build library and demo.
		<p>Python - Qt %s - PyQt on %s""" % (
		platform.python_version(),
		platform.system()))
	
	def open_help_file(self):
		os.system('notepad ./doc/help.txt')

	def Itemdelete_app(self):
	    row=self.App_list.currentRow()
	    self.App_list.takeItem(row)

	    list_item=[]
	    self.App_list.takeItem(row)
	def Itemadd_app(self):
	    text=self.CaseBox.currentText()
	    num=self.App_list.count()
	    list_item=[]
	    flag=1
	    for i in range(0,num):
	        list_item.append(self.App_list.item(i).text())
	        if list_item[i]==text:
	            flag=0
	    if flag:
	        self.App_list.addItem(text)
	def Itemdelete_lib(self):
	    row=self.Board_list.currentRow ()
	    self.Board_list.takeItem(row)

	    list_item=[]
	    self.Board_list.takeItem(row)
	def Itemadd_lib(self):
	    text=self.BoardBox.currentText()
	    num=self.Board_list.count()
	    list_item=[]
	    flag=1
	    for i in range(0,num):
	        list_item.append(self.Board_list.item(i).text())
	        #print list_item[i]
	        if list_item[i]==text:
	            flag=0
	    if flag:
	        self.Board_list.addItem(text)
	def Check_Box_Status(self):
			text=self.Atl_Path_line.text()
			self.run_flag=1
			board_list=['K02F12810','K22F51212','K24F25612','K60D10','K64F12','KL03Z4','KL46Z4','KV10Z7','KV30F12810','KV31F51212']
			conf_dict={'ide_list':[],'build_list':[],'app_list':[],'lib_list':[],'board_list':[]}
			if self.Build_Lib.checkState():
				conf_dict['build_list'].append('Lib')
			if self.Build_App.checkState():
				conf_dict['build_list'].append('App')
			if self.Select_Atl.checkState():
				conf_dict['ide_list'].append('atl')

			if self.Select_Iar.checkState():
				conf_dict['ide_list'].append('iar')

			if self.Select_Arm.checkState():
				conf_dict['ide_list'].append('arm')

			if self.Select_Uv4.checkState():
				conf_dict['ide_list'].append('uv4')

			if self.Select_Kds.checkState():
				conf_dict['ide_list'].append('kds')


			if self.Select_hal.checkState():
				conf_dict['lib_list'].append('ksdk_hal_lib')


			if self.Select_mqx.checkState():
				conf_dict['lib_list'].append('ksdk_mqx_lib')


			if self.Select_platform.checkState():
				conf_dict['lib_list'].append('ksdk_platform_lib')


			if self.Select_ucosii.checkState():

				conf_dict['lib_list'].append('ksdk_ucosii_lib')

			if self.Select_ucosiii.checkState():
				conf_dict['lib_list'].append('ksdk_ucosiii_lib')

			if self.Select_startup.checkState():
				conf_dict['lib_list'].append('ksdk_startup_lib')

			if self.Select_std.checkState():
				conf_dict['lib_list'].append('ksdk_std_lib')

			if self.Select_freertos.checkState():
				conf_dict['lib_list'].append('ksdk_freertos_lib')

			if self.Build_board_all.checkState():
				for board in board_list:
					conf_dict['board_list'].append(board)
			else:
				for i in range(0,self.Board_list.count()):
					text=self.Board_list.item(i).text()
					text=str(text)
					conf_dict['board_list'].append(text)

			num=self.App_list.count()
			for i in range(0,num):
				text=self.App_list.item(i).text()
				text=str(text)
				conf_dict['app_list'].append(text)

			if 0==len(conf_dict['lib_list']):
				msg_box = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Waring", "Please Select  Lib!")
				msg_box.setWindowIcon(QtGui.QIcon("./icon/icon.jpg"))
				msg_box.exec_()
				self.run_flag=0
		    
			elif  0==len(conf_dict['ide_list']):
				msg_box = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Waring", "Please Select IDE!")
				msg_box.setWindowIcon(QtGui.QIcon("./icon/icon.jpg"))
				msg_box.exec_()
				self.run_flag=0
			elif 0==self.Build_Lib.checkState():
				msg_box = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Waring", "Please Select Build library!")
				msg_box.setWindowIcon(QtGui.QIcon("./icon/icon.jpg"))
				msg_box.exec_()
				self.run_flag=0

			elif 0==len(conf_dict['board_list']) and 0==self.Build_board_all.checkState():
				msg_box = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Waring", "Please Select Board!")
				msg_box.setWindowIcon(QtGui.QIcon("./icon/icon.jpg"))
				msg_box.exec_()
				self.run_flag=0

			elif 1==len(conf_dict['build_list']):
				if 'App'==conf_dict['build_list'][0]:
					msg_box = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Waring", "Please Select Library!")
					msg_box.setWindowIcon(QtGui.QIcon("./icon/icon.jpg"))
					msg_box.exec_()
					self.run_flag=0
				if 0!=len(conf_dict['app_list']):
					msg_box = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Waring", "Please select App!")
					msg_box.setWindowIcon(QtGui.QIcon("./icon/icon.jpg"))
					msg_box.exec_()
					self.run_flag=0

			elif 0==len(conf_dict['app_list']) and 2==len(conf_dict['build_list']):
					msg_box = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Waring", "Please select demos to build!")
					msg_box.setWindowIcon(QtGui.QIcon("./icon/icon.jpg"))
					msg_box.exec_()
					self.run_flag=0
			if self.run_flag:
				f=open('./config/config.yml','w+')
				yaml.dump(conf_dict,f)
				f.close()
				self.Add_Path()
				self.Prograss_Timer()
				print "\n\n"
				print "====================configuration information==============="
				print "           lib_list  : %s"   % (conf_dict['lib_list'])
				print "           ide_list  : %s"   % (conf_dict['ide_list'])
				print "           build_list: %s"   % (conf_dict['build_list'])
				print "           board_list: %s"   % (conf_dict['board_list'])
				if len(conf_dict['app_list']):
					print "           app_list  : %s"   % (conf_dict['app_list'])
				print "============================================================"

	def Run_Cmd(self):
		self.run_cmd_process= subprocess.Popen("python ./run/Perform.py",creationflags = subprocess.CREATE_NEW_PROCESS_GROUP)
		self.run_cmd_process_pid=self.run_cmd_process
		self.stop_flag=1
	    
	def timerEvent(self,e):
	    if self.step >= 100:
	        self.save_progress.hide()
	        self.timer.stop()
	        self.step=0
	        return
	    self.step = self.step + 10
	    self.save_progress.setValue(self.step)
	    self.timer.start(100, self)

	def Prograss_Timer(self):
	    self.save_progress.show()
	    self.timer.start(100, self)

	def Add_Path(self):
	    Path_config={'atl':[],'kds':[],'arm':[],'iar':[],'uv4':[],'main_path':[]}
	    text=self.Atl_Path_line.text()
	    text=str(text)
	    Path_config['atl']=text
	    text=self.Kds_Path_line.text()
	    text=str(text)
	    Path_config['kds']=text
	    text=self.Arm_Path_line.text()
	    text=str(text)
	    Path_config['arm']=text
	    text=self.Iar_Path_line.text()
	    text=str(text)
	    Path_config['iar']=text
	    text=self.Uv4_Path_line.text()
	    text=str(text)
	    Path_config['uv4']=text
	    text=self.Main_Path_line.text()
	    text=str(text)
	    Path_config['main_path']=text
	    f=open('./config/Path.yml','w+')
	    yaml.dump(Path_config,f)
	    f.close()

	def Display_path(self):
	    self.Atl_Path_line.setText(Path_display['atl'])
	    self.Kds_Path_line.setText(Path_display['kds'])
	    self.Arm_Path_line.setText(Path_display['arm'])
	    self.Uv4_Path_line.setText(Path_display['uv4'])
	    self.Iar_Path_line.setText(Path_display['iar'])
	    self.Main_Path_line.setText(Path_display['main_path'])
  
app = QtGui.QApplication(sys.argv)
testui= One_Build_class()
testui.show()
sys.exit(app.exec_())
