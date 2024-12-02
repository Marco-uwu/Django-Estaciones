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
	form.submit(); // Enviar el formulario si todo es válido
    }
}

function filtrarEstacion() {
    const estacionMedicion = document.getElementById('filtro-estacion').value;
    const url = new URL(window.location.href);
    url.searchParams.set('estacion_medicion', estacionMedicion);
    window.location.href = url.toString();
}

document.addEventListener("DOMContentLoaded", function () {
    // Selecciona todos los enlaces de navegación y las secciones
    const navLinks = document.querySelectorAll('[data-section]');
    const sections = document.querySelectorAll('section');

    // Función para ocultar todas las secciones
    const hideAllSections = () => {
        sections.forEach(section => {
            section.style.display = "none";
        });
    };

    // Función para mostrar una sección específica
    const showSection = (sectionId) => {
        const targetSection = document.getElementById(sectionId);
        if (targetSection) {
            hideAllSections();
            targetSection.style.display = "block";
        }
    };

    // Restaurar la última sección seleccionada desde localStorage
    const lastSection = localStorage.getItem('lastSelectedSection');
    if (lastSection) {
        showSection(lastSection);
    } else {
        // Si no hay una selección previa, mostrar la primera sección por defecto
        showSection('seccion_estado');
    }

    // Agregar evento de clic a cada enlace de navegación
    navLinks.forEach(link => {
        link.addEventListener('click', function (event) {
            event.preventDefault(); // Previene el comportamiento predeterminado del enlace

            // Obtener la sección asociada al enlace
            const targetSectionId = this.getAttribute('data-section');

            // Mostrar la sección seleccionada
            showSection(targetSectionId);

            // Guardar la sección seleccionada en localStorage
            localStorage.setItem('lastSelectedSection', targetSectionId);
        });
    });
});

function actualizarTabla() {
  const selectElement = document.getElementById('filtro-estacion');
  const valorSeleccionado = selectElement.value;

  const celdaResultado = document.getElementById('encabezado_mediciones');
  celdaResultado.textContent = valorSeleccionado;
}
