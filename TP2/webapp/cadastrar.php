<?php
require_once 'functions.php';

$error = $success = null;

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action']) && $_POST['action'] === 'register') {
    try {
        if (registerUser($_POST)) {
            $success = "Cadastro realizado com sucesso!";
        }
    } catch (Exception $e) {
        $error = $e->getMessage();
    }
}
?>

<!DOCTYPE html>
<html lang="pt-BR">

<head>
    <meta charset="UTF-8">
    <title>Cadastro</title>
    <script src="/js/script.js" defer></script><script src="/js/script.js" defer></script>
    <link rel="stylesheet" href="css/styles.css">
</head>

<body>
    <h2>Cadastro de Usuário</h2>

    <?php if ($error): ?>
        <div><?= htmlspecialchars($error) ?></div>
    <?php endif ?>

    <?php if ($success): ?>
        <div><?= htmlspecialchars($success) ?></div>
    <?php endif ?>

    <form method="POST">
        <input type="hidden" name="action" value="register">
        <div>
            <label>Username <input type="text" name="username" minlength="4" required></label>
        </div>
        <div>
            <label>Password <input type="password" name="password" minlength="8" required></label>
        </div>
        <button type="submit">Cadastrar</button>
    </form>

    <p><a href="index.php">Voltar para Login</a></p>
</body>

</html>
