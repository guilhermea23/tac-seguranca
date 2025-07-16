<?php
require_once 'functions.php';

$error = null;

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action']) && $_POST['action'] === 'login') {
    try {
        if (loginUser($_POST['username'], $_POST['password'])) {
            header("Location: /");
            exit;
        } else {
            throw new RuntimeException("Invalid credentials");
        }
    } catch (Exception $e) {
        $error = $e->getMessage();
    }
}

if (isset($_GET['logout'])) {
    session_destroy();
    header("Location: /");
    exit;
}
?>

<!DOCTYPE html>
<html lang="pt-BR">

<head>
    <meta charset="UTF-8">
    <title>Login</title>
    <script src="/js/script.js" defer></script>
    <link rel="stylesheet" href="css/styles.css">
</head>

<body>

    <?php if (isset($_SESSION['user'])): ?>
        <nav>
            <div>
                <a href="#">Admin System</a>
                <div>
                    <span>Hello, <?= htmlspecialchars($_SESSION['user']['username']) ?></span>
                    <a href="?logout=1">Logout</a>
                </div>
            </div>
        </nav>

        <main>
            <?php if (isAdmin()): ?>
                <h2>Registered Users</h2>
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Username</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach (getDBConnection()->query("SELECT id, username FROM users") as $user): ?>
                            <tr>
                                <td><?= htmlspecialchars($user['id']) ?></td>
                                <td><?= htmlspecialchars($user['username']) ?></td>
                                <td><a href="?view=<?= $user['id'] ?>">View</a></td>
                            </tr>
                        <?php endforeach ?>
                    </tbody>
                </table>
            <?php else: ?>
                <div>Access denied</div>
            <?php endif ?>
        </main>

    <?php else: ?>
        <h2>Login</h2>

        <?php if ($error): ?>
            <div><?= htmlspecialchars($error) ?></div>
        <?php endif ?>

        <form method="POST">
            <input type="hidden" name="action" value="login">
            <div>
                <label>Username <input type="text" name="username" required></label>
            </div>
            <div>
                <label>Password <input type="password" name="password" required></label>
            </div>
            <button type="submit">Login</button>
        </form>

        <p>Não tem uma conta? <a href="cadastrar.php">Cadastrar</a></p>
    <?php endif ?>

</body>

</html>
