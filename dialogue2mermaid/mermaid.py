HTML_1 = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <link rel="stylesheet" href="mermaid.min.css">
  </head>
  <body>

    <div class="mermaid">
"""

HTML_2 = """    </div>
    <script src="mermaid.min.js"></script>
    <script>mermaid.initialize({startOnLoad:true});</script>
  </body>
</html>
"""


def mermaid_to_html(mermaid: str) -> str:
    return HTML_1 + 'graph TB\n' + mermaid + '-1((END))\n' + HTML_2
