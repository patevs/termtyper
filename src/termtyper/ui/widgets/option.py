from textual import events
from textual.widget import Widget
from rich.align import Align
from rich.text import Span, Text
from rich.panel import Panel

from ...utils import Parser


class Option(Widget):
    """
    A widget to show options in horizontal fashion
    with the selected option with a colored background
    """
    def __init__(self, name: str, options: list[str]):
        super().__init__()
        self.name = name
        self.options = [i.strip() for i in options]
        self.cursor = self.options.index(Parser().get_data(self.name))
        self._set_option_string()

    def _set_option_string(self):
        m = max(len(i) for i in self.options) + 4  # 4 for nice padding
        self.options_string = "|".join(i.center(m) for i in self.options)
        self.positions = [
            [i, i + m - 2] for i in range(1, len(self.options_string), m + 1)
        ]

    async def on_mouse_scroll_down(self, _: events.MouseScrollDown):
        self.cursor = (self.cursor + 1) % len(self.options)
        Parser().set_data(self.name, self.options[self.cursor])
        self.refresh()

    async def on_mouse_scroll_up(self, _: events.MouseScrollUp):
        self.cursor = (self.cursor - 1 + len(self.options)) % len(self.options)
        Parser().set_data(self.name, self.options[self.cursor])
        self.refresh()

    def render(self):
        return Panel(
            Align.center(
                Text(
                    self.options_string,
                    spans=[
                        Span(
                            self.positions[self.cursor][0],
                            self.positions[self.cursor][1],
                            "reverse green",
                        )
                    ],
                ),
                vertical="middle",
            )
        )


if __name__ == "__main__":
    from textual.app import App

    class MyApp(App):
        async def on_mount(self):
            await self.view.dock(
                Option("test", ["Linux", "MacPriceyOS", "YourPCRanIntoAnError"])
            )

    MyApp.run()