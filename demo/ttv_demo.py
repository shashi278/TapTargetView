from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout

from kivymd.uix.behaviors import (
    RectangularElevationBehavior,
    SpecificBackgroundColorBehavior,
)
from kivymd.app import MDApp

from taptargetview.taptargetview import TapTargetView

KV = """
Screen:

    Image:
        source: "data/logo/kivy-icon-512.png"

    CustomToolbar:
        id: toolbar
        size_hint_y: None
        height: app.theme_cls.standard_increment
        md_bg_color: app.theme_cls.primary_color
        pos_hint: {"top": 1}
        elevation: 10
        spacing: "20dp"
        
        MDIconButton:
            id: btn_left_top
            icon: "menu"
            pos_hint: {"center_y": .5}
            on_release: app.show_tap_target_view_top()
            text_color: toolbar.specific_text_color
            theme_text_color: "Custom"

        MDLabel:
            text: "TapTargetViewDemo"
            font_style: 'H6'
            theme_text_color: "Custom"
            text_color: toolbar.specific_text_color

        
    MDFloatingActionButton:
        id: btn_right_button
        icon: "plus"
        on_release: app.show_tap_target_view_bottom()
        pos: (root.width - (self.width) - dp(20), 10)
        md_bg_color: app.theme_cls.primary_color
"""


class CustomToolbar(
    RectangularElevationBehavior, SpecificBackgroundColorBehavior, BoxLayout
):
    pass


class TapTargetViewDemo(MDApp):
    screen = None
    tap_target_view_top = None
    tap_target_view_bottom = None

    def build(self):
        self.screen = Builder.load_string(KV)
        return self.screen

    def show_tap_target_view_bottom(self):
        if self.tap_target_view_bottom:
            self.tap_target_view_bottom.stop()
            self.tap_target_view_bottom = None
            return

        self.tap_target_view_bottom = self.get_tap_target_view(
            self.screen.ids.btn_right_button, "right_bottom"
        )
        self.tap_target_view_bottom.start()

    def show_tap_target_view_top(self):
        if self.tap_target_view_top:
            self.screen.ids.btn_left_top.text_color = (
                self.screen.ids.toolbar.specific_text_color
            )
            self.tap_target_view_top.stop()
            self.tap_target_view_top = None
            return

        self.tap_target_view_top = self.get_tap_target_view(
            self.screen.ids.btn_left_top, "left_top"
        )
        self.screen.ids.btn_left_top.text_color = self.theme_cls.opposite_bg_darkest
        self.tap_target_view_top.start()

    def get_tap_target_view(self, widget, widget_position):
        return TapTargetView(
            widget=widget,
            cancelable=True,
            outer_radius=dp(400),
            target_radius=dp(72),
            outer_circle_color=self.theme_cls.primary_color[:-1],
            outer_circle_alpha=0.9,
            title_text="This is an add button",
            title_text_size="24sp",
            description_text="You can cancel it by clicking outside",
            widget_position=widget_position,
        )


TapTargetViewDemo().run()
