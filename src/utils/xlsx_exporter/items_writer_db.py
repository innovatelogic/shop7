from common.connection_db import ConnectionDB, LayoutDB
from group_tree import find_node_by_id
from bson.objectid import ObjectId

class ItemsWriterDB:
    def __init__(self, items, groups_root, connection):
        self.items = items
        self.groups_root = groups_root
        self.connection = connection
               
    def write(self):
        print ('Start write items to database...')
        
        items_db = self.connection.getCollection(self.connection.db, LayoutDB.ITEMS_NAME)
        
        for item in self.items:
            record = {'name':item['Name']}
            
            if 'Keywords' in item:
                record['keywords'] = item['Keywords']
                
            if 'Desc' in item:
                record['desc'] = item['Desc']
            
            if 'Price' not in item:
                print('WARNING! item # %s have not price. Set \'0\'' % item['UniqID'])
                record['price'] = 0
            else:
                record['price'] = item['Price']
            
            if 'Currency' not in item:
                print('WARNING! item # %s have not currency. Set \'UAH\'' % item['UniqID'])
                record['Currency'] = 'UAH'
            else:
                record['currency'] = item['Currency']
                
            if 'Unit' in item:
                record['unit'] = item['Unit']
                
            if 'ImageRefs' in item:
                record['imageRefs'] = item['ImageRefs']
                
            if 'Availability' in item:
                record['availability'] = item['Availability']
            
            if 'Amount' in item:
                record['amount'] = item['Amount'] 
            
            if 'GroupID2' in item:
                group = find_node_by_id(item['GroupID2'], self.groups_root)
                if group:
                    record['group_id'] = group._id
                else:
                    print ('WARNING! Item\'s # %s group ID not found set Root' % item['UniqID'])
            else:
                print ('WARNING! Item\'s # %s group ID not found set Root' % item['UniqID'])
                record['group_id'] = self.groups_root._id
                
                #dict['GroupID'] = item['']        
                #dict['Prom_ua_subsection'] = item['']        
                #dict['UniqID'] = item['']            
                #dict['ProductID'] = item['']                            
                #dict['SubsectionID'] = item['']                    
                #dict['GroupID2'] = item['']   
            
            for idx in range(0, 10):
                name = 'characteristicName' + str(idx)
                val = str('characteristicName') + str(idx)
                
                if name in item:                 
                    record[name] = item[name]
                if val in item:                                      
                    record[val] = item[val]

            items_db.insert(record)
            
        print ('Write items OK')