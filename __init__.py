import cudatext as cu
from .md_find_headers import gen_markdown_headers

#
# http://wiki.freepascal.org/CudaText_API#How_plugin_can_fill_Code_Tree.3F
#


class Command:

    def __init__(self):
        self.h_tree = cu.app_proc(cu.PROC_GET_CODETREE, '')

    def update_tree(self):
        cu.ed.set_prop(cu.PROP_CODETREE, False)
        cu.tree_proc(self.h_tree, cu.TREE_ITEM_DELETE, 0)
        lines = cu.ed.get_text_all().split("\n")
        last_levels = {0: 0}
        for line, line_number, level, header in gen_markdown_headers(lines):
            for i in range(1, level + 2):
                parent = last_levels.get(level - i)
                if parent is None:
                    continue
                identity = cu.tree_proc(self.h_tree, cu.TREE_ITEM_ADD, parent, index=-1, text=header)

                last_levels[level] = identity
                for j in range(level+1, 10):
                    if j in last_levels:
                        del last_levels[j]
                        
                box = (0, line_number, len(line), line_number)
                cu.tree_proc(self.h_tree, cu.TREE_ITEM_SET_RANGE, identity, index=-1, text=box)
                break

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
