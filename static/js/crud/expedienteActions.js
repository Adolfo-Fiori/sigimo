// expedienteActions.js

document.getElementById('btn-encargar').addEventListener('click', function() {
    if(validarDatos()){
        enviarDatosBackend();
    } else {
        alert("Por favor, rellene todos los campos correctamente");
    }
});

document.getElementById('btnImprimirCertificado').addEventListener('click', function(){
    enviarDatosCert();
    imprimirCertificado();
    }
    );




function validarDatos() {
    var id = document.getElementById('pacienteId').value;
    var nombre = document.getElementById('nombre').value;
    var apellidoPaterno = document.getElementById('apellidoPaterno').value;
    var apellidoMaterno = document.getElementById('apellidoMaterno').value;
    var fechaNacimiento = document.getElementById('fechaNacimiento').value;
    var direccion = document.getElementById('direccion').value;
    var telefono = document.getElementById('telefono').value;
    var email = document.getElementById('email').value;
    var genero = document.getElementById('genero').value;
    var tipoAntecedente = document.getElementById('tipoAntecedente').value;
    var descripcion = document.getElementById('descripcionAntecedente').value;
    var sintomatologia = document.getElementById('sintomatologia').value;
    var tipoEstudio = document.getElementById('nombreEstudio').value;

    if (!id || !nombre || !apellidoPaterno || !apellidoMaterno || !fechaNacimiento || !direccion || !telefono || !email || !genero || !tipoAntecedente || !descripcion || !sintomatologia || !tipoEstudio) {
        alert('Todos los campos son obligatorios.');
        return false;
    }

    if (!/^\d+$/.test(telefono)) {
        alert('El teléfono solo debe contener números.');
        return false;
    }

    var emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    if (!emailRegex.test(email)) {
        alert('Ingresa un correo electrónico válido.');
        return false;
    }

    return true;
}


function enviarDatosBackend() {
    let data = {
        paciente: {
            pacienteId: document.getElementById('pacienteId').value,
            nombre: document.getElementById('nombre').value,
            apellidoPaterno: document.getElementById('apellidoPaterno').value,
            apellidoMaterno: document.getElementById('apellidoMaterno').value,
            fechaNacimiento: document.getElementById('fechaNacimiento').value,
            direccion: document.getElementById('direccion').value,
            telefono: document.getElementById('telefono').value,
            email: document.getElementById('email').value,
            genero: document.getElementById('genero').value
        },
        antecedente: {
            tipoAntecedente: document.getElementById('tipoAntecedente').value,
            descripcion: document.getElementById('descripcionAntecedente').value
        },
        diagnostico: {
            sintomatologia: document.getElementById('sintomatologia').value
        },
        estudio: {
            nombreEstudio: document.getElementById('nombreEstudio').value
        }
    };

    fetch('/api/insertExp', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json())
    .then(data => {
        alert(data.message); // Se mostrará el alerta independientemente del resultado
        if (data.message === 'Datos insertados exitosamente') {
            const btnImprimirCertificado = document.getElementById('btnImprimirCertificado');
            btnImprimirCertificado.disabled = false;
        } else {
            alert(data.message); // Aquí se muestra el alerta si algo salió mal
        }
    })
    .catch(error => console.error('Error:', error));
}

function enviarDatosCert() {
    let dataCert = {
        certificado: {
            pacienteId: document.getElementById('pacienteId').value,
            fechaEmision: new Date().toISOString().split('T')[0],  // Tomamos la fecha actual
            motivo: document.getElementById('sintomatologia').value
        }
    };

    fetch('/api/insertCert', {
        method: 'POST',
        body: JSON.stringify(dataCert),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json())
    .then(data => {
        alert(data.message); 
    })
    .catch(error => console.error('Error:', error));
}

function imprimirCertificado() {
    // Primero, crea un documento PDF con jsPDF
    let doc = new jsPDF.jsPDF();
    
    // Agrega contenido al PDF. Esto es un ejemplo básico, pero puedes personalizarlo según lo que necesites.
    let pacienteId = document.getElementById('pacienteId').value;
    let sintomatologia = document.getElementById('sintomatologia').value;
    let fecha = new Date().toISOString().split('T')[0];

    doc.setFontSize(20);
    doc.text('Certificado Médico', 105, 20, null, null, 'center');
    doc.setFontSize(14);
    doc.text(`Paciente ID: ${pacienteId}`, 20, 40);
    doc.text(`Fecha de Emisión: ${fecha}`, 20, 60);
    doc.text('Sintomatología:', 20, 80);
    doc.text(sintomatologia, 20, 100);

    // Convertir el PDF creado a un blob para visualizarlo con PDF.js
    const pdfBlob = doc.output('blob');

    // Configurar PDF.js para visualizar el PDF
    const loadingTask = pdfjsLib.getDocument({data: pdfBlob});

    loadingTask.promise.then(function(pdf) {
        // Muestra la primera página
        pdf.getPage(1).then(function(page) {
            const scale = 1.5;
            const viewport = page.getViewport({scale: scale});

            // Preparar el lienzo donde PDF.js mostrará el PDF.
            let canvas = document.getElementById('pdfCanvas');
            if (!canvas) {
                canvas = document.createElement('canvas');
                document.body.appendChild(canvas);
                canvas.id = 'pdfCanvas';
            }
            const context = canvas.getContext('2d');
            canvas.height = viewport.height;
            canvas.width = viewport.width;

            // Renderiza la página
            const renderContext = {
                canvasContext: context,
                viewport: viewport
            };
            page.render(renderContext).promise.then(function() {
                // Una vez que el PDF es visible, permite la impresión
                window.print();
            });
        });
    });
}
