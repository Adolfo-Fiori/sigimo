document.getElementById('create-account-form').addEventListener('submit', function(e){
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    fetch('http://localhost:5000/create-account', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, email, password })
    })
    .then(response => response.json())
    .then(data => {
        if(data.success){
            var modal = document.getElementById("verificationModal");
            modal.style.display = "block";
        } else {
            alert('Error al crear cuenta: ' + data.message);
        }
    })
    .then(/*...*/)
    .catch(error => console.error('Error:', error));
});

// Función para cerrar el modal
document.querySelector(".close-button").addEventListener("click", function() {
    var modal = document.getElementById("verificationModal");
    modal.style.display = "none";
});
// Función para enviar la verificación
function verifyAccount() {
    const email = document.getElementById('email').value;
    const verificationCode = document.getElementById('verificationCode').value;
    // Resto de tu código para hacer fetch a '/verify-account'
    fetch('http://localhost:5000/verify-account', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, verificationCode })
    })
    .then(response => response.json())
    .then(data => {
        if(data.success){
            // Si la verificación es exitosa
            var modal = document.getElementById("verificationModal");
            modal.style.display = "none";
            alert('¡Cuenta verificada con éxito!');
        } else {
            // Si hay un error en la verificación
            alert('Error al verificar la cuenta: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Hubo un error al verificar la cuenta.');
    });
}
