<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Leaderboard</title>
</head>
<body class="mdc-typography" style="width:800px; position:absolute; top: 50%;  left: 50%; transform: translate(-50%, -50%);">
<br>
<head>
    <link rel="stylesheet" href="rss/style.css">
    <script type='text/javascript' src='rss/script.js'></script>
</head>
<?php

// Données de connexion à la base de données
$host = $_ENV['DB_HOST'];
$dbname = $_ENV[];
$username = $_ENV[];
$password = $_ENV[];

// Connexion à la base de données
try {
    $conn = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
} catch (PDOException $e) {
    echo "Erreur de connexion à la base de données : " . $e->getMessage();
    exit();
}

// Réquête SQL
$query = "SELECT * FROM Users ORDER BY score DESC LIMIT 10";

// Exécution de la requête
$result = $conn->query($query);

// Affichage des résultats dans un tableau de deux colonnes
echo '<div class="mdc-data-table" style="width:800px;">';
echo '<div class="mdc-data-table__table-container">';
echo '<table class="mdc-data-table__table">';
echo '<tr class="mdc-data-table__header-row"><th class="mdc-data-table__header-cell" role="columnheader"><b>Nom</b></th><th class="mdc-data-table__header-cell" role="columnheader"><b>Score</b></th></tr>';
$i = 0;
foreach ($result as $row) {
        $i++;
        $chaine = $row['email'];
        $split = explode("@", $chaine);
        $nom_complet = explode(".", $split[0]);
        $prenom = ucfirst($nom_complet[0]);
        $nom = strtoupper($nom_complet[1]);
        $score = $row['score'];
        if ($i == 1){
                echo "<tr class='mdc-data-table__header-row'><td class='mdc-data-table__cell'>{$prenom} {$nom} &#129351</td><td class='mdc-data-table__cell'>{$score}</td></tr>";
        }elseif($i == 2){
                echo "<tr class='mdc-data-table__header-row'><td class='mdc-data-table__cell'>{$prenom} {$nom} &#129352</td><td class='mdc-data-table__cell'>{$score}</td></tr>";
        }elseif($i == 3){
                echo "<tr class='mdc-data-table__header-row'><td class='mdc-data-table__cell'>{$prenom} {$nom} &#129353</td><td class='mdc-data-table__cell'>{$score}</td></tr>";
        }else{
                echo "<tr class='mdc-data-table__header-row'><td class='mdc-data-table__cell'>{$prenom} {$nom}</td><td class='mdc-data-table__cell'>{$score}</td></tr>";
        }
        }
echo "</table>";
echo '</div>';
echo '</div>';
// Fermeture de la connexion
$conn = null;

?>

</body>
</html>