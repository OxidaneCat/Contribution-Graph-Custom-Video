# Contribution-Graph-Custom-Video
Previous Name: Bad-Apple-Contribution-Graph
A Custom animation contribution graph playing Bad Apple on github Contribution Graph with 3289 frames.
I do want to play or customize other videos. However, it takes a lot of time to edit all the files, so I'm looking forward for contributors to improve this project.
<div align="center">
  <img src=".github/Readme/Images/contribution_animation.png" width="100%">
</div>


## Use This Repository
This will play the Bad Apple!! on the Contribution Graph like the one above.

1. Create a Github token in your [setting](https://github.com/settings/tokens) with read:user and public_repo
2. Put the Github token in your profile special repository secrets in `settings/secrets/actions `
3. Set up Github Action on your profile special repository by adding a .yml file under `.github/workflows`
4. Here is an example of the yml file for this repository
```yml
name: Profile
on:
  schedule: [{cron: "0 23 * * *"}]
  workflow_dispatch:
jobs:
  render:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
      - uses: OxidaneCat/Contribution-Graph-Custom-Video@main
        with:
          token: ${{ secrets.NAME OF THE SECRET }}
```
> [!NOTE]
> DO NOT PUT THE TOKEN IN THE YML FILE. MAKE SURE TO PUT IT IN SECRETS IN THE REPOSITORY SETTINGS


## Customization Options
 - clone the repository and change the Frames
 - [Fork](https://github.com/OxidaneCat/Contribution-Graph-Custom-Video/fork) the repository and become a contributor
</br>
Custom animation for the contribution graph:
You will need to extract many frames from a video to play the animation.

> [!CAUTION]
> **Third-party software is used at your own risk. </br>
> I am not affiliated with any third party software. </br>
> I will not take liability for security issues, data loss, downtime, compatibility problems, licensing or copyright violations, or any damages caused by third-party software

FFmpeg is a free open-source software that can extract frames as PNG images from a video by using the following command:
```terminal
ffmpeg -i MEDIA.mp4 frame_%04d.png
```
Make sure to change `MEDIA.mp4` to the name of the mp4 file

</br>
### Contributing
Contributions, bug reports, and feature ideas are welcome!
1. [Fork](https://github.com/OxidaneCat/Contribution-Graph-Custom-Video/fork) the repository.
2. Make the changes in the new branch
3. Create a pull request
</br>
By submitting a contribution to this repository, you agree that your contributions will be licensed under the same PolyForm Noncommercial License 1.0.0



### Third-Party Assets & Fan-Work Disclaimer
This project is an unofficial **Touhou Project** derivative work
The PolyForm license above applies only to the original source code written by me (OxidaneCat). All rights to the underlying *Bad Apple!!* music, characters, and shadow-art animation belong to their respective creators:
 - Original Composition and Touhou Project: ZUN (Touhou Gensokyo ~ Lotus Land Story)
 - Music Arrangement and Vocals: Alstroemeria Records (Masayoshi Minoshima, Haruka, nomico)
 - Shadow-Art Animation: Anira (あにら) & MMM (Storyboard)
[https://en.touhouwiki.net/wiki/Bad_Apple!!](https://en.touhouwiki.net/wiki/Bad_Apple!!)

