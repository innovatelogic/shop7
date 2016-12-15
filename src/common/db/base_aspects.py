from types.types import Category

BASE_ASPECTS = 'base_aspects'

class BaseAspects():
    def __init__(self, instance):
        self.instance = instance
        pass
#----------------------------------------------------------------------------------------------
    def init(self):
        self.cat = self.instance.connection.db[BASE_ASPECTS]
        
#----------------------------------------------------------------------------------------------
    def clear(self, aspect):
        self.cat.update_one({'_id':aspect}, {'$set': {"categories" : []}})

#----------------------------------------------------------------------------------------------
    def add_category(self, aspect, category):
        self.cat.update_one({'_id':aspect}, {'$push': {"categories" : category.get()}})
        
#----------------------------------------------------------------------------------------------
    def get_root_category(self, aspect):
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