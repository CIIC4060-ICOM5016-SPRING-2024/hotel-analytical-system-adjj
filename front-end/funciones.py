class Functions:
    def __init__(self):
        pass

    def create_navBar(self):
        from IPython.display import display
        import ipywidgets as widgets

        # Definir el HTML y CSS para la barra de navegación
        navbar_html = """
        <style>
            #navbar {
              background-color: #FF5733; /* Color de fondo de la barra de navegación */
              color: white;
              display: flex;
              justify-content: space-between;
              align-items: center;
              padding: 10px;
            }
            #navbar .logo {
              font-weight: bold;
              font-size: 24px;
            }
            #navbar .menu {
              list-style-type: none;
              margin: 0;
              padding: 0;
            }

            #navbar .menu li {
              display: inline;
              margin-right: 20px;
              font-weight: bold;
              font-size: 18px;
            }

            #navbar .menu li a {
              color: white; /* Color del texto de los enlaces */
              text-decoration: none;
              padding: 8px 12px;
            }

            #navbar .menu li a:hover {
              background-color: #C7460E; /* Color de fondo de los enlaces al pasar el mouse */
              border-radius: 4px;
            }
        </style>

        <div id="navbar">
          <div class="logo">hotel-analytical-system</div>
          <ul class="menu">
            <li><a href="./login.ipynb">Login</a></li>
            <li><a href="./local_statistics.ipynb">Local Statistics</a></li>
            <li><a href="./global_statistics.ipynb">Global Statistics</a></li>
            <li><a href="./create_records.ipynb">Create Records</a></li>
            <li><a href="./update_delete_records.ipynb">Update/Delete Records</a></li>
          </ul>
        </div>
        """

        # Crear el widget HTML con el contenido definido
        navbar_widget = widgets.HTML(value=navbar_html)

        # Mostrar el widget HTML
        display(navbar_widget)