<?php
    $file_name = "temp.txt";
    $data = file( $file_name );
?>
<style>
   a:link {
    color: #0000d0; 
   }
   a:visited {
    color: #ffffff;
   }
</style>
<center>
<table border="1">
    <tr>
        <td><b>Condition</b></td>
        <td><b>Name</b></td>
		<td><b>Link</b></td>
    </tr>
<?php
$fp = fopen("temp.txt", 'w');
$xd=count($data);
for($i=0;$i<$xd-1;$i++)
	for($j=$i+1;$j<$xd;$j++)
	{
		if ($data[$i]==$data[$j])
		{
			$data[$j]='';
		}
	}
for($i=0;$i<$xd;$i++)
{
	fwrite($fp, $data[$i]);
}
    foreach( $data as $value ):
        $value = explode( "	", $value );
		if(!empty($value[0])&&!empty($value[1])&&!empty($value[2]))
		{
?>
    <tr>
        <td><?=$value[0]?></td>
        <td><?=$value[1]?></td>
		<td><?=$value[2]?></td>
    </tr>
<?php
		}
    endforeach;
?>
</table>
</center>