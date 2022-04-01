# Machine-Learning-Robot-Movement
This copies the 2D movements of a user after training on a users movement. Its intended use is for studying teleoperation and telepresence with signal loss when users are no longer available but want a robot to replicate their movement intermittantly.

## What the module does
- this module intends to Optimize tele-operation procedures using various computational algorithms.
- Allows user to "train on data" by creating .csv files containing data mimicking mouse cursor movement (left click to start recording, left click let up to stop and start new drawing) and json file
- Use mouse data text file to have robot mimick movements from user mouse data and run applications to execute the data
- Allow for configurable state declarations (radians or degree, bounded or unbounded (more than 365)), and what gets saved to .json to have easy IRL algo implemented

## How to run
- Everything can be run using the GUI.py script to bring up the custom GUI
- click the "train" button in the gui, name your directory in the terminal, then start drawing charecter in the left half of the GUI and following the instructions prompted but the GUI
- draw as many verions of the movement as desired to train on, the more there is the more robust the algorithm (preferably over 10 to reduce chances of error/unvisited states)
- when done exit out, go back to GUI and click and hit the r button to "Restart" and clear the environemt
- to add the policy you trained on see "Adding/Importing a trained a ML policy" below
- Once a policy is imported left click and start drawing in the left half in gui to start surgery 
- lift up left click to have robot mimick user movements and instantiate the ML policy defined from training 
- at any point right click to have the doctor stop drawing/doing surgery

Notes:
- pink indicates where cutout time occured and emphasizes the differncces between what the robot and user did whereas black indicates where they are in sync
- the outside border of the robot environment will also change as there is instantiated cutout

## Installations
You will need to install the following python packages. 

- pip install pyautogui
- pip install tk

# Adding/Importing a trained a ML policy 
Once your policy has been created from training, in the "Policies" folder drag the "imitation_policy.csv" file from the training folder you created to the "POILICY_TO_DRAW" folder and replace the file. The default in the folder is for the lowercase letter a. After it is in the POLICY_TO_DRAW folder, go to the GUI and press the "IMPORT" button to have it ready.

## What it looks like for training on the Character "A"

![Test Image 1](/images/gif.gif)
