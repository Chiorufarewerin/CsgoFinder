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
		echo '<br>'.$value[1]."\t".empty($value[1]);
		if(!empty($value[0])&&!empty($value[1])&&!empty($value[2]))
			echo "\tlol";
    endforeach;
?>
</table>
</center>