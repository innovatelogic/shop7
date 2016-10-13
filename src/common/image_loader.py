import os, io, json, time
import urllib
import shutil

class ImageURLLoader():
	''' loads image files by url from specified json file '''
	def __init__(self, filename, out_folder):
		self.filename = filename
		self.out_folder = out_folder
		self.mapping = {}
		self.num_images = 0
	
	def run(self):
		
		self.mapping = {}
		self.num_images = 0
		
		timestr = time.strftime("%Y%m%d-%H%M%S")
		
		self.loadItems(self.filename)
		
		number = 0
		print("image store folder {}".format(self.out_folder))
		
		if not os.path.exists(self.out_folder):
			os.makedirs(self.out_folder)
			print('create folder {}'.format(self.out_folder))
		else:
			print('img output folder exist rename')
			old_folder = self.out_folder + '/_ren_' + timestr
			os.rename(self.out_folder, old_folder)
			print('folder {} renamed to {}'.format(self.out_folder, old_folder))
			os.makedirs(self.out_folder)
			print('create folder {}'.format(self.out_folder))
		
		for key, value in self.mapping.iteritems():
			resource_folder = self.out_folder + '/' + str(key)
			print('create item folder {}'.format(resource_folder))
			os.makedirs(resource_folder)
			n = 0
			for val in value:
				if not val:
					print('format error in {}'.format(key))
					continue
				
				try:
					urllib.urlretrieve(val, resource_folder + '/' + str(n) + '.jpeg')
					print("loaded {}".format(val))
					n += 1
					number+=1
				except URLError, e:
					print('exception {} file {} not found. moving on...'.format(e, val))

		
		print('[ImageURLLoader::run] loaded {} from {} images'.format(number, self.num_images))
	
	def loadItems(self, filename):
		print ('opening image mapping file:' + filename)
		with io.open(filename, 'r', encoding="utf8") as f:
			print 'opening OK'
			for line in f:
				row = json.loads(line)
				refs = row['refs'].split(',')
				self.num_images += len(refs)
				self.mapping[row['id']] = refs 