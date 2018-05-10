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
        heads = gen_markdown_headers(lines)
        for index, (line_number, level, header) in enumerate(heads):
            for test_level in range(level-1, -1, -1):
                parent = last_levels.get(test_level)
                if parent is None:
                    continue
                identity = cu.tree_proc(self.h_tree, cu.TREE_ITEM_ADD, parent, index=-1, text=header)

                last_levels[level] = identity
                # when adding level K, forget all levels >K
                for j in range(level+1, 10):
                    if j in last_levels:
                        del last_levels[j]
                        
                if index == len(heads)-1:
                    end_y = len(lines)-1
                    end_x = len(cu.ed.get_text_line(end_y))
                else:
                    end_y = heads[index+1][0] # line_index of next header
                    end_x = 0
                    
                rng = (0, line_number, end_x, end_y)
                cu.tree_proc(self.h_tree, cu.TREE_ITEM_SET_RANGE, identity, index=-1, text=rng)
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
