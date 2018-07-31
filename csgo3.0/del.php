<?php
  if(!empty($_POST['paswd'])){
     $pass = "123qwe456";
    if($_POST['paswd']==$pass){
     fopen('temp.txt', 'w');
	 echo 'Deleted!';
    }
    else {
       echo 'Wrong password!';
    }
  }
  else
  {
    ?>
    <form method="POST">
      <input type="text" name="paswd">
      <input type="submit">
    </form>
    <?php
  }
?>