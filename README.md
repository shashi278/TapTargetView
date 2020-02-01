# TapTargetView
An attempt to mimic android's TapTargetView using Python and Kivy.

Inspired by [Android's TapTargetView](https://github.com/KeepSafe/TapTargetView)

## Current Demo
![TapTargetView demo](demo/ttv_demo_2.gif)

#### TODO:
* [x] Track clicks inside `outer_circle`
* [x] Track clicks inside `target_circle` and remove the requirement of binding on widget's events
* [x] Add property to allow cancelling if clicked outside the `outer_circle`
* [ ] Current implementation removes the elevation from the widget. Needs to be fixed.
* [ ] Add shadow property
* [ ] Better implementation of function to stop animation
* [ ] Improve ripple animation
