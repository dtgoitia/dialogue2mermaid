HTML_1 = """
<!doctype html>
<html lang="en">
  <head>
    <title>Node Flow</title>

    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <!-- Bootstrap CSS -->
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css" integrity="sha384-PsH8R72JQ3SOdhVi3uxftmaW6Vc51MKb0q5P2rRUpPvrszuE4W1povHYgTpBfshb" crossorigin="anonymous">
	<link rel="stylesheet" type="text/css" href="./css/style.css">
  </head>
  <body>
	<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
	  <a class="navbar-brand" href="#"><img src="./css/logo.png" width="80" height="40" class="d-inline-block align-top" alt="">Project - Node Flow</a>
	  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
	    <span class="navbar-toggler-icon"></span>
	  </button>

	  <div class="collapse navbar-collapse" id="navbarSupportedContent">
	    <ul class="navbar-nav mr-auto">
	      <!--<li class="nav-item active">
	        <a class="nav-link" href="#">Home <span class="sr-only">(current)</span></a>
	      </li> --!>
	    </ul>
	  </div>
	</nav>

  <main role="main" class="custom-container"><br />
	<div class="row">
    <div class="col-md-12">
      <div class="mermaid center-block">
"""

HTML_2 = """    
      </div> 
    </div>
  </div>
  </main>
  
	<footer class="text-muted">
      <div class="container">
      	<hr />
        <p>&copy; 2018 - <a href="#">Project - Node Flow</a></p>
      </div>
    </footer>

    <!-- Optional JavaScript -->
    <script type="text/javascript"></script>
    <script type="text/javascript" src="./js/engine.js"></script>
	<script type="text/javascript" src="./js/draw.js"></script>
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.3/umd/popper.min.js" integrity="sha384-vFJXuSJphROIrBnz7yo7oB41mKfc8JzQZiCq4NCceLEaO4IHwicKwpJf9c9IpFgh" crossorigin="anonymous"></script>
	  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/js/bootstrap.min.js" integrity="sha384-alpBpkh1PFOepccYVYDB4do5UnbKysX5WZXm3XxPqe5iKTfUKjNkCk9SaVuEZflJ" crossorigin="anonymous"></script>
    <script src="mermaid.min.js"></script>
    <script>mermaid.initialize({startOnLoad:true});</script>
  </body>
</html>
"""


def mermaid_to_html(mermaid: str) -> str:
    return f"{HTML_1}graph TB\n{mermaid}\n{HTML_2}"
