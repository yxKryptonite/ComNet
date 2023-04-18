"""Welcome to Pynecone! This file outlines the steps to create a basic app."""
from pcconfig import config

import pynecone as pc

from .components import point

docs_url = "https://pynecone.io/docs/getting-started/introduction"
filename = f"{config.app_name}/{config.app_name}.py"


class State(pc.State):
    """The app state."""

    pass


def index() -> pc.Component:
    return pc.center(
        pc.vstack(
            pc.heading("Lab1: WiFi Localization", font_size="2em"),
            pc.box(
                bg="lightgrey",
                border_radius="15px",
                border_color="black",
                border_width="thick",
                width="100%",
                padding=5,
            ),
            point(0,0,0),
            spacing="1.5em",
            font_size="2em",
        ),
        
        padding_top="10%",
    )


# Add state and page to the app.
app = pc.App(
    state=State,
    stylesheets=[
        "https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css",
    ],
)
app.add_page(index)
app.compile()
