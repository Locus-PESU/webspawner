<?php

    $servername = "localhost";
    $username = "root";
    $password = "mayank@sql";
    $dbname = "blog";

    $conn = mysqli_connect($servername,$username,$password,$dbname);

    $target_dir = "uploads/";
    $target_file = $target_dir . basename($_FILES["file"]["name"]);
    $uploadOk = 1;
    $imageFileType = pathinfo($target_file,PATHINFO_EXTENSION);

    if (move_uploaded_file($_FILES["file"]["tmp_name"], $target_file))
    {
        echo "The file ". basename( $_FILES["file"]["name"]). " has been uploaded.";
    } else
    {
        echo "Sorry, there was an error uploading your file.";
    }

    $mime = $_POST['mime'];
    $user = $_POST['username'];
    $filerealname = $_POST['name'];

    $filedisplayname = basename( $_FILES["file"]["name"]);

    echo "$filedisplayname";
    $query = "INSERT into host (mime, data,filename, username) values ('$mime','$filerealname','$filedisplayname','$user');";

    mysqli_query($conn, $query);

    header("Location: index.php");
    die();

?>
