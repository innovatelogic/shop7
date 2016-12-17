import io
from bson.objectid import ObjectId
from common.db.types.types import Category

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
        self.load_aspect("basic", cache_ref)
        self.load_aspect("prom_ua", cache_ref)
        #self.load_aspect("amazon")
        self.load_aspect("ebay", cache_ref)

#----------------------------------------------------------------------------------------------
    def load_aspect(self, aspect, cache_ref):
        ''' create category tree'''
        print('Load aspect {}'.format(aspect))
        
        bResult = False
        
        count = 0

        root_node = CategoryNode(self.db_inst.base_aspects.get_root_category(aspect), None)

        if root_node.category:
            self.aspects[aspect] = Aspect(aspect, root_node)
            
            if cache_ref:
                cache_ref.add_base_category(aspect, str(root_node.category._id)) #cache
            
            stack = []
            stack.append(root_node)
            
            while len(stack):
                top = stack.pop(0)
                
                childs = self.db_inst.base_aspects.get_childs(aspect, top.category)
                count += 1

                for child in childs:
                    child_node = CategoryNode(child, top)
                    self.aspects[aspect].hashmap[str(child_node.category._id)] = child_node
                    
                    if cache_ref:
                        cache_ref.add_base_category(aspect, str(child_node.category._id)) #cache
                    
                    top.childs.append(child_node)
                    stack.insert(0, child_node) 

        if count == 0:
            print('aspect {} not loaded completely'.format(aspect))
        else:
            print('Load aspect model OK: {} loaded'.format(count))
            bResult = True
        return bResult
        
#----------------------------------------------------------------------------------------------  
    def save_aspect(self, aspect, src_root):
        ''' assign src_root to db. remove difference from db tree.
            not consistent with cache. offline use only
         '''
        print('save_aspect')
        stack_db = []
        stack_src = []
        stack_prev_dest = []
        
        db_root = self.db_inst.base_aspects.get_root_category(aspect)
        
        if not db_root:
            print('{} root not exist. create new'.format(aspect))
            db_root = Category({'_id': ObjectId(), 'parent_id': None, 'name':'root'})
            self.db_inst.base_aspects.cat.insert({'_id':aspect})
            self.db_inst.base_aspects.add_category(aspect, db_root)
            
        stack_src.append(src_root)
        stack_db.append(db_root)
        
        while(stack_src or stack_db):
            print('-----')
            new_stack_src = []
            new_stack_dst = []
            
            common_names = []
            for src_node in stack_src:
                #print src_node.category.name
                for dst_node in stack_db:
                    #print ('dst_node {}'.format(dst_node.name))
                    if src_node.category.name == dst_node.name:
                        common_names.append(dst_node.name)
                        stack_prev_dest.append(src_node)
                        ''' add dst children to next iteration '''
                        db_childs = self.db_inst.base_aspects.get_childs(aspect, dst_node)
                        for child in db_childs:
                            print ('dst child add {}'.format(child.name))
                            new_stack_dst.append(child)
                            
                ''' add source children to next iteration '''
                for child in src_node.childs:
                    new_stack_src.append(child)
                    print ('src child add {}'.format(child.category.name))
                    
            print('comm {}'.format(common_names))     
            
            ''' add source's unique to destination space'''
            for src_node in stack_src:
                bExist = False
                for name in common_names:
                    if name == src_node.category.name:
                        bExist = True
                        
                if not bExist:
                    for dst_prev in stack_prev_dest:
                        print(src_node.parent)
                        #print('id: {} : {} parent_name {}'.format(src_node.parent.category._id, dst_prev.parent_id, dst_prev.name))
                        if src_node.parent.category._id == dst_prev.category._id:
                            ''' add to db'''
                            self.db_inst.base_aspects.add_category(aspect, src_node.category)
                            stack_prev_dest.append(src_node)
                            
                            #print('add category {}'.format(src_node.category.name))
                            break
            
            '''remove disjoint nodes from dest's parent'''
            for dst in stack_db:
                print('to rem category {}'.format(dst.name))
                bRem = True
                for comm in common_names:
                    if comm == dst.name:
                        bRem = False 
                if bRem:
                    self.db_inst.base_aspects.remove_category(aspect, dst._id)
                    print('rem category {}'.format(dst.name))

            stack_src = new_stack_src
            stack_db = new_stack_dst

        pass
    
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
    def dump_category_tree(self, filename, root):
        print("opening damp groups file:" + filename)
        with io.open(filename + '.dump', 'w', encoding='utf8') as f:
            print("opening OK")
            f.write(unicode('{\n'))
            root.dump(f, 0)
            f.write(unicode('}\n'))
            
    #----------------------------------------------------------------------------------------------
    def treeMerge(self, source_root, dest_root):
        ''' merge two trees. assign diff from source to dest.
            modify dest tree.
            not consistent with cache. offline only
        '''
        stack_dest = []
        stack_src = []
        stack_prev_dest = []
        
        stack_src.append(source_root)
        stack_dest.append(dest_root)
        
        while(stack_src or stack_dest):
            print('------')
            new_stack_src = []
            new_stack_dst = []
            
            '''find common nodes in both spaces'''
            common_ab = []
            for src_node in stack_src:
                for dst_node in stack_dest:
                    if src_node.category.name == dst_node.category.name:
                        common_ab.append(dst_node)
                        stack_prev_dest.append(dst_node)
                        ''' add dst children to next iteration '''
                        for child in dst_node.childs:
                            new_stack_dst.append(child)
                            print('add new_stack_dst {}'.format(child.category.name))
                            
                ''' add source children to next iteration '''
                for child in src_node.childs:
                    new_stack_src.append(child)
                    
            for a in common_ab:
                print a.category.name

            ''' add source's unique to destination space'''
            for src_node in stack_src:
                bAdd = False
                for comm in common_ab:
                    if comm.category.name == src_node.category.name:
                        bAdd = True
                if not bAdd:
                    #print('add {}'.format(src_node.category.name))
                    for dst_prev in stack_prev_dest:
                        #print('chk {}'.format(dst_prev.category.name))
                        if src_node.parent.category.name == dst_prev.category.name:
                            '''check id's invalid assign new '''
                            if src_node.category._id == -1:
                                src_node.category._id = ObjectId()
                            if src_node.category.parent_id == -1:
                                src_node.category.parent_id = dst_prev.category._id
                              
                            src_copy = CategoryNode(src_node.category, dst_prev)
                            dst_prev.childs.append(src_copy)
                            stack_prev_dest.append(src_copy)
                            break
            
            '''remove disjoint nodes from dest's parent'''
            for dst in stack_dest:
                print('to rem {}'.format(dst.category.name))
                bRem = True
                for comm in common_ab:
                    if comm.category.name == dst.category.name:
                        bRem = False 
                        print('{} common'.format(dst.category.name))
                if bRem:
                    
                    dst.parent.childs.remove(dst)
            
            stack_src = new_stack_src
            stack_dest = new_stack_dst
            