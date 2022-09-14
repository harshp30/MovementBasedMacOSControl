September 2022

# MovementBasedMacOSControl

## Description

This is a python script that takes advantage of mediapipe. This uses computer vision to keep track of a body with certain nodes and landmarks. 

This is a diagram representation of the different nodes and landmarks mediapipe gives access to

![mediapipe diagram](https://github.com/harshp30/MovementBasedMacOSControl/blob/main/images/chart.png)

Using these points I created a script to look out for certain body movements. Then using osascript I assigned certain body movements to certain functions on my MacBook. This is the list of movements and the corresponding function (I made the functions for the apple music app).

Left Arm Curl -> PLAY

Right Arm Curl -> PAUSE

Left Leg Curl -> VOLUME 100

Right Leg Curl -> VOLUME 0

Cross Arms (both left and irght arm curl) -> Open/Close Music App (alternating)

The body movements are tracked by creating angle points between the different nodes. As seen in the picture below I calculated the angle between these points and once they went below a certain value I know a "curl" had occurred. 

![angle diagram](https://github.com/harshp30/MovementBasedMacOSControl/blob/main/images/angles.png)

## Use Case

This can be a helpful application for those who are unable to use their keyboard (the movements would have to be toned down)

Another application of this project could be for long-range functionality, for example, if someone is working from various devices and is far from their laptop simple movements could say the user from making the walk over to the laptop repeatedly.

## Demonstration

Youtube Link: https://www.youtube.com/watch?v=NXm064K_FTc&ab_channel=HarshPatel

## Key Learnings

I learned a lot about body tracking through mediapipe in this project. It was very interesting to see just how well each node was tracked and how responsive the system was. Before this project, I had no idea you could control a MacBook through scripts. This was a discovery for me and I had a lot of fun exploring the different functions available through osascript

## Key Challenges

The biggest challenge I faced during this project was figuring out what movements and at which angles those movements would register with the computer consistently. Since for the demo I was quite a distance away from the computer I needed to think of very obvious and repeatable movements that the camera can register consistently. The angles I figure out through some basic math with a good mix of trial and error.

## Future Improvements and Expansion

For future implementations of this project (especially if it's being used for those who are unable to use certain features of a laptop), I would make sure to make an emphasis on "easier" movements which may require a mediapipe alternative. I would also be sure to focus my efforts on making useful functions, in this case, I used it for music control, but more important functions could be implemented.
