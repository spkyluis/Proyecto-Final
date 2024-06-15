// Seleccionamos los elementos necesarios
const btnModal = document.getElementById('btn-modal');
const modal = document.getElementById('modal');
const btnClose = document.getElementById('btn-close');

// Función para mostrar la ventana emergente
function showModal() {
    modal.style.display = 'block'; // Mostramos la ventana emergente
    document.body.style.overflow = 'hidden'; // Desactivamos el scroll en la página inicial
}

// Función para cerrar la ventana emergente
function closeModal() {
    modal.style.display = 'none'; // Ocultamos la ventana emergente
    document.body.style.overflow = 'auto'; // Reactivamos el scroll en la página inicial
}

// Eventos para mostrar y cerrar la ventana emergente
btnModal.addEventListener('click', showModal);
btnClose.addEventListener('click', closeModal);