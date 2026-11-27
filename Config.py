import os
GithubUsername = os.getenv ("GITHUB_ACTOR")
GithubToken = os.getenv ("GITHUB_TOKEN")

FramesDir = "Frames"
OutputApng = os.getenv("OUTPUT_FILE", "contribution_animation.png")
Cols = 54
Rows = 31  
Scale = 10

ColorWhite = (255, 255, 255, 255)  # No contribution
ColorBlack = (0, 0, 0, 255)        # No contribution
ColorDarkGreen = (14, 68, 41, 255) # Did contribute 
ColorLightGreen = (57, 211, 83, 255) # Did contribute
