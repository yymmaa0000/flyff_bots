<br />
<p align="center">
  <h3 align="center">My Flyff Bots</h3>

  <p align="center">
	This is a project I built on top of the original forked FlyFF vision bot. I have made the bot compatible with Flyff Universe.
	Please get familiar with the original project first before reaading the rest.
	<br />
	:warning: Windows only :warning:
    <br />
	<br />
    <a href="https://github.com/xandao-dev/flyff-bots"><strong>Explore the original project»</strong></a>
    <br />
  </p>
</p>

## Improved Foreground Vision Bot

The vision bot now works with Flyff Universe. I have also improved the character patroling algorithm and added a heal bot that automatically heals the player when the HP drops below 60%.

No UI changes.

### Game Setup Requirement
Make the following keyboard setup:

1 = auto attack. You could also change the code to make it attack by pressing C to cast spells from action bar or other key slot

2 = pick up

3 = heal

c = buffs action bar

N = cancel target

Play the game in a 1920*1080 resolution screen. Press F11 to maximize your game.

Set your interface theme to Gold. Put your character health window to the top left corner of your game interface. Change the window size to the smallest and set the display to percentage.

<img src="foreground_vision_bot/docs/Health_Window_Example.png" alt="Flyff bot">

The reason for such setup is that the bot will determine the player's health by taking a screen shot of your health window and parse its health percentage values.

<img src="foreground_vision_bot/docs/HealthBar_original.png" alt="Flyff bot">   Parsed into        <img src="foreground_vision_bot/docs/HealthBar_processed.png" alt="Flyff bot">

### Installation

To make the text recognition work, you need to install pytesseract. You can search google how to install that

Install tesseract for windows. You need to visit the Windows section of this link:
https://tesseract-ocr.github.io/tessdoc/Installation.html

To access tesseract-OCR from any location, you may have to add the directory where the tesseract-OCR binaries are located to the Path variables, maybe something like C:\Program Files\Tesseract-OCR.

To do that, refer to here: https://www.geeksforgeeks.org/how-to-set-up-command-prompt-for-python-in-windows10/
