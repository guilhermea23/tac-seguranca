// Máscaras para formulário
document.addEventListener("DOMContentLoaded", function () {
    // Validação de formulário
    const forms = document.querySelectorAll("form");
    forms.forEach((form) => {
        form.addEventListener("submit", function (e) {
            const password = form.querySelector('input[type="password"]');
            if (password && password.value.length < 8) {
                alert("A senha deve ter pelo menos 8 caracteres");
                e.preventDefault();
            }
        });
    });
});
