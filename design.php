<?php
    session_start();

    $servername = "localhost";
    $username = "root";
    $password = "mayank@sql";
    $dbname = "blog";

    $conn = mysqli_connect($servername,$username,$password,$dbname);

    $user = $_SESSION["user"];
    $title = $_SESSION["title"];
    $tags = $_SESSION["tags"];

    $blog = $_POST["blog"];

    $query = "INSERT INTO blogs (username, title, tags, blog) values ('$user','$title','$tags','$blog');";
    mysqli_query($conn, $query);
    header("Location: index.php");
    die();
?>
