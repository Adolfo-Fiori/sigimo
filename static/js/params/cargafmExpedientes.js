// opciones.js
const opcionesAntecedentes = [
    "Alergias a medicamentos",
    "Embarazos",
    "Enfermedades autoinmune",
    // ... otras opciones ...
];

const opcionesEstudios = [
    "Ultrasonido",
    "Toma de orina",
    "Copro",
    // ... otras opciones ...
];

window.onload = function() {
    const btnImprimirCertificado = document.getElementById('btnImprimirCertificado');
    btnImprimirCertificado.disabled = true;
    const selectAntecedentes = document.getElementById('tipoAntecedente');
    opcionesAntecedentes.forEach(opcion => {
        const el = document.createElement('option');
        el.textContent = opcion;
        el.value = opcion;
        selectAntecedentes.appendChild(el);
    });

    const selectEstudios = document.getElementById('nombreEstudio');
    opcionesEstudios.forEach(opcion => {
        const el = document.createElement('option');
        el.textContent = opcion;
        el.value = opcion;
        selectEstudios.appendChild(el);
    });
};
