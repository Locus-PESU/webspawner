<?php

	require __DIR__.'/vendor/autoload.php';
        $loader = new Twig_Loader_Filesystem(__DIR__.'/');
        $twig = new Twig_Environment($loader, array());


	$servername = "localhost";
    $username = "root";
    $password = "mayank@sql";
    $dbname = "blog";

    $conn = mysqli_connect($servername,$username,$password,$dbname);

    $query = "SELECT * from blogs order by create_on desc";

    $ret = mysqli_query($conn, $query);
    $rows = mysqli_fetch_all($ret);

    echo $twig->render('archives.html', array(
                'blogs' => $rows
            ));

?>