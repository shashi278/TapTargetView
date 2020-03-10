![TapTargetView demo](demo/ttv_demo_2.gif)

# TapTargetView [![Build Status](https://travis-ci.org/shashi278/TapTargetView.svg?branch=master)](https://travis-ci.org/shashi278/TapTargetView)
###### <i>This is now being used in [KivyMD](https://github.com/HeaTTheatR/KivyMD)</i>

An attempt to mimic android's TapTargetView using Python and Kivy.

Inspired by [Android's TapTargetView](https://github.com/KeepSafe/TapTargetView)

## Installation
#### *Using Pip*
 * `pip install taptargetview`
  
#### *Manually*

 * `git clone https://github.com/shashi278/TapTargetView.git`
    
 * `cd TapTargetView`
    
 * `python setup.py install`

## Simple Usage
```python

TapTargetView(
        my_button,
        outer_circle_color= [0,1,1],
        outer_circle_alpha= .85,
        title_text= "My Button",
        description_text="It does something when pressed",
        widget_position="center",
        title_position="right_bottom",
        end= my_callback
).start()

```
Refer to [demo](demo/ttv_demo.py) for extensive usages.

### Sequencing
Sequencing is easier. Just bind `start` of one instance to the `on_end` of another instance.
```python

ttv2= TapTargetView(
        my_button2,
        outer_circle_color= [1,0,1],
        outer_circle_alpha= .05,
        title_text= "My Second Button",
        description_text="It too does something when pressed",
        widget_position="left",
        end= my_callback
      )
      
ttv1= TapTargetView(
        my_button1,
        outer_circle_color= [0,1,1],
        outer_circle_alpha= .85,
        title_text= "My First Button",
        description_text="It does something when pressed",
        widget_position="center",
        title_position="right_bottom",
        end= ttv2.start
        )

ttv1.start()

```

### Customizable attributes:
```python
"""
widget:                 widget to add TapTargetView upon
outer_radius:           (optional), Radius for outer circle, defaults to dp(300)
outer_circle_color:     (optional), Color for the outer circle, defaults to [1,0,0]
outer_circle_alpha:     (optional), Alpha value for outer circle, defaults to .96
target_radius:          (optional), Radius for target circle, defaults to dp(45)
target_circle_color:    (optional), Color for target circle, defaults to [1,1,1]
title_text:             (optional), Title to be shown on the view, defaults to ''
title_text_size:        (optional), Text size for title, defaults to dp(25)
title_text_color:       (optional), Text color for title, defaults to [1,1,1,1]
title_text_bold:        (optional), Whether title should be bold, defaults to `True`
description_text:       (optional), Description to be shown below the title(Keep it short),
                        defaults to ''
description_text_size:  (optional), Text size for description text, defaults to dp(20)
description_text_color: (optional), Text color for description text, defaults to [.9,.9,.9,1]
description_text_bold:  (optional), Whether description should be bold, defaults to False
draw_shadow:            (optional), Whether to show shadow, defaults to False
cancelable:             (optional), Whether clicking outside the outer circle dismisses the view,
                        defaults to False
widget_position:        (optional), Sets the position of the widget on the outer_circle.
                        Can be one of "left","right","top","bottom","left_top","right_top",
                        "left_bottom","right_bottom", and "center", defaults to "left"
title_position:         (optional), Sets the position of `title_text` on the outer circle.
                        Only works if `widget_position` is set to "center". In all other cases,
                        it calculates the `title_position` itself.
                        Must be set to other than "auto" when `widget_position` is set to "center".
                        Can be one of "left","right","top","bottom","left_top","right_top",
                        "left_bottom", and "right_bottom", defaults to "auto" (since `widget_position` is "left")
stop_on_outer_touch:    (optional), whether clicking on outer circle stops the animation,
                        defaults to False
stop_on_target_touch:   (optional), whether clicking on target circle should stop the animation,
                        defaults to True
end:                    (optional), Function to be called when the animation stops, defaults to None
"""
```
