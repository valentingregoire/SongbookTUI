from typing import Generator

from textual.containers import Horizontal
from textual.widget import Widget
from textual.widgets import Button

from tui.utils import cancel, ok
from tui.widgets.action_button import ActionButton
from tui.widgets.containers import ActionsBar


class WidgetFactory:
    @staticmethod
    def btn_cancel() -> ActionButton:
        return ActionButton(f"{cancel()}", action="pop_screen", classes="btn-link error")
    
    @staticmethod
    def btn_ok() -> ActionButton:
        return ActionButton(f"[b]{ok()}", action="screen.ok", classes="btn-link success")

    @staticmethod
    def actions_bar_ok_cancel(widgets: list[Widget] = []) -> ActionsBar:
        actions_bar = ActionsBar()
        for widget in widgets: 
            actions_bar.compose_add_child(widget)
        actions_bar.compose_add_child(
            WidgetFactory.btn_cancel()
        )
        actions_bar.compose_add_child(
            WidgetFactory.btn_ok()
        )
        return actions_bar
    