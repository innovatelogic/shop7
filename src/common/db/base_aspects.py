from types.category import Category

BASE_ASPECTS = 'base_aspects'

class BaseAspects():
    def __init__(self, instance):
        self.instance = instance
        pass
#----------------------------------------------------------------------------------------------
    def init(self):
        print("BaseAspects init:" + BASE_ASPECTS)
        self.cat = self.instance.connection.db[BASE_ASPECTS]
        
#----------------------------------------------------------------------------------------------
    def clear(self, aspect):
        self.cat.update_one({'_id':aspect}, {'$set': {"categories" : []}})

#----------------------------------------------------------------------------------------------
    def removeAspect(self, aspect_name):
        '''
        @param aspect_name: used as id
        @return True if removed otherwise False 
         '''
        out = False
        if aspect_name:
            self.cat.remove({"_id":aspect_name})
            out = True
        return out
    
#----------------------------------------------------------------------------------------------
    def isAspectExist(self, aspect):
        cursor = self.cat.find({ '_id': aspect}).limit(1)
        return cursor.count() > 0
        
#----------------------------------------------------------------------------------------------
    def add_category(self, aspect, category):
        updateResult = self.cat.update_one({'_id':aspect}, {'$push': {"categories" : category.get()}})
        #print updateResult.acknowledged
        
#----------------------------------------------------------------------------------------------
    def updateCategory(self, aspect, category):
        updateResult = self.cat.update_one(
            {'_id':aspect, "categories._id":category._id},
            {'$set': {"categories.$.local" : category.local,
                      'categories.$.foreign_id':category.foreign_id,
                      'categories.$.controller':category.controller}}
            )
    
#----------------------------------------------------------------------------------------------
    def setDefaultCategoryName(self, aspect, name):
        self.cat.update_one({'_id':aspect}, {'$set': {"default" : name}})
        
#----------------------------------------------------------------------------------------------
    def getDefaultCategoryName(self, aspect_id):
        out = ''
        data = self.cat.find_one({'_id':aspect_id})
        if 'default' in data:
            out = data['default']
        return out

 #----------------------------------------------------------------------------------------------
    def remove_category(self, aspect, category_id):
        self.cat.update({'_id':aspect}, {'$pull': {"categories" : {'_id':category_id}}})
        
#----------------------------------------------------------------------------------------------
    def get_root_category(self, aspect):
        ''' get root category node. None if not exist '''
        data = self.cat.find_one({'_id':aspect}, { "categories": { '$elemMatch' :  {'name':'root'} } })
        
        if data and data.get('categories') and len(data['categories']):
            return Category(data['categories'][0])
        return None

#----------------------------------------------------------------------------------------------
    def get_childs(self, aspect, parent):
        out = []
        if parent:
            
            pipeline = [
                {'$match': { '_id':aspect}},
                {'$unwind':'$categories'},
                {'$match': {"categories.parent_id":parent._id} },
                #{ "$group": {'categories':{ _id:'$_id'}}}
                ]
            
            cursor = self.cat.aggregate(pipeline)
            
            records = list(cursor)
            
            #records = self.cat.find({'_id':aspect}, { "categories": { '$elemMatch' : {'parent_id':parent._id} } })
            #print records
            for record in records:
                if record and record.get('categories') and len(record['categories']):
                    #print record['categories']
                    out.append(Category(record['categories']))
                    
        return out

#----------------------------------------------------------------------------------------------
    def drop(self):
        '''drop collection. rem in production'''
        self.cat.drop()