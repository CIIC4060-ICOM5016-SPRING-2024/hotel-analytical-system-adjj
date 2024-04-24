from IPython.display import display
import ipywidgets as widgets

class HtmlCSS:
    def __init__(self):
        pass

    def create_navBar(self, tuple_list):


        # Construir los elementos <li> de la lista dinámicamente
        menu_items_html = "".join([f'<li><a href="#{item[0]}">{item[1]}</a></li>' for item in tuple_list])

        # Definir el HTML y CSS para la barra de navegación
        navbar_html = f"""
        <style>
            #navbar {{
              background-color: #FF5733; /* Color de fondo de la barra de navegación */
              color: white;
              display: flex;
              justify-content: space-between;
              align-items: center;
              padding: 10px;
            }}
            #navbar .logo {{
              font-weight: bold;
              font-size: 24px;
            }}
            #navbar .menu {{
              list-style-type: none;
              margin: 0;
              padding: 0;
            }}

            #navbar .menu li {{
              display: inline;
              margin-right: 20px;
              font-weight: bold;
              font-size: 18px;
            }}

            #navbar .menu li a {{
              color: white; /* Color del texto de los enlaces */
              text-decoration: none;
              padding: 8px 12px;
            }}

            #navbar .menu li a:hover {{
              background-color: #C7460E; /* Color de fondo de los enlaces al pasar el mouse */
              border-radius: 4px;
            }}
        </style>

        <div id="navbar">
          <div class="logo">hotel-analytical-system</div>
          <ul class="menu">
            {menu_items_html}
          </ul>
        </div>
        """

        # Crear el widget HTML con el contenido definido
        navbar_widget = widgets.HTML(value=navbar_html)

        # Mostrar el widget HTML
        display(navbar_widget)

    def create_styled_section(self, section_id, title, background_color="#FF5733", text_color="white"):
        # Construir el CSS específico para esta sección
        section_style = f"""
        <style>
        #{section_id} {{
          color: {text_color}; /* Cambia el color del texto */
          font-weight: bold; /* Hace el texto en negrita */
        }}

        /* Para dar estilo al título que viene después del ancla */
        #{section_id} + h1 {{
          background-color: {background_color}; /* Color de fondo */
          color: {text_color}; /* Color del texto */
          padding: 10px; /* Espaciado interno */
          border-radius: 5px; /* Bordes redondeados */
        }}
        </style>
        """

        # Construir el HTML de la sección con el ancla y el título
        section_html = f"""
        <div id="{section_id}">
            <a id="{section_id}"></a>
            <h1 style='background-color: {background_color}; color: {text_color}; padding: 10px; border-radius: 5px;'>{title}</h1>
        </div>
        """

        # Combinar el estilo y el HTML, y mostrarlo utilizando un widget HTML
        full_html = section_style + section_html
        display(widgets.HTML(value=full_html))

