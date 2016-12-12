

class AddItemController():
	def __init__(self, cases_controller):
		self.cases_controller = cases_controller
		self.__page = 0

#----------------------------------------------------------------------------------------------
	def start(self):
		print('start')
		self.__page = 0
		self.cases_controller.getView().addItemSetPage(self.__page)
		
#----------------------------------------------------------------------------------------------
	def finish(self, flag):
		print('finish {}'.format(flag))

#----------------------------------------------------------------------------------------------	
	def page(self):
		return self.__page
	
#----------------------------------------------------------------------------------------------
	def cancelAddItem(self):
		print('canelAddItem')
		self.cases_controller.getView().addItemCancel()
		self.finish(False)
		
#----------------------------------------------------------------------------------------------
	def prevStep(self):
		print('prevStep')
		self.__page -= 1
		self.cases_controller.getView().addItemSetPage(self.__page)
		
#----------------------------------------------------------------------------------------------
	def nextStep(self):
		print('nextStep')
		self.__page += 1
		self.cases_controller.getView().addItemSetPage(self.__page)
		
#----------------------------------------------------------------------------------------------
	def getPage(self):
		return self.page