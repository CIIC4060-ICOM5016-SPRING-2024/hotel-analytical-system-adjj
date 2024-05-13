from IPython.display import display
import ipywidgets as widgets

class HtmlCSS:
    def __init__(self):
        pass

    def create_navBar(self, tuple_list):
        # Construct the list items dynamically
        menu_items_html = "".join([f'<li><a href="#{item[0]}">{item[1]}</a></li>' for item in tuple_list])

        # Define the HTML and CSS for the navigation bar
        navbar_html = f"""
        <style>
            #navbar {{
                background-color: #34495E; /* Dark blue background */
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
                color: white; /* Text color for links */
                text-decoration: none;
                padding: 8px 12px;
            }}
            #navbar .menu li a:hover {{
                background-color: #1ABC9C; /* Turquoise background on hover */
                border-radius: 4px;
            }}
        </style>

        <div id="navbar">
            <div class="logo">Hotel Analytics Systems</div>
            <ul class="menu">
                {menu_items_html}
            </ul>
        </div>
        """

        # Create an HTML widget with the defined content and display it
        navbar_widget = widgets.HTML(value=navbar_html)
        display(navbar_widget)

    def create_styled_section(self, section_id, title, background_color="#34495E", text_color="white"):
        # Build specific CSS for this section
        section_style = f"""
        <style>
        #{section_id} {{
            color: {text_color};
            font-weight: bold;
        }}
        #{section_id} + h1 {{
            background-color: {background_color};
            color: {text_color};
            padding: 10px;
            border-radius: 5px;
            margin-top: 10px; /* Add spacing above the title */
        }}
        </style>
        """

        # Build the HTML for the section with the anchor and title
        section_html = f"""
        <div id="{section_id}">
            <a id="{section_id}"></a>
            <h1 style='background-color: {background_color}; color: {text_color}; padding: 10px; border-radius: 5px;'>{title}</h1>
        </div>
        """

        # Combine the style and HTML, and display it using an HTML widget
        full_html = section_style + section_html
        display(widgets.HTML(value=full_html))
