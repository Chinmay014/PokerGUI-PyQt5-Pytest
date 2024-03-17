*** Settings ***
Documentation    Sikuli and Robotframework
Library    SikuliLibrary    mode=NEW
Library    OperatingSystem

Suite Setup    Run Keywords  Start Sikuli Process  AND  Run Python Script  AND  Read Images
Suite Teardown    Run Keywords  Close Application    ${APP_LOCATION}  AND  Stop Remote Server  AND  Sleep  5

*** Variables ***
${IMAGE_PATH}    PokerGUI.sikuli
${APP_LOCATION}    "F:/DesktopC/PythonUltimateCourse/Robotframework-Sikuli/pokergame/pokergame.exe"
${TITLE_SCREEN}    title_screen.png
${PLAYER_1}    player1.png
${PLAYER_2}    player2.png
${EXIT_BUTTON}    exit.png

*** Test Cases ***
Test 1
    All on Call
# Test 2
#     P1 folds in First Turn
# Test 3
#     P2 folds in First Turn
*** Keywords ***
Read Images
    Add Image Path    ${IMAGE_PATH}
Run Python Script
    # ${result}    Run    py -3 ./path/to/pokergame.py
    Open Application    py -3 ./path/to/pokergame.py
All on Call
    # Wait Until Screen Contain    ${TITLE_SCREEN}    15
    Click    ${PLAYER_1}    xOffset=315    yOffset=294
    Click    ${PLAYER_2}    xOffset=313    yOffset=292
    Click    ${PLAYER_1}    xOffset=315    yOffset=294
    Click    ${PLAYER_2}    xOffset=313    yOffset=292
    Click    ${PLAYER_1}    xOffset=315    yOffset=294
    Click    ${PLAYER_2}    xOffset=313    yOffset=292
    Click    ${PLAYER_1}    xOffset=315    yOffset=294
    Click    ${EXIT_BUTTON}    xOffset=92    yOffset=-3
P1 folds in First Turn
    Click    ${PLAYER_1}    xOffset=312    yOffset=266
    Click    ${EXIT_BUTTON}    xOffset=92    yOffset=-3
P2 folds in First Turn
    Click    ${PLAYER_1}    xOffset=315    yOffset=294
    Click    ${PLAYER_2}    xOffset=312    yOffset=266
    Click    ${EXIT_BUTTON}    xOffset=92    yOffset=-3