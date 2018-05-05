import os
from cudatext import *
from .md_find_headers import *

#
# http://wiki.freepascal.org/CudaText_API#How_plugin_can_fill_Code_Tree.3F
#

class Command:

    def __init__(self):

        self.h_tree = app_proc(PROC_GET_CODETREE, '')
        #self._test_md()

    def _test_md(self):
    
        fn = os.path.join(os.path.dirname(__file__), 'test.md')
        with open(fn) as f:
            lines = f.read().splitlines()
        print(markdown_find_headers(lines))
        

    def update_tree(self):

        ed.set_prop(PROP_CODETREE, False)

        n = ed.get_line_count()

        tree_proc(self.h_tree, TREE_ITEM_DELETE, 0)
        tree_proc(self.h_tree, TREE_ITEM_ADD, 0, index=-1, text='Test, lines: '+str(n))

    def on_change_slow(self, ed_self):

        # lexer name is checked via .inf
        self.update_tree()

    def check_and_update(self):

        if ed.get_prop(PROP_LEXER_FILE) == 'Markdown':
            self.update_tree()

    def on_open(self, ed_self):
    
        self.check_and_update()
        
    def on_tab_change(self, ed_self):

        self.check_and_update()
