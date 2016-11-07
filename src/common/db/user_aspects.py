from types.types import Category, UserAspect
from bson.objectid import ObjectId

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
        
    def get_aspect(self, _id):
        data = self.cat.find_one({'_id':ObjectId(_id)})
        if data:
            category_root = self.get_root_category(ObjectId(_id))
            node_root = UserAspect.Node(category_root)
            
            stack = []
            stack.append(node_root)
            
            while (len(stack) > 0):
                top = stack.pop(0)
                
                childs = self.get_childs(ObjectId(_id), top.category)

                for child in childs:
                    node = UserAspect.Node(child)
                    top.childs.append(node)
                    stack.insert(0, node) 
            
            return UserAspect({'_id':data['_id'], 'group_id':data['group_id'], 'node_root':node_root})
        return None
        
    def add_aspect(self, aspect):
        self.cat.insert(aspect.get())
           
    def add_category(self, _id, category):
        self.cat.update_one({'_id':aspect}, {'$push': {CATEGORIES_NAME : category.get()}})
        
    def get_root_category(self, _id):
        data = self.cat.find_one({'_id':_id}, { CATEGORIES_NAME: { '$elemMatch' :  {'name':'root'} } })
        
        if data and data.get('categories') and len(data[CATEGORIES_NAME]):
            return Category(data['categories'][0])
        return None
    
    def get_childs(self, _id, parent):
        out = []
        
        if parent:
            pipeline = [
                {'$match': { '_id':_id}},
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