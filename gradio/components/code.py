"""gr.Code() component"""

from __future__ import annotations

from typing import Literal

from gradio_client.documentation import document, set_documentation_group
from gradio_client.serializing import StringSerializable

from gradio.blocks import Default, get, NoOverride
from gradio.components.base import IOComponent
from gradio.events import Changeable, Inputable

set_documentation_group("component")


@document("languages")
class Code(Changeable, Inputable, IOComponent, StringSerializable):
    """
    Creates a Code editor for entering, editing or viewing code.
    Preprocessing: passes a {str} of code into the function.
    Postprocessing: expects the function to return a {str} of code or a single-elment {tuple}: (string filepath,)
    """

    languages = [
        "python",
        "markdown",
        "json",
        "html",
        "css",
        "javascript",
        "typescript",
        "yaml",
        "dockerfile",
        "shell",
        "r",
        None,
    ]

    def __init__(
        self,
        value: str | tuple[str] | None | Default = Default(None),
        language: Literal[
            "python",
            "markdown",
            "json",
            "html",
            "css",
            "javascript",
            "typescript",
            "yaml",
            "dockerfile",
            "shell",
            "r",
        ]
        | None = None,
        *,
        lines: int | None | Default = Default(5),
        label: str | None | Default = Default(None),
        interactive: bool | None | Default = Default(None),
        show_label: bool | None | Default = Default(None),
        container: bool | None | Default = Default(True),
        scale: int | None | Default = Default(None),
        min_width: int | None | Default = Default(160),
        visible: bool | Default = Default(True),
        elem_id: str | None | Default = Default(None),
        elem_classes: list[str] | str | None | Default = Default(None),
        **kwargs,
    ):
        """
        Parameters:
            value: Default value to show in the code editor. If callable, the function will be called whenever the app loads to set the initial value of the component.
            language: The language to display the code as. Supported languages listed in `gr.Code.languages`.
            label: component name in interface.
            interactive: Whether user should be able to enter code or only view it.
            show_label: if True, will display label.
            container: If True, will place the component in a container - providing some extra padding around the border.
            scale: relative width compared to adjacent Components in a Row. For example, if Component A has scale=2, and Component B has scale=1, A will be twice as wide as B. Should be an integer.
            min_width: minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.
            visible: If False, component will be hidden.
            elem_id: An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.
            elem_classes: An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.
        """
        self.lines = get(lines)
        self.language = get(language)
        if self.language != NoOverride:
            assert self.language in Code.languages, f"Language {self.language} not supported."

        IOComponent.__init__(
            self,
            label=label,
            interactive=interactive,
            show_label=show_label,
            container=container,
            scale=scale,
            min_width=min_width,
            visible=visible,
            elem_id=elem_id,
            elem_classes=elem_classes,
            value=value,
            **kwargs,
        )

    def postprocess(self, y):
        if y is None:
            return None
        elif isinstance(y, tuple):
            with open(y[0]) as file_data:
                return file_data.read()
        else:
            return y.strip()
