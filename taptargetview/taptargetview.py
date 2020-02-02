
"""
Attempt to mimic the working of Android's TapTargetView using Kivy and Python.
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
        outer_radius=dp(300),
        outer_circle_color= [1,0,0],
        outer_circle_alpha=.96,
        target_radius=dp(45),
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
        stop_on_outer_touch=False,
        stop_on_target_touch=True,
        on_end= None,
        **kwargs
        ):
        """
        Attributes:
        ===========
        
        widget:                 widget to add TapTargetView upon
        outer_radius:           (optional), Radius for outer circle, defaults to dp(300)
        outer_circle_color:     (optional), Color for the outer circle, defaults to [1,0,0]
        outer_circle_alpha:     (optional), Alpha value for outer circle, defaults to .96
        target_radius:          (optional), Radius for target circle, defaults to dp(45)
        target_circle_color:    (optional), Color for target circle, defaults to [1,1,1]
        title_text:             (optional), Title to be shown on the view, defaults to ''
        title_text_size:        (optional), Text size for title, defaults to dp(25)
        title_text_color:       (optional), Text color for title, defaults to [1,1,1,1]
        title_text_bold:        (optional), Whether title should be bold. Defaults to `True`
        description_text:       (optional), Description to be shown below the title(Keep it short)
                                Defaults to ''
        description_text_size:  (optional), Text size for description text, defaults to dp(20)
        description_text_color: (optional), Text color for description text, defaults to [.9,.9,.9,1]
        description_text_bold:  (optional), Whether description should be bold. Defaults to False
        draw_shadow:            (optional), Whether to show shadow, defaults to False
        cancelable:             (optional), Whether clicking outside the outer circle dismisses the view
                                Defaults to False
        widget_position:        (optional), Sets the position of the widget on the outer_circle.
                                Can be one of "left","right","top","bottom","left_top","right_top",
                                "left_bottom","right_bottom", and "center".
                                Defaults to "left"
        title_position:         (optional), Sets the position of `title_text` on the outer circle.
                                Only works if `widget_position` is set to "center". In all other cases,
                                it calculates the `title_position` itself.
                                Must be set to other than "auto" when `widget_position` is set to "center".
                                Can be one of "left","right","top","bottom","left_top","right_top",
                                "left_bottom", and "right_bottom".
                                Defaults to "auto"(since `widget_position` defaults to "left")
        stop_on_outer_touch:    (optional), whether clicking on outer circle stops the animation
                                Defaults to False
        stop_on_target_touch:   (optional), whether clicking on target circle should stop the animation
                                Defaults to True
        on_end:                 (optional), Function to be called when the animation stops.
                                Defaults to None
        """
        self.widget= widget
        self.outer_radius= 2*outer_radius
        self.outer_circle_color= outer_circle_color
        self.outer_circle_alpha= outer_circle_alpha
        self.target_radius= 2*target_radius
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
        self.stop_on_outer_touch= stop_on_outer_touch
        self.stop_on_target_touch= stop_on_target_touch
        self.on_end= on_end

        self.ripple_max_dist=dp(70)

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
        self.register_event_type("on_outer_touch")
        self.register_event_type("on_target_touch")
        self.register_event_type("on_outside_click")

    def _initialize(self):
        setattr(self.widget, "outer_radius", 0)
        setattr(self.widget, "target_radius", 0)
        setattr(self.widget, "target_ripple_radius", 0)
        setattr(self.widget, "target_ripple_alpha",0)

        # Note:
        # bind some function on widget event when this function is called instead of
        # when the class itself is initialized to prevent all widgets of all instances
        # to get bind at once and start messing up
        self.widget.bind(on_touch_down=self._some_func)
    
    def _draw_canvas(self):
        _pos= self._ttv_pos()

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
        
    def _after_stop(self, *args):
        self.widget.canvas.before.clear()
        args[0].stop_all(self.widget)
        if self.on_end:
            self.on_end()

        # Note:
        # Don't forget to unbind the function or it'll mess
        # up with other next bindings
        self.widget.unbind(on_touch_down=self._some_func)
    
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
        anim.bind(on_progress= lambda x,y,z: self._draw_canvas())
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
        self.anim_ripple.bind(on_progress= lambda x,y,z: self._draw_canvas())
        self.anim_ripple.bind(on_complete=self._repeat_ripple)
        self.anim_ripple.start(self.widget)
    
    def _repeat_ripple(self, *args):
        setattr(self.widget, "target_ripple_radius", self.target_radius)
        setattr(self.widget, "target_ripple_alpha",1)
        self._animate_ripple()
    
    def on_target_touch(self):
        #print("Clicked on target circle")
        if self.stop_on_target_touch:
            self.stop()
    
    def on_outer_touch(self):
        #print("Clicked on outer circle")
        if self.stop_on_outer_touch:
            self.stop()
    
    def on_outside_click(self):
        if self.cancelable:
            self.stop()
    
    def _some_func(self, wid, touch):
        """
        This function decides which one to dispatch
        based on the touch position
        """
        if self._check_pos_target(touch.pos):
            self.dispatch("on_target_touch")

        elif self._check_pos_outer(touch.pos):
            self.dispatch("on_outer_touch")
        
        else:
            self.dispatch("on_outside_click")
    
    def _check_pos_outer(self, pos):
        """
        Checks if a given `pos` coordinate is within the
        `outer_radius`
        """
        cx= self.circ_pos[0]+self.outer_radius/2
        cy= self.circ_pos[1]+self.outer_radius/2
        r= self.outer_radius/2
        h,k= pos

        lhs= (cx-h)**2+(cy-k)**2
        rhs= r**2
        if lhs<=rhs:
            return True
        return False
            
    def _check_pos_target(self,pos):
        """
        Checks if a given `pos` coordinate is within the
        `target_radius`
        """
        cx= self.widget.pos[0]+self.widget.width/2
        cy= self.widget.pos[1]+self.widget.height/2
        r= self.target_radius/2
        h,k= pos

        lhs= (cx-h)**2+(cy-k)**2
        rhs= r**2
        if lhs<=rhs:
            return True
        return False

    def _ttv_pos(self):
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
            
        self.circ_pos= circ_pos
        return circ_pos,title_pos

if __name__=="__main__":
    pass