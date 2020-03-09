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
        source: "kivymd_logo.png"
 
    CustomToolbar:
        id: toolbar
        size_hint_y: None
        height: app.theme_cls.standard_increment
        md_bg_color: app.theme_cls.primary_color
        pos_hint: {"top": 1}
        elevation: 10
        spacing: "20dp"

        AnchorLayout:
            anchor_x: "left"
            MDIconButton:
                id: menu_btn
                md_bg_color: app.theme_cls.primary_color
                #theme_text_color: "Custom"
                #text_color: 0, 0, 0, 1
                icon: "menu"
                opposite_colors: True

        BoxLayout:
            AnchorLayout:
            BoxLayout:
                AnchorLayout:
                    MDIconButton:
                        id: search_btn
                        md_bg_color: 0, 0, 0, 0
                        theme_text_color:"Custom"
                        text_color: 1, 1, 1, 1
                        icon: "magnify"
                        opposite_colors: True
                AnchorLayout:
                    MDIconButton:
                        id: info_btn
                        md_bg_color: 0, 0, 0, 0
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1
                        icon: "information-outline"
                        opposite_colors: True

    BoxLayout:
        orientation:"vertical"
        Label:
            id: lbl
            text: ""
            color: .8, .8, .8, 1
            font_size: sp(50)
        BoxLayout:
            AnchorLayout:
                size_hint_x: .3
                MDFloatingActionButton:
                    id: add_btn
                    icon: 'plus'
            AnchorLayout:
"""


class CustomToolbar(
    RectangularElevationBehavior, SpecificBackgroundColorBehavior, BoxLayout
):
    pass


class TapTargetViewDemo(MDApp):
    def build(self):
        x = Builder.load_string(example_kv)
        self.lbl = x.ids.lbl
        self.final_text = "Congrats! You're \n educated now!!"

        ttv4 = TapTargetView(
            widget=x.ids.add_btn,
            outer_radius=dp(225),
            cancelable=True,
            outer_circle_color=self.theme_cls.primary_color[:-1],
            outer_circle_alpha=0.9,
            title_text="This is an add button",
            description_text="You can cancel it by clicking outside",
            widget_position="left_bottom",
            end=self.set_text,
        )

        ttv3 = TapTargetView(
            widget=x.ids.info_btn,
            outer_radius=dp(325),
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
            widget=x.ids.search_btn,
            outer_circle_color=[155 / 255, 89 / 255, 182 / 255],
            target_circle_color=[0.2, 0.2, 0.2],
            title_text="This is the search button",
            description_text="It won't search anything for now.",
            widget_position="center",
            title_position="left_bottom",
            end=ttv3.start,
        )

        ttv1 = TapTargetView(
            widget=x.ids.menu_btn,
            outer_circle_color=self.theme_cls.primary_color[:-1],
            outer_circle_alpha=0.85,
            title_text="Menu Button",
            description_text="Opens up the drawer",
            widget_position="center",
            title_position="right_bottom",
            end=ttv2.start,
        )
        ttv1.start()
        return x

    def set_text(self, *args):
        self.lbl.text = self.final_text


TapTargetViewDemo().run()