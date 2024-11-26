function validarFormulario(event) {
    event.preventDefault(); // Evitar el envío del formulario hasta que se valide
    
    const form = document.getElementById('form-parametros');
    const inputs = form.querySelectorAll('.input-parametro');
    let isValid = true;
    
    // Recorrer los inputs en grupos de 3 (v_min, v_ide, v_max)
    for (let i = 0; i < inputs.length; i += 3) {
        const v_min = parseFloat(inputs[i].value);
        const v_ide = parseFloat(inputs[i + 1].value);
        const v_max = parseFloat(inputs[i + 2].value);

        if (!(v_min < v_ide && v_ide < v_max)) {
            isValid = false;
            alert(`Los valores en la fila ${Math.floor(i / 3) + 1} no cumplen las condiciones:
                Mínimo < Óptimo < Máximo`);
            break; // Salir del bucle si hay un error
        }
    }

    if (isValid) {
        alert('Formulario enviado correctamente!');
	form.submit(); // Enviar el formulario si todo es válido
    }
}

