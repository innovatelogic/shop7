
class UserSettings():
    def __init__(self, spec):
        self.active_base_aspect = spec['active_base_aspect']
        self.show_base_aspect_whole_tree = spec['show_base_aspect_whole_tree']
    
    def get(self):
        record = {
            'active_base_aspect':self.active_base_aspect,
            'show_base_aspect_whole_tree':self.show_base_aspect_whole_tree,
            }
        return record