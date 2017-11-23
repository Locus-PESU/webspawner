<?php

	$servername = "localhost";
    $username = "root";
    $password = "mayank@sql";
    $dbname = "blog";

    require __DIR__.'/vendor/autoload.php';
    $loader = new Twig_Loader_Filesystem(__DIR__.'/');
    $twig = new Twig_Environment($loader, array());

    $conn = mysqli_connect($servername,$username,$password,$dbname);
	$title =  $_GET['title'];
	$time =  $_GET['time'];

	$query = "SELECT * from blogs where title = '$title' and create_on = '$time';";
	$ret = mysqli_query($conn, $query);
	$blog = mysqli_fetch_assoc($ret);

	echo $twig->render('showblog.html', array('blog' => $blog));


?>
