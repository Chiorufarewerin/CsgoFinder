<?php
header( "refresh:1;url=index.php" );
set_time_limit(0);
$url='http://csgolounge.com/?p=';
$search='Condition: 99.9';
$search2='<a href="trade';
$zir='★';
for($xxx=0;$xxx<=5;$xxx++)
{
$fp = fopen("temp.txt", 'a');
for($y=1;$y<=5;$y++)
{
$url228="$url"."$y";
$file = file("$url228"); 
for($i=count($file);$i>0;$i--)
{
	if(preg_match("~$search~u",$file["$i"],$matches, PREG_OFFSET_CAPTURE) && !preg_match("~$zir~u",$file["$i"]))
	{
		$pos=strpos($file["$i"],'C');
		$pos2=strpos($file["$i"],'market/listings');
		$pos21=strpos(substr($file["$i"],$pos2+16),'/');
		$pos22=strpos(substr(substr($file["$i"],$pos2+16),$pos21+1),'"');
		fwrite($fp, substr($file["$i"],$pos,18)."\t".substr(substr($file["$i"],$pos2+16),$pos21+1,$pos22)."\t");
		for($n=$i;$n>0;$n--)
		{
			if(preg_match("~$search2~u",$file["$n"]))
			{
				$pos3=strpos($file["$n"],"$search2");
				fwrite($fp, '<a href="http://csgolounge.com/'.substr($file["$n"],$pos3+9,strlen(substr($file["$n"],$pos3+9))-3).' target="_blank">Trade link</a>'."\n");
				break;
			}
		}
	}
	echo "$matches[1]";
}
}
}
?>