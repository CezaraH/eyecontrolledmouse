# eyecontrolledmouse
Mouse controlled by eye movements using Python 2.7 and opencv2 with built-in calibration bar.

Video of it in action: https://youtu.be/-a8ucjNlaJs

This was created for my Bacherlor's project "Eye Controlled Mouse for investigating Low-Cost Assistive Technologies" using python 2.7, opencv and several other libraries including numpy, PIL, win32api. If you want to run this app, you will need to have all of those modules installed. 

The app allows for camera input from two cameras, as users with laptops may find it easier to use the tracker with a webcam. When you first initialise the app you should click calibration settings to find a sensitivity that works for you. The default value is 20, but you may want to raise this is if your room is bright. Zoom your camera in so that your eye is the only thing in the camera feed and calibrate it until the app finds your pupil reliably.

There is no click input, so that will have to be done manually. However, I'm sure this could be implemented if anyone felt adventurous to work upon my script. In my initial vision, this application would be used together with a joycon as research suggests most users with motor impairments retain a level of dexterity in their extremities. They can use this app while using the joycon for click executions.

Many thanks to Sergio Canu's resources:
https://pysource.com/category/tutorials/

And Harrison Kinsley's videos:
https://hkinsley.com/
