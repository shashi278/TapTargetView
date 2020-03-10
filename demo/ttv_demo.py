from kivy.animation import Animation
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout

from kivymd.app import MDApp
from kivymd.uix.behaviors import (
    RectangularElevationBehavior,
    SpecificBackgroundColorBehavior,
)
from taptargetview.taptargetview import TapTargetView

example_kv = """
Screen:

    Image:
        id: logo
        source: "kivymd_logo.png"

    CustomToolbar:
        id: toolbar
        size_hint_y: None
        height: app.theme_cls.standard_increment
        md_bg_color: app.theme_cls.primary_color
        elevation: 10
        padding: "8dp", 0, 0, 0
        pos_hint: {"top": 1}

        MDIconButton:
            id: menu_btn
            icon: "menu"
            theme_text_color: "Custom"
            text_color: toolbar.specific_text_color
            md_bg_color: app.theme_cls.primary_color
            pos_hint: {"center_y": .5}

        Widget:
            size_hint_x: None
            width: "25dp"

        MDLabel:
            text: "TapTargetView"
            shorten: True
            font_style: 'H6'
            theme_text_color: "Custom"
            text_color: toolbar.specific_text_color

        MDIconButton:
            id: search_btn
            icon: "magnify"
            md_bg_color: 0, 0, 0, 0
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            pos_hint: {"center_y": .5}

        MDIconButton:
            id: info_btn
            icon: "information-outline"
            md_bg_color: 0, 0, 0, 0
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            pos_hint: {"center_y": .5}

    MDLabel:
        id: lbl
        text: "Congrats! You're" + "\\n" +  "educated now!!"
        opacity: 0
        font_size: "24sp"
        halign: "center"

    MDFloatingActionButton:
        id: add_btn
        icon: "plus"
        pos: 10, 10
"""


class CustomToolbar(
    RectangularElevationBehavior, SpecificBackgroundColorBehavior, BoxLayout
):
    pass


class TapTargetViewDemo(MDApp):
    def build(self):
        self.screen = Builder.load_string(example_kv)

        ttv4 = TapTargetView(
            widget=self.screen.ids.add_btn,
            outer_radius=dp(320),
            cancelable=True,
            outer_circle_color=self.theme_cls.primary_color[:-1],
            outer_circle_alpha=0.9,
            title_text="This is an add button",
            description_text="You can cancel it by clicking outside",
            widget_position="left_bottom",
            end=self.complete,
        )

        ttv3 = TapTargetView(
            widget=self.screen.ids.info_btn,
            outer_radius=dp(440),
            outer_circle_color=self.theme_cls.primary_color[:-1],
            outer_circle_alpha=0.8,
            target_circle_color=[255 / 255, 34 / 255, 212 / 255],
            title_text="This is the info button",
            description_text="No information available yet!",
            widget_position="center",
            title_position="left_bottom",
            end=ttv4.start,
        )

        ttv2 = TapTargetView(
            widget=self.screen.ids.search_btn,
            outer_circle_color=[155 / 255, 89 / 255, 182 / 255],
            target_circle_color=[0.2, 0.2, 0.2],
            title_text="This is the search button",
            description_text="It won't search anything for now.",
            widget_position="center",
            title_position="left_bottom",
            end=ttv3.start,
        )

        ttv1 = TapTargetView(
            widget=self.screen.ids.menu_btn,
            outer_circle_color=self.theme_cls.primary_color[:-1],
            outer_circle_alpha=0.85,
            title_text="Menu Button",
            description_text="Opens up the drawer",
            widget_position="center",
            title_position="right_bottom",
            end=ttv2.start,
        )
        ttv1.start()

        return self.screen

    def complete(self, *args):
        Animation(opacity=0.3, d=0.2).start(self.screen.ids.logo)
        Animation(opacity=0.3, d=0.2).start(self.screen.ids.lbl)


TapTargetViewDemo().run()
