<?php
    session_start();

    $_SESSION["user"] = $_POST["username"];
    $_SESSION["title"] = $_POST["title"];
    $_SESSION["tags"] = $_POST["tags"];

?>
<html>
  <head>
    <style>
        #sourceTA {
            display: block;
        }
        #targetDiv {
          border: 1px dashed #333333;
          width: 600px;
          height: 400px;
        }
        *
        {
            color: black ;
        }
        button, input
        {
            padding: 1%;
            color: black;
            border-radius: 8px;
        }
    </style>
  </head>
  <body style ="
                background-image: url('http://cdn.backgroundhost.com/backgrounds/subtlepatterns/retina_wood.png');
            ">
      <form action = "design.php" method="post">
    <textarea id="sourceTA" rows="20" cols="80" name = "blog" placeholder="Enter blog content !"></textarea>
        <hr/>
        <input type="submit" />
    </form>
    <button id="runBtn" onClick="run()">Preview</button>
        <div id="targetDiv"></div>

        <script src="https://cdn.rawgit.com/showdownjs/showdown/1.0.1/dist/showdown.min.js"></script>
        <script>
            function run() {
                var text = document.getElementById('sourceTA').value,
                    target = document.getElementById('targetDiv'),
                    converter = new showdown.Converter(),
                    html = converter.makeHtml(text);

                  target.innerHTML = html;
              }
        </script>

  </body>
</html>