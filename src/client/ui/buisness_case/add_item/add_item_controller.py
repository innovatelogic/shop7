

class AddItemController():
	ZERO_PAGE = 0
	MAX_PAGE = 3
	def __init__(self, cases_controller):
		self.cases_controller = cases_controller
		self.__page = self.ZERO_PAGE

#----------------------------------------------------------------------------------------------
	def start(self):
		print('start')
		self.__page = self.ZERO_PAGE
		self.cases_controller.getView().addItemSetPage(self.__page)
		
#----------------------------------------------------------------------------------------------
	def finish(self, flag):
		print('finish {}'.format(flag))
		self.cases_controller.getView().addItemCancel()
		
#----------------------------------------------------------------------------------------------	
	def page(self):
		return self.__page
	
#----------------------------------------------------------------------------------------------
	def cancelAddItem(self):
		print('canelAddItem')
		self.finish(False)
		
#----------------------------------------------------------------------------------------------
	def prevStep(self):
		self.__page -= 1
		self.cases_controller.getView().addItemSetPage(self.__page)
		
#----------------------------------------------------------------------------------------------
	def nextStep(self):
		self.__page += 1
		
		if self.__page == self.MAX_PAGE:
			self.finish(True)
		else:
			self.cases_controller.getView().addItemSetPage(self.__page)

#----------------------------------------------------------------------------------------------
	def getPage(self):
		return self.__page