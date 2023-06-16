# AIoT Smart Fridge System

## Introduction
Smart Fridge comes with food recognition, expiration alert, face detection, and a web UI to monitor fridge state, visualize items in fridge, and generate recipe with ChatGPT.
<div style="margin-top: 16px; margin-inline: auto; display: grid; grid-template-columns: repeat(2, 1fr); row-gap: 16px; max-width: 700px;">
  <div style="max-height: 700px">
    <div style="padding: 2px 5px; background: rgba(255,255,255,0.5); color: black; border-radius: 8px; width: fit-content;">Home page</div>
    <img src="./images/1-home.png" />
  </div>
  <div style="max-height: 700px">
    <div style="padding: 2px 5px; background: rgba(255,255,255,0.5); color: black; border-radius: 8px; width: fit-content;">Expiration date</div>
    <img src="./images/2-expiration-date.png" />
  </div>
  <div style="max-height: 700px">
    <div style="padding: 2px 5px; background: rgba(255,255,255,0.5); color: black; border-radius: 8px; width: fit-content;">Stolen items</div>
    <img src="./images/3-stolen.png" />
  </div>
  <div style="max-height: 700px">
    <div style="padding: 2px 5px; background: rgba(255,255,255,0.5); color: black; border-radius: 8px; width: fit-content;">ChatGPT recipe</div>
    <img src="./images/4-gpt-recipe.png" />
  </div>
</div>

## Hardware
- Raspberry Pi 4B x3
- Sensors
  - Temperature and Humidity Sensor
  - Camera Module (Webcam)

## Frontend Web UI
[SmartFridge](https://github.com/ANITA-0604/SmartFridge) is the frontend codebase developed using Next.js.

## Backend
Python Flask server that
- Provides API endpoints for frontend and other Raspberry Pi
- Uses Redis DB to store fridge state and items in fridge

## Object Detection
Raspberry Pi on-device detection using YOLO-v5
<div>
  <img style="border-radius: 8px; max-width: 500px" src="./images/object-detection.png" />
</div>

## Face Detection
