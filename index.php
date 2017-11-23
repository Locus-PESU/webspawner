<?php

        require __DIR__.'/vendor/autoload.php';
        $loader = new Twig_Loader_Filesystem(__DIR__.'/');
        $twig = new Twig_Environment($loader, array());

        $servername = "localhost";
        $username = "root";
        $password = "mayank@sql";
        $dbname = "blog";

        $conn = mysqli_connect($servername,$username,$password,$dbname);

        $query = "SELECT * FROM blogs ORDER BY create_on DESC;";
        $res = mysqli_query($conn, $query);
        $rows = mysqli_fetch_all($res);
        $ten = [];
        $i = 0;
        while ($i<10)
        {
               $ten[$i] = $rows[$i];
               $i++;
        }
        echo $twig->render('home.html', array(
                'blogs' => $ten
             ));

?>