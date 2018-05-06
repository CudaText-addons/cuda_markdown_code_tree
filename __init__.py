import os
import cudatext as cu
from .md_find_headers import gen_markdown_headers

#
# http://wiki.freepascal.org/CudaText_API#How_plugin_can_fill_Code_Tree.3F
#


class Command:

    def __init__(self):
        self.h_tree = cu.app_proc(cu.PROC_GET_CODETREE, '')
        self._test_md()

    def _test_md(self):

        fn = os.path.join(os.path.dirname(__file__), 'test.md')
        with open(fn) as f:
            lines = f.read().splitlines()
        for info in gen_markdown_headers(lines):
            print(info)

    def update_tree(self):
        cu.ed.set_prop(cu.PROP_CODETREE, False)
        n = cu.ed.get_line_count()
        cu.tree_proc(self.h_tree, cu.TREE_ITEM_DELETE, 0)
        cu.tree_proc(self.h_tree, cu.TREE_ITEM_ADD, 0, index=-1, text='Test, lines: '+str(n))

    def on_change_slow(self, ed_self):
        # lexer name is checked via .inf
        self.update_tree()

    def check_and_update(self):
        if cu.ed.get_prop(cu.PROP_LEXER_FILE) == 'Markdown':
            self.update_tree()

    def on_open(self, ed_self):
        self.check_and_update()

    def on_tab_change(self, ed_self):
        self.check_and_update()
