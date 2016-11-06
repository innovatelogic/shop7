from types.types import Category

USER_ASPECTS = 'user_aspects'
CATEGORIES_NAME = "categories"

class UserAspects():
    def __init__(self, instance):
        self.instance = instance
        pass
    
    def init(self):
        self.cat = self.instance.connection.db[USER_ASPECTS]
        
    def clear(self, group_id):
        self.cat.update_one({'group_id':group_id}, {'$set': {CATEGORIES_NAME : []}})
        
    def add_aspect(self, aspect):
        self.cat.insert(aspect.get())
           
    def add_category(self, group_id, category):
        self.cat.update_one({'_id':aspect}, {'$push': {CATEGORIES_NAME : category.get()}})
        
    def get_root_category(self, group_id):
        data = self.cat.find_one({'_id':group_id}, { CATEGORIES_NAME: { '$elemMatch' :  {'name':'root'} } })
        
        if data and data.get('categories') and len(data[CATEGORIES_NAME]):
            return Category(data['categories'][0])
        return None
    
    def get_childs(self, group_id, parent):
        out = []
        
        if parent:
            pipeline = [
                {'$match': { '_id':group_id}},
                {'$unwind':'$categories'},
                {'$match': {"categories.parent_id":parent._id} },
                #{ "$group": {'categories':{ _id:'$_id'}}}
                ]
            
            cursor = self.cat.aggregate(pipeline)
            
            records = list(cursor)
            
            #records = self.cat.find({'_id':aspect}, { "categories": { '$elemMatch' : {'parent_id':parent._id} } })
            #print records
            for record in records:
                if record and record.get(CATEGORIES_NAME) and len(record[CATEGORIES_NAME]):
                    #print record['categories']
                    out.append(Category(record[CATEGORIES_NAME]))
                
        return out
    
    def drop(self):
        '''drop collection. rem in production'''
        self.cat.drop()