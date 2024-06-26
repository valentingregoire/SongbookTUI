from textual.widget import Widget

from tui import utils
from tui.utils import cancel, ok, FLOPPY
from tui.widgets.action_button import ActionButton
from tui.widgets.containers import ActionsBar
from tui.widgets.form import Form


class WidgetFactory:
    @staticmethod
    def btn_cancel() -> ActionButton:
        return ActionButton(
            f"{cancel()}", action="screen.cancel", classes="btn-link error"
        )

    @staticmethod
    def btn_ok() -> ActionButton:
        return ActionButton(
            f"[b]{ok()}", action="screen.ok", classes="btn-link success"
        )

    @staticmethod
    def btn_save() -> ActionButton:
        return ActionButton(
            f"[b]{FLOPPY} Save", action="screen.save", classes="btn-link primary"
        )

    @staticmethod
    def btn_submit() -> ActionButton:
        return ActionButton(
            f"[b]{ok('Submit')}",
            action="screen.submit",
            event=Form.PreSubmit(),
            classes="btn-link primary",
        )

    @staticmethod
    def btn_edit() -> ActionButton:
        return ActionButton(
            f"[b]{utils.PENSIL} Edit",
            action="screen.edit",
            classes="btn-link primary",
        )

    @staticmethod
    def actions_bar_ok_cancel(widgets: list[Widget] = []) -> ActionsBar:
        actions_bar = WidgetFactory.actions_bar(widgets)
        actions_bar.compose_add_child(WidgetFactory.btn_cancel())
        actions_bar.compose_add_child(WidgetFactory.btn_ok())
        return actions_bar

    @staticmethod
    def actions_bar_form(widgets: list[Widget] = []) -> ActionsBar:
        actions_bar = WidgetFactory.actions_bar(widgets)
        actions_bar.compose_add_child(WidgetFactory.btn_cancel())
        actions_bar.compose_add_child(WidgetFactory.btn_submit())
        return actions_bar

    @staticmethod
    def actions_bar(widgets: list[Widget] = []) -> ActionsBar:
        actions_bar = ActionsBar()
        for widget in widgets:
            actions_bar.compose_add_child(widget)
        return actions_bar
