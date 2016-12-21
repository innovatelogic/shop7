import io
from xml.dom import minidom
from xml.dom.minidom import *
from bson.objectid import ObjectId
from common.db.types.types import Category
from pyexpat import ExpatError

#----------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------- 
class CategoryNode():
    def __init__(self, category, parent):
        self.category = category
        self.parent = parent
        self.childs = []
        
    def dump(self, f, deep):
        ''' debug serialize '''
        self.woffset(deep, f)
        f.write(unicode('{} {}'.format(str(self.category.name), self.category._id) + '\n', 'utf8'))
        
        if self.childs:
            for child in self.childs:
                child.dump(f, deep + 1)
            
    def woffset(self, deep, f):
        for x in range(0, deep):
            f.write(unicode('  '))
            
#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------   
class Aspect():
    def __init__(self, name, root):
        self.name = name
        self.root = root
        self.hashmap = {}
        if self.root:
            self.hashmap[str(self.root.category._id)] = self.root

#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------        
class BaseAspectsContainer():
    def __init__(self, db_inst):
        self.db_inst = db_inst
        self.aspects = {}
        pass

#----------------------------------------------------------------------------------------------
    def load(self, cache_ref):
        aspect = BaseAspectHelper.load_aspect("basic", self.db_inst, cache_ref)
        if aspect:
            self.aspects['basic'] = aspect
        
        aspect = BaseAspectHelper.load_aspect("prom_ua", self.db_inst, cache_ref)
        if aspect:
            self.aspects['prom_ua'] = aspect
            
        aspect = BaseAspectHelper.load_aspect("ebay", self.db_inst, cache_ref)
        if aspect:
            self.aspects['ebay'] = aspect

#----------------------------------------------------------------------------------------------
    def get_first_level_categories(self, aspect):
        ''' return categories by id. integer means how levels will return '''
        out = []
        if self.aspects.get(aspect):
            aspect = self.aspects[aspect]
            out.append({'_id':str(aspect.root.category._id), 
                        'parent_id': str(aspect.root.category.parent_id),
                        'name':aspect.root.category.name, 
                        'n_childs':str(len(aspect.root.childs))})
                
            for item in aspect.root.childs:
                out.append({'_id':str(item.category._id), 
                            'parent_id': str(item.category.parent_id),
                            'name':item.category.name, 
                            'n_childs':str(len(item.childs))})
                
        return out
    
#----------------------------------------------------------------------------------------------
    def get_child_categories(self, aspect, category_id):
        out = []
        if self.aspects.get(aspect):
            aspect = self.aspects[aspect]
            node = aspect.hashmap[category_id]
            for item in node.childs:
                out.append({'_id':str(item.category._id), 
                            'parent_id': str(item.category.parent_id),
                            'name':item.category.name, 
                            'n_childs':str(len(item.childs))})
        return out
    
#----------------------------------------------------------------------------------------------
    def get_aspects(self):
        ''' returns array of loaded aspects'''
        out = []
        for key in self.aspects:
            out.append(key)
        return out
    
#----------------------------------------------------------------------------------------------
    def get_aspect(self, id):
        out = None
        if id in self.aspects:
            out = self.aspects[id]
        return out
    
#----------------------------------------------------------------------------------------------
    def get_aspect_category(self, aspect, category_id):
        out = None
        if self.aspects.get(aspect):
            if category_id in self.aspects[aspect].hashmap:
                out = self.aspects[aspect].hashmap[category_id]
        return out
    
#----------------------------------------------------------------------------------------------
    def get_aspect_category_root(self, aspect):
        out = None
        if aspect in self.aspects:
            out = self.aspects[aspect].root
        return out

#----------------------------------------------------------------------------------------------
    def get_aspect_child_categories(self, aspect, parent_id):
        out = []
        if aspect in self.aspects:
            node = self.aspects[aspect].hashmap[str(parent_id)]
            for item in node.childs:
                out.append(item)
        return out
            
#----------------------------------------------------------------------------------------------
class BaseAspectHelper():
    @staticmethod
    def dump_category_tree(filename, root):
        print("opening damp groups file:" + filename)
        with io.open(filename + '.dump', 'w', encoding='utf8') as f:
            print("opening OK")
            f.write(unicode('{\n'))
            root.dump(f, 0)
            f.write(unicode('}\n'))
                
    #----------------------------------------------------------------------------------------------
    @staticmethod
    def treeMerge(source_root, dest_root):
        ''' merge two trees. assign diff from source to dest.
            modify dest tree.
            not consistent with cache. offline only
        '''
        print('[treeMerge]')
        stack_dest = []
        stack_src = []
        stack_prev_dest = []
        
        total_cat_added = 0
        total_cat_updated = 0
        total_cat_removed = 0
        
        stack_src.append(source_root)
        stack_dest.append(dest_root)
        
        while(stack_src or stack_dest):
            print('------')
            new_stack_src = []
            new_stack_dst = []
            new_prev_dst = []
            
            cat_added = 0
            cat_updated = 0
            cat_removed = 0
            
            '''find common nodes in both spaces'''
            common_ab = []
            for src_node in stack_src:
                for dst_node in stack_dest:
                    if BaseAspectHelper.GetCategoryFullName(src_node) == BaseAspectHelper.GetCategoryFullName(dst_node):
                        BaseAspectHelper.UpdateCategory(dst_node.category, src_node.category)
                        cat_updated += 1
                        
                        common_ab.append(dst_node)
                        new_prev_dst.append(dst_node)
                        
                        for child in dst_node.childs: # add dst children to next iteration
                            new_stack_dst.append(child)
                            #print('add new_stack_dst {}'.format(child.category.name))
                            
                ''' add source children to next iteration '''
                for child in src_node.childs:
                    new_stack_src.append(child)
                    
            #for a in common_ab:
            #    print a.category.name

            ''' add source's unique to destination space'''
            for src_node in stack_src:
                bAdd = False
                for comm in common_ab:
                    if BaseAspectHelper.GetCategoryFullName(comm) == BaseAspectHelper.GetCategoryFullName(src_node):
                        bAdd = True
                        break
                    
                if not bAdd:
                    for dst_prev in stack_prev_dest:
                        if BaseAspectHelper.GetCategoryFullName(src_node.parent) == BaseAspectHelper.GetCategoryFullName(dst_prev):

                            if src_node.category._id == -1: # check id's invalid assign new
                                src_node.category._id = ObjectId()
                            if src_node.category.parent_id == -1:
                                src_node.category.parent_id = dst_prev.category._id
                              
                            src_copy = CategoryNode(src_node.category, dst_prev)
                            dst_prev.childs.append(src_copy)
                            new_prev_dst.append(src_copy)
                            cat_added += 1
                            break
            
            '''remove disjoint nodes from dest's parent'''
            for dst in stack_dest:
                #print('to rem {}'.format(dst.category.name))
                bRem = True
                for comm in common_ab:
                    if BaseAspectHelper.GetCategoryFullName(comm) == BaseAspectHelper.GetCategoryFullName(dst):
                        bRem = False 
                        #print('{} common'.format(dst.category.name))
                if bRem:
                    dst.parent.childs.remove(dst)
                    cat_removed += BaseAspectHelper.countChild(dst.category)
            
            print ('updated:{}  removed:{}  added:{}'.format(cat_updated, cat_removed, cat_added))

            total_cat_added += cat_added
            total_cat_updated += cat_updated
            total_cat_removed += cat_removed
            
            stack_prev_dest = new_prev_dst
            stack_src = new_stack_src
            stack_dest = new_stack_dst
            
        print ('Total: updated:{}  removed:{}  added:{}'.format(total_cat_updated, total_cat_removed, total_cat_added))
            
    #----------------------------------------------------------------------------------------------
    @staticmethod
    def save_aspect(db, aspect, src_root):
        ''' assign src_root to db. remove difference from db tree.
            not consistent with cache. offline use only
         '''
        print('save_aspect')
        stack_db = []
        stack_src = []
        stack_prev_dest = []
        
        total_cat_added = 0
        total_cat_updated = 0
        total_cat_removed = 0
        
        db_root = db.base_aspects.get_root_category(aspect)
        
        if not db_root:
            print('{} root not exist. create new'.format(aspect))
            db_root = Category({'_id': ObjectId(), 'parent_id': None, 'name':'root'})
            db.base_aspects.cat.insert({'_id':aspect})
            db.base_aspects.add_category(aspect, db_root)
            
        stack_src.append(src_root)
        stack_db.append(db_root)
        
        while(stack_src or stack_db):
            print('-----')
            new_stack_src = []
            new_stack_dst = []
            new_prev_dst = []
            
            cat_added = 0
            cat_updated = 0
            cat_removed = 0
            
            common_ab = []
            for src_node in stack_src:
                for dst_node in stack_db:
                    if src_node.category._id == dst_node._id:
                        common_ab.append(dst_node)
                        new_prev_dst.append(src_node)
                        
                        db.base_aspects.updateCategory(aspect, dst_node)
                        cat_updated += 1
                        
                        db_childs = db.base_aspects.get_childs(aspect, dst_node) # add dst children to next iteration
                        for child in db_childs:
                            new_stack_dst.append(child)
                            
                ''' add source children to next iteration '''
                for child in src_node.childs:
                    new_stack_src.append(child)
                    #print ('src child add {}'.format(child.category.name))
                    
            #print('comm {}'.format(common_names))     
            
            ''' add source's unique to destination space'''
            for src_node in stack_src:
                bExist = False
                for cat in common_ab:
                    if cat._id == src_node.category._id:
                        bExist = True
                        
                if not bExist:
                    for dst_prev in stack_prev_dest:
                        if src_node.parent.category._id == dst_prev.category._id:
                            db.base_aspects.add_category(aspect, src_node.category) # add to db
                            new_prev_dst.append(src_node)
                            cat_added += 1
                            #print('add category {}'.format(src_node.category.name))
                            break
            
            '''remove disjoint nodes from dest's parent'''
            for dst in stack_db:
                bRem = True
                for cat in common_ab:
                    if cat._id == dst._id:
                        bRem = False 
                if bRem:
                    cat_removed += self.removeCategory(db, aspect, dst)
                    
            print ('updated:{}  removed:{}  added:{}'.format(cat_updated, cat_removed, cat_added))
            
            total_cat_added += cat_added
            total_cat_updated += cat_updated
            total_cat_removed += cat_removed
            
            stack_prev_dest = new_prev_dst
            stack_src = new_stack_src
            stack_db = new_stack_dst
        
        print ('Total: updated:{}  removed:{}  added:{}'.format(total_cat_updated, total_cat_removed, total_cat_added))
        
        pass
    
    #----------------------------------------------------------------------------------------------
    @staticmethod
    def removeCategory(db, aspect, category):
        ''' removes category from db '''
        stack = []
        stack.append(category)
        
        count = 0
        while stack:
            new_stack = []
            for node in stack:
                db_childs = db.base_aspects.get_childs(aspect, node)
                for child in db_childs:
                    new_stack.append(child)
                db.base_aspects.remove_category(aspect, node._id)
                count += 1
            stack = new_stack
        return count + 1
   
    #----------------------------------------------------------------------------------------------
    @staticmethod
    def countChild(db, aspect, category):
        ''' count's all child + 1 '''
        stack = []
        stack.append(category)
        
        count = 0
        while stack:
            top = stack.pop(0)
            count += 1
            for child in top.childs:
                stack.append(child)
        return count + 1
    
    #----------------------------------------------------------------------------------------------
    @staticmethod
    def load_aspect(aspect, db, cache_ref):
        ''' create category tree'''
        print('Load aspect {}'.format(aspect))
        
        aspect_out = None
        
        count = 0
        root_node = CategoryNode(db.base_aspects.get_root_category(aspect), None)

        if root_node.category:
            aspect_out = Aspect(aspect, root_node)
            
            if cache_ref:
                cache_ref.add_base_category(aspect, str(root_node.category._id)) #cache
            
            stack = []
            stack.append(root_node)
            
            print('start load')
            while len(stack):
                top = stack.pop(0)
                
                childs = db.base_aspects.get_childs(aspect, top.category)
                count += 1

                for child in childs:
                    child_node = CategoryNode(child, top)
                    aspect_out.hashmap[str(child_node.category._id)] = child_node
                    
                    if cache_ref:
                        cache_ref.add_base_category(aspect, str(child_node.category._id)) #cache
                    
                    top.childs.append(child_node)
                    stack.insert(0, child_node) 
            print('end load')
        if count == 0:
            print('aspect {} not loaded completely'.format(aspect))
        else:
            print('Load aspect model OK: {} loaded'.format(count))
            
        return aspect_out
    
    #----------------------------------------------------------------------------------------------
    @staticmethod
    def loadFromXML(filename):
        ''' load tree of categories from xml fixed format. return root node
            do not fill db related fields
        '''
        print('[loadFromXML] {}'.format(filename))
        
        INVALID_ID = -1
        root = []
        default_name = ''
        try:
            doc = minidom.parse(filename)
            root_node = doc.getElementsByTagName("node")[0]
        
            root = CategoryNode(Category({'_id':INVALID_ID, 'parent_id':None, 'name':'root', 'local':''}), None)
            
            stack = []
            stack.append((root_node, root))
            count = 1
            
            while(stack):
                new_stack = []
                for node in stack:
                    childs = node[0].childNodes
                    
                    for child in childs:
                        if child.nodeType == child.ELEMENT_NODE and child.localName == 'node':
                            name = child.getAttribute("name")
                            
                            local = ''
                            if child.hasAttribute('local'):
                                local = child.getAttribute("local")
                            
                            foreign_id = ''
                            if child.hasAttribute('foreign_id'):
                                foreign_id = child.getAttribute("foreign_id")
                                
                            if child.hasAttribute('default'):
                                default_name = name
                                
                            cat = CategoryNode(Category({'_id':INVALID_ID, 'parent_id':INVALID_ID, 'name':name, 'local':local, 'foreign_id':foreign_id}), node[1])
                            node[1].childs.append(cat)
                            
                            new_stack.append((child, cat))
                            count += 1
                stack = new_stack
                
            print('processed {} categories'.format(count))
        except ExpatError as e:
            print(str(e))
        
        #BaseAspectHelper.dump_category_tree(filename + '.tmp2', root)
        return [root, default_name]
    
    #----------------------------------------------------------------------------------------------
    @staticmethod
    def UpdateCategory(dst_cat, src_cat):
        dst_cat.local = src_cat.local
        dst_cat.foreign_id = src_cat.foreign_id
        
    #----------------------------------------------------------------------------------------------    
    @staticmethod    
    def GetCategoryFullName(category_node):
        full_name = category_node.category.name
        parent = category_node.parent
        while parent:
            full_name = parent.category.name + '/' + full_name
            parent = parent.parent
        return full_name