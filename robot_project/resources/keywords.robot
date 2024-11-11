*** Settings ***
Documentation    Keywords for Ainur application interactions
Library          SeleniumLibrary
Resource         variables.robot

*** Variables ***
${ENV_FILE}    ./config/.env

*** Keywords ***
Open Ainur Application
    Get Env Credentials
    Log    Opening browser with URL: ${URL}
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Title Should Be    Sign in
    Log    Browser opened successfully

User Is Logged In
    Log    Attempting to log in with username: ${USERNAME}
    Input Text    ${LOGIN_INPUT}    ${USERNAME}
    Input Text    ${PASSWORD_INPUT}    ${PASSWORD}
    Click Element    ${LOGIN_BUTTON}
    Run Keyword And Handle Error    Wait Until Page Contains Element    ${DASHBOARD_ELEMENT}    timeout=10s    Handle Login Failure
    Log    Successfully logged in

Handle Login Failure
    Log    Login failed: Invalid credentials or the dashboard element was not found.    WARN
    Capture Page Screenshot
    Fail    Login failed due to invalid credentials or timeout waiting for the dashboard.

User Navigates To Product Page
    Click Element    ${PRODUCT_MENU}
    Wait Until Page Contains Element    ${PAGINATION_ELEMENT}    timeout=15s

Input Product Name
    [Arguments]    ${name}
    Click Element    ${NEW_PRODUCT_BUTTON}
    Wait Until Page Contains Element    ${PRODUCT_MODAL}    timeout=10s
    Input Text    ${INPUT_NAME}    ${name}

Input Article
    [Arguments]    ${article}
    Input Text    ${INPUT_ARTICLE}    ${article}

Select Marking Type
    Wait Until Element Is Visible    ${MARKING_DROPDOWN}    timeout=10s
    Click Element    ${MARKING_DROPDOWN}
    Wait Until Element Is Visible    ${MARKING_DROPDOWN_ITEM}    timeout=10s
    Click Element    ${MARKING_DROPDOWN_ITEM}

Input Purchase Price
    [Arguments]    ${price}
    Input Text    ${INPUT_PURCHASE}    ${price}

Save Product
    Wait Until Element Is Visible    ${SAVE_BUTTON}    timeout=10s
    Click Element    ${SAVE_BUTTON}
