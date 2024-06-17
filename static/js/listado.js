document.addEventListener('DOMContentLoaded', function () {

  function cargarListaCompleta(listaPalabras) {
    var lista = document.getElementById('lista-palabras');  //  Nos ubicamos en la lista de palabras
    lista.innerHTML = ''; // Limpiar la lista antes de cargar.

    listaPalabras.forEach(function (palabra) {  // Para cada palabra en la lista...
      var li = document.createElement('li');  // Crea un elemento de la lista
      li.textContent = palabra;  // Agrega la palabra al elemento
      lista.appendChild(li);  // Agrega el elemento a la lista
    });

  }

  cargarListaCompleta(listaPalabras);  // Se carga la lista completa al cargar la página por primera vez

});

const filtrar = () => {  // Filtrar la lista de palabras
  const campoBusqueda = document.getElementById("campo-busqueda");  // Obtener el valor del campo de búsqueda
  const valorBusqueda = campoBusqueda.value.trim().toUpperCase();  // Pasar el valor del campo de búsqueda a mayúsculas para coincidir con formato de la lista y quita posibles espacios 

  const listaPalabras = document.querySelectorAll("#lista-palabras li");  // Cargar todas las palabras en la lista

  listaPalabras.forEach((elemento) => {   // Para cada elemento de la lista de palabras...
    const palabra = elemento.textContent.toUpperCase();  // Guardar el contenido de la palabra
    elemento.style.display = palabra.includes(valorBusqueda) ? "" : "none";  // Si el contenido  de la palabra coincide con el valor de búsqueda, se muestra, de lo contrario se oculta

  });
}