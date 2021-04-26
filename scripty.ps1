[int]$name = Read-Host -Prompt 'Enter the numbers of UAV?'
$name+=1
$i=1;
Start-Process powershell "python hq.py hq $name"
while($i -lt $name){
    Start-Process powershell "python uav.py $i $name"
    $i += 1
 }
 Read-Host -Prompt "Press Enter to exit"