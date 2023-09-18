<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Leaderboard</title>
</head>
<body class="mdc-typography" style="position:absolute; top: 50%;  left: 50%; transform: translate(-50%, -50%);">
<h1 style="text-align:center; margin: unset; float:left; font-size:40px; margin-bottom:10px;">Leaderboard</h1>
<img src="logo_resel.svg" style="width:100px; float:right; margin-bottom:10px;"/>
<br>
<head>
    <link rel="stylesheet" href="rss/style.css">
    <script type='text/javascript' src='rss/script.js'></script>
</head>

<div class="result" style="width:800px;"></div>

<script type="text/javascript" src="rss/jquery.js"></script>
<script>
    function refresh_div() {
        jQuery.ajax({
            url:'leaderboard.php',
            type:'POST',
            success:function(results) {
                jQuery(".result").html(results);
            }
        });
    }
    refresh_div();
    t = setInterval(refresh_div,10000);
</script>