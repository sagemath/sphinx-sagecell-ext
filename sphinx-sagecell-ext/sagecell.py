# -*- coding: utf-8 -*-

from docutils.nodes import Element, General
from docutils.parsers.rst import directives
from sphinx.util.compat import Directive

linked = True # The default value for 'Linked Cells' option

class sagecell(General, Element):
    pass

class SageCell(Directive):

    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = False
    option_spec = {
        "linked": directives.unchanged
    }

    def run(self):

        node = sagecell()
        node['content'] = "\n".join(self.content)
        node['linked'] = self.options.get("linked")
        return [node]

def visit_sagecell_node(self, node):

    global linked

    if node['linked'] == "true":
        self.body.append("<div class='sage_linked'>")
    elif node['linked'] == "false":
        self.body.append("<div class='sage_unlinked'>")
    elif linked == True:
        self.body.append("<div class='sage_linked'>")
    elif linked == False:
        self.body.append("<div class='sage_unlinked'>")
    else:
        self.body.append("<div class='sage_unlinked'>")
    self.body.append("<script type='text/x-sage'>")
    self.body.append(node['content'])
    self.body.append("</script>")
    self.body.append("</div>")

def depart_sagecell_node(self, node):
    pass


def latex_visit_sagecell_node(self, node):

    global linked

    self.body.append("\n\n")
    self.body.append("\\begin{verbatim}\n")
    self.body.append(node['content'])
    self.body.append("\n\end{verbatim}")
    self.body.append("\n\n")

def mint_latex_visit_sagecell_node(self, node):

    global linked

    self.body.append("\n\n")
    self.body.append("\\definecolor{bg}{rgb}{0.95,0.95,0.95}\n")
    self.body.append("\\begin{minted}[breaklines, frame=lines,linenos,bgcolor=bg]{py}\n")
    self.body.append(node['content'])
    self.body.append("\n\\end{minted}")
    self.body.append("\n\n")


    

def latex_depart_sagecell_node(self, node):
    pass


def setup(app):

    # Register a Docutils node class
    app.add_node(sagecell,
                 html=(visit_sagecell_node, depart_sagecell_node),
    latex=(mint_latex_visit_sagecell_node, latex_depart_sagecell_node))
    # Register a Docutils directive
    app.add_directive("sagecellserver", SageCell)
