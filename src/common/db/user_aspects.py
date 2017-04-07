from types.types import UserAspect
from types.category import Category
from bson.objectid import ObjectId

USER_ASPECTS = 'user_aspects'
CATEGORIES_NAME = "categories"

#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
class UserAspects():
    def __init__(self, instance):
        self.instance = instance
        pass
    
#----------------------------------------------------------------------------------------------
    def init(self):
        self.cat = self.instance.connection.db[USER_ASPECTS]
        
#----------------------------------------------------------------------------------------------
    def clear(self, group_id):
        self.cat.update_one({'group_id':group_id}, {'$set': {CATEGORIES_NAME : []}})
        
#----------------------------------------------------------------------------------------------
    def get_aspect(self, _id):
        out = None
        data = self.cat.find_one({'_id':ObjectId(_id)})
        if data:
            category_root = self.get_root_category(ObjectId(_id))
            node_root = UserAspect.Node(category_root, None)
            
            hashmap = {}
            hashmap[str(category_root._id)] = node_root
            
            stack = []
            stack.append(node_root)
            
            while (len(stack) > 0):
                top = stack.pop(0)
                
                childs = self.get_childs(ObjectId(_id), top.category) # array of Category's

                for child in childs:
                    node = UserAspect.Node(child, top)
                    hashmap[str(child._id)] = node
                    top.childs.append(node)
                    stack.insert(0, node) 
            
            out = UserAspect({'_id':data['_id'], 'group_id':data['group_id'], 'node_root':node_root, 'hashmap':hashmap})
        return out
    
#----------------------------------------------------------------------------------------------        
    def add_aspect(self, aspect):
        self.cat.insert(aspect.get())

#----------------------------------------------------------------------------------------------
    def add_category(self, aspect_id, category):
        self.cat.update_one({'_id':aspect_id}, {'$push': {CATEGORIES_NAME : category.get()}})
        
#----------------------------------------------------------------------------------------------
    def remove_category(self, aspect_id, category_id):
        self.cat.update({'_id':aspect_id}, {'$pull': {CATEGORIES_NAME : {'_id':category_id}}})
        
#----------------------------------------------------------------------------------------------
    def get_root_category(self, _id):
        data = self.cat.find_one({'_id':_id}, { CATEGORIES_NAME: { '$elemMatch' :  {'name':'root'} } })
        
        if data and data.get('categories') and len(data[CATEGORIES_NAME]):
            return Category(data['categories'][0])
        return None
    
#----------------------------------------------------------------------------------------------
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
            
            for record in records:
                if record and record.get(CATEGORIES_NAME) and len(record[CATEGORIES_NAME]):
                   out.append(Category(record[CATEGORIES_NAME]))
                
        return out
    
#----------------------------------------------------------------------------------------------
    def drop(self):
        '''drop collection. rem in production'''
        self.cat.drop()
        
#----------------------------------------------------------------------------------------------
    def createUserAspect(self, group_id):
        '''creates default user aspect
            @param group_id - ObjectId type
            @return: userAspect object of UserAspect type
        '''
        DEFAULT_CATEGORY_NAME = 'All'
        root_category =  Category({'_id': ObjectId(), 'parent_id': None, 'name':'root'})
        all_category =  Category({'_id': ObjectId(), 'parent_id': root_category._id, 'name':DEFAULT_CATEGORY_NAME})
        
        root_node = UserAspect.Node(root_category, None)
        all_node = UserAspect.Node(all_category, root_node)

        root_node.childs.append(all_node)
        
        user_aspect = UserAspect({'_id':ObjectId(), 'group_id':group_id, 'node_root':root_node, 'hashmap':{}})

        self.add_aspect(user_aspect)
        
        return user_aspect

#----------------------------------------------------------------------------------------------
    def removeUserAspect(self, group):
        out = False
        if group:
            self.cat.remove({"group_id":group._id})
            out = True
        return out
    
    #----------------------------------------------------------------------------------------------
    def removeCategory(self, aspect_id, category):
        ''' removes category from db 
        @return: count of removed categories
        '''
        if category.name != 'root' and category.name != 'All':
            stack = []
            stack.append(category)
            
            count = 0
            while stack:
                new_stack = []
                for node in stack:
                    db_childs = self.get_childs(aspect_id, node)
                    for child in db_childs:
                        new_stack.append(child)
                    self.remove_category(aspect_id, node._id)
                    count += 1
                stack = new_stack
            return count
    
#----------------------------------------------------------------------------------------------
    def drop(self):
        '''drop collection. rem in production'''
        self.cat.drop()