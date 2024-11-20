function validarFormulario(event) {
    event.preventDefault(); // Evita el envío del formulario

    const grupos = document.querySelectorAll('.nice-form-group');
    let valido = true;
    let errores = [];

    grupos.forEach(grupo => {
        const inputs = grupo.querySelectorAll('.input-parametro');
        const minimo = parseFloat(inputs[0].value);
        const optimo = parseFloat(inputs[1].value);
        const maximo = parseFloat(inputs[2].value);

        if (!(minimo < optimo && optimo < maximo)) {
            valido = false;
        }
    });

    if (!valido) {
        alert(`Error en los valores. El mínimo debe ser menor que el óptimo y el máximo.`);
    } else {
        alert('Formulario enviado correctamente.');
    }
}