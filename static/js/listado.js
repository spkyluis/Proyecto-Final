document.addEventListener('DOMContentLoaded', function () {  // En cuanto se carga la página, ejecuta esta función

  function cargarLista(listaPalabras, donde) {  //  Carga una lista de palabras en el id que le pasemos por parámetro
    var lista = document.getElementById(donde);  //  Nos ubicamos en la lista de palabras
    lista.innerHTML = ''; // Limpiar la lista antes de cargar.

    listaPalabras.forEach(function (palabra) {  // Para cada palabra en la lista...
      var li = document.createElement('li');  // Crea un elemento de la lista
      li.textContent = palabra;  // Agrega la palabra al elemento
      lista.appendChild(li);  // Agrega el elemento a la lista
    });

  }

  cargarLista(listaPalabras, 'lista-palabras')  // Se carga la lista completa al cargar la página por primera vez
  cargarLista(lista_para_mostrar_mas, 'lista-palabras-top10mas')  // Se carga la lista top 10 más populares al cargar la página por primera vez
  cargarLista(lista_para_mostrar_menos, 'lista-palabras-top10menos')  // Se carga la lista top 10 más populares al cargar la página por primera vez

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