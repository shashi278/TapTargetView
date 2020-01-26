
"""
Attempt to mimic the working of Android's TapTargetView using Kivy in Python.
Here's android one: https://github.com/KeepSafe/TapTargetView

Author: Shashi Ranjan(https://github.com/shashi278)

"""

from kivy.animation import Animation
from kivy.metrics import dp,sp
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.core.text import Label as CoreLabel
from kivy.event import EventDispatcher

class TapTargetView(EventDispatcher):
    """
    Rough try to mimic the working of Android's TapTargetView

    """
    def __init__(
        self,
        widget,
        outer_radius=dp(400),
        outer_circle_color= [1,0,0],
        outer_circle_alpha=.96,
        target_radius=dp(70),
        target_circle_color=[1,1,1],
        title_text="",
        title_text_size= dp(25),
        title_text_color=[1,1,1,1],
        title_text_bold= True,
        description_text="",
        description_text_size=dp(20),
        description_text_color=[.9,.9,.9,1],
        description_text_bold= False,
        draw_shadow=False,
        cancelable=False,
        widget_position="left",
        title_position="auto",
        on_end= None,
        **kwargs
        ):
        """
        Attributes:
        ===========
        
        widget:             widget to add TapTargetView upon
        outer_radius:       (optional), Radius for outer circle, defaults to dp(400)
        outer_circle_color: (optional), Color for the outer circle, defaults to [1,0,0]
        outer_circle_alpha: (optional), Alpha value for outer circle, defaults to .96
        target_radius:      (optional), Radius for target circle, defaults to dp(80)
        target_circle_color:(optional), Color for target circle, defaults to [1,1,1]
        title_text:         (optional), Title to be shown on the view, defaults to ''
        title_text_size:    (optional), Text size for title, defaults to sp(30)
        title_text_color:   (optional), Text color for title, defaults to [1,1,1,1]
        title_text_bold:    (optional), Whether title should be bold. Defaults to `True`
        description_text:   (optional), Description to be shown below the title(Keep it short). Defaults to ''
        description_text_size:      (optional), Text size for description text, defaults to sp(10)
        description_text_color:     (optional), Text color for description text, defaults to [.8,.8,.8,1]
        description_text_bold:      (optional), Whether description should be bold. Defaults to False
        draw_shadow:        (optional), Whether to show shadow, defaults to False
        cancelable:         (optional), Whether clicking outside the outer circle dismisses the view, defaults to False
        widget_position:    (optional), Sets the position of the widget on the outer_circle.
                            Can be one of "left","right","top","bottom","left_top","right_top",
                            "left_bottom","right_bottom", and "center".
                            Defaults to "left"
        title_position:     (optional), Sets the position of `title_text` on the outer circle.
                            Only works if `widget_position` is set to "center". In all other cases,
                            it calculates the `title_position` itself.
                            Must be set to other than "auto" when `widget_position` is set to "center".
                            Can be one of "left","right","top","bottom","left_top","right_top",
                            "left_bottom", and "right_bottom".
                            Defaults to "auto"(since `widget_position` defaults to "left")
        on_end:             (optional), Function to be called when the animation ends by clicking the button.
                            Defaults to None
        """
        self.widget= widget
        self.outer_radius= outer_radius
        self.outer_circle_color= outer_circle_color
        self.outer_circle_alpha= outer_circle_alpha
        self.target_radius= target_radius
        self.target_circle_color= target_circle_color
        self.title_text_size= title_text_size
        self.title_text_color= title_text_color
        self.title_text_bold= title_text_bold
        self.description_text_size= description_text_size
        self.description_text_color= description_text_color
        self.description_text_bold= description_text_bold
        self.draw_shadow= draw_shadow
        self.cancelable= cancelable
        self.widget_position= widget_position
        self.title_position= title_position
        self.on_end= on_end

        self.ripple_max_dist=dp(70)

        #just to track if it's already been ended or not
        self._count=0

        self.title_text= CoreLabel(
            text=title_text,
            font_size=self.title_text_size,
            bold=self.title_text_bold,)
        self.title_text.refresh()
        self.title_text= self.title_text.texture

        self.description_text= CoreLabel(
            text=description_text,
            font_size=self.description_text_size,
            bold=self.description_text_bold)
        self.description_text.refresh()
        self.description_text= self.description_text.texture

        super(TapTargetView,self).__init__(**kwargs)
    
    def _initialize(self):
        setattr(self.widget, "outer_radius", 0)
        setattr(self.widget, "target_radius", 0)
        setattr(self.widget, "target_ripple_radius", 0)
        setattr(self.widget, "target_ripple_alpha",0)
    
    def draw_canvas(self):
        _pos= self.ttv_pos()

        self.widget.canvas.before.clear()
        with self.widget.canvas.before:
            #outer circle
            Color(*self.outer_circle_color, self.outer_circle_alpha)
            _rad1= self.widget.outer_radius
            Ellipse(
                size=(_rad1, _rad1),
                pos= _pos[0]
            )
            
            #Title text
            Color(*self.title_text_color)
            Rectangle(
                size= self.title_text.size,
                texture= self.title_text,
                pos= _pos[1]
            )
            
            #Description text
            Color(*self.description_text_color)
            Rectangle(
                size= self.description_text.size,
                texture= self.description_text,
                pos= (_pos[1][0], _pos[1][1]-self.description_text.size[1]-5)
            )
            
            #target circle
            Color(*self.target_circle_color)
            _rad2= self.widget.target_radius
            Ellipse(
                size=(_rad2, _rad2),
                pos=(
                    self.widget.x-(_rad2/2-self.widget.size[0]/2),
                    self.widget.y-(_rad2/2-self.widget.size[0]/2)
                )
            )

            #target ripple
            Color(*self.target_circle_color, self.widget.target_ripple_alpha)
            _rad3= self.widget.target_ripple_radius
            Ellipse(
                size=(_rad3, _rad3),
                pos=(
                    self.widget.x-(_rad3/2-self.widget.size[0]/2),
                    self.widget.y-(_rad3/2-self.widget.size[0]/2)
                )
            )
        
    def stop(self, *args):
        
        #it needs a better implementation
        self.anim_ripple.unbind(on_complete=self._repeat_ripple)
        self.description_text_color=[1,1,1,0]
        self.title_text_color=[1,1,1,0]
        anim= Animation(
            d=.15,
            t="in_cubic",
            **dict(zip(["outer_radius", "target_radius", "target_ripple_radius"],[0,0,0]))
        )
        anim.bind(on_complete= self._after_stop)
        anim.start(self.widget)
        self._count+=1
        
    def _after_stop(self, *args):
        self.widget.canvas.before.clear()
        args[0].stop_all(self.widget)
        if self._count==1 and self.on_end is not None:
            self.on_end()
    
    def start(self):
        self._initialize()
        self._animate_outer()
    
    def _animate_outer(self):
        anim= Animation(
            d=.3,
            t="out_cubic",
            **dict(zip(["outer_radius", "target_radius"],[self.outer_radius, self.target_radius]))
        )
        anim.cancel_all(self.widget)
        anim.bind(on_progress= lambda x,y,z: self.draw_canvas())
        anim.bind(on_complete=self._animate_ripple)
        anim.start(self.widget)
        setattr(self.widget, "target_ripple_radius", self.target_radius)
        setattr(self.widget, "target_ripple_alpha",1)
    
    def _animate_ripple(self, *args):
        self.anim_ripple= Animation(
            d=1,
            t="in_cubic",
            target_ripple_radius= self.target_radius+self.ripple_max_dist,
            target_ripple_alpha=0
        )
        self.anim_ripple.stop_all(self.widget)
        self.anim_ripple.bind(on_progress= lambda x,y,z: self.draw_canvas())
        self.anim_ripple.bind(on_complete=self._repeat_ripple)
        self.anim_ripple.start(self.widget)
    
    def _repeat_ripple(self, *args):
        setattr(self.widget, "target_ripple_radius", self.target_radius)
        setattr(self.widget, "target_ripple_alpha",1)
        self._animate_ripple()
    
    def on_target_click(self):
        pass
    
    def on_outer_click(self):
        pass

    def ttv_pos(self):
        """
        Calculates the `pos` value for outer circle and text
        based on the position provided

        param returns: A tupple containing pos for the circle and text

        """
        _rad1= self.widget.outer_radius
        _center_x= self.widget.x-(_rad1/2-self.widget.size[0]/2)
        _center_y= self.widget.y-(_rad1/2-self.widget.size[0]/2)

        if self.widget_position=="left":
            circ_pos=(_center_x+_rad1/3, _center_y)
            title_pos= (_center_x+_rad1/1.4, _center_y+_rad1/1.4)
        
        elif self.widget_position=="right":
            circ_pos= (_center_x-_rad1/3, _center_y)
            title_pos= (_center_x-_rad1/10, _center_y+_rad1/1.4)
        
        elif self.widget_position=="top":
            circ_pos= (_center_x, _center_y-_rad1/3)
            title_pos= (_center_x+_rad1/4, _center_y+_rad1/4)

        elif self.widget_position=="bottom":
            circ_pos= (_center_x, _center_y+_rad1/3)
            title_pos= (_center_x+_rad1/4, _center_y+_rad1/1.2)
        
        #corner ones need to be at a little smaller distance
        #than edge ones that's why _rad1/4
        elif self.widget_position=="left_top":
            circ_pos=(_center_x+_rad1/4, _center_y-_rad1/4)
            title_pos= (_center_x+_rad1/2, _center_y+_rad1/4)
        
        elif self.widget_position=="right_top":
            circ_pos=(_center_x-_rad1/4, _center_y-_rad1/4)
            title_pos= (_center_x-_rad1/10, _center_y+_rad1/4)
        
        elif self.widget_position=="left_bottom":
            circ_pos=(_center_x+_rad1/4, _center_y+_rad1/4)
            title_pos= (_center_x+_rad1/2, _center_y+_rad1/1.2)
        
        elif self.widget_position=="right_bottom":
            circ_pos=(_center_x-_rad1/4, _center_y+_rad1/4)
            title_pos= (_center_x, _center_y+_rad1/1.2)
        
        else:
            #center
            circ_pos=(_center_x, _center_y)

            if self.title_position=="auto":
                raise ValueError("widget_position='center' requires title_position to be set.")
            
            elif self.title_position=="left":
                title_pos= (_center_x+_rad1/10, _center_y+_rad1/2)
            
            elif self.title_position=="right":
                title_pos= (_center_x+_rad1/1.6, _center_y+_rad1/2)
            
            elif self.title_position=="top":
                title_pos= (_center_x+_rad1/2.5, _center_y+_rad1/1.3)
            
            elif self.title_position=="bottom":
                title_pos= (_center_x+_rad1/2.5, _center_y+_rad1/4)
            
            elif self.title_position=="left_top":
                title_pos= (_center_x+_rad1/8, _center_y+_rad1/1.4)
            
            elif self.title_position=="right_top":
                title_pos= (_center_x+_rad1/2, _center_y+_rad1/1.3)
            
            elif self.title_position=="left_bottom":
                title_pos= (_center_x+_rad1/8, _center_y+_rad1/4)
            
            elif self.title_position=="right_bottom":
                title_pos= (_center_x+_rad1/2, _center_y+_rad1/3.5)
            
            else:
                raise ValueError("'{}' is not a valid value for title_position".format(self.title_position))
            

        return circ_pos,title_pos



if __name__ == "__main__":
    from kivy.app import App
    from kivy.lang import Builder

    from kivymd.uix.button import MDIconButton
    from kivymd.theming import ThemeManager

    
    example_kv="""
BoxLayout:
    orientation:"vertical"

    BoxLayout:
        size_hint_y: None
        height: dp(60)
        canvas:
            Color:
                rgba: app.theme_cls.primary_color
            Rectangle:
                pos: self.pos
                size: self.size
        
        AnchorLayout:
            anchor_x:"left"
            MDIconButton:
                id: menu_btn
                md_bg_color: app.theme_cls.primary_color
                #theme_text_color:"Custom"
                #text_color:0,0,0,1
                icon: "menu"
                opposite_colors: True

        
        BoxLayout:
            AnchorLayout:
            BoxLayout:
                AnchorLayout:
                    MDIconButton:
                        id: search_btn
                        md_bg_color: 0,0,0,0
                        theme_text_color:"Custom"
                        text_color:1,1,1,1
                        icon: "magnify"
                        opposite_colors: True

                AnchorLayout:
                    MDIconButton:
                        id: info_btn
                        md_bg_color: 0,0,0,0
                        theme_text_color:"Custom"
                        text_color:1,1,1,1
                        icon: "information-outline"
                        opposite_colors: True

    
    BoxLayout:
        orientation:"vertical"
        Label:
            id: lbl
            text: ""
            color: .8,.8,.8,1
            font_size: sp(50)

        BoxLayout:
            AnchorLayout:
                size_hint_x:.3
                MDFloatingActionButton:
                    id: add_btn
                    icon: 'plus'
            AnchorLayout:


"""

    class TapTargetViewDemo(App):
        theme_cls= ThemeManager()

        def build(self):
            x= Builder.load_string(example_kv)
            menu_btn= x.ids.menu_btn
            search_btn= x.ids.search_btn
            info_btn= x.ids.info_btn
            add_btn= x.ids.add_btn

            self.lbl= x.ids.lbl
            self.final_text="Congrats! You're \n educated now!!"

            ttv4= TapTargetView(
                add_btn,
                outer_radius=dp(450),
                outer_circle_color= self.theme_cls.primary_color[:-1],
                outer_circle_alpha= .9,
                target_radius=dp(90),
                target_circle_color= [1,1,1],
                title_text= "This is an add button",
                description_text="Click here to add a new data",
                widget_position="left_bottom",

                on_end=self.set_text
            )

            ttv3= TapTargetView(
                info_btn,
                outer_radius=dp(650),
                outer_circle_color= self.theme_cls.primary_color[:-1],
                outer_circle_alpha= .8,
                target_radius=dp(90),
                target_circle_color=[255/255, 34/255, 212/255],
                title_text= "This is the info button",
                description_text="No information available yet!",
                widget_position="center",
                title_position="left_bottom",

                on_end=ttv4.start
            )

            ttv2= TapTargetView(
                search_btn,
                outer_radius=dp(600),
                outer_circle_color= [155/255, 89/255, 182/255],
                outer_circle_alpha= .95,
                target_radius=dp(90),
                target_circle_color=[.2,.2,.2],
                title_text= "This is the search button",
                description_text="It won't search anything for now.",
                widget_position="center",
                title_position="left_bottom",

                on_end=ttv3.start
            )

            ttv1= TapTargetView(
                menu_btn,
                outer_radius=dp(600),
                outer_circle_color= self.theme_cls.primary_color[:-1],
                outer_circle_alpha= .85,
                target_radius=(100),
                title_text= "Menu Button",
                description_text="Opens up the drawer",
                widget_position="center",
                title_position="right_bottom",

                on_end= ttv2.start
            )

            ttv1.start()

            menu_btn.bind(on_release= ttv1.stop)
            search_btn.bind(on_release= ttv2.stop)
            info_btn.bind(on_release= ttv3.stop)
            add_btn.bind(on_release= ttv4.stop)

            return x
        
        def set_text(self):
            self.lbl.text= self.final_text
    
    TapTargetViewDemo().run()
