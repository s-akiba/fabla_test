<?php
    $count = 0;
    $strMsg   = '';

    $request = '';
    if (isset($_SERVER['HTTP_X_REQUESTED_WITH'])) {
        $request = strtolower($_SERVER['HTTP_X_REQUESTED_WITH']);
    }
    if ($request !== 'xmlhttprequest') {
        exit;
    }
 
    $message = '';
    if (isset($_POST['message']) && is_string($_POST['message'])) {
        $message = htmlspecialchars($_POST['message'], ENT_QUOTES);
    }
    if ($message == '') {
        exit;
    }


    $fp = fopen('./message.txt', 'r');
    if (flock($fp, LOCK_SH)) {
        while (!feof($fp)) {
            if ($count > 200) {
                break;
            }
            $strMsg = $strMsg . fgets($fp);
            $count = $count + 1;
        }
    }
    flock($fp, LOCK_UN);
    fclose($fp);

    $strMsg = date("Y-m-d H:i:s") . ' - ' . $message . "\n" . $strMsg;
    file_put_contents('./message.txt', $strMsg, LOCK_EX);
?>