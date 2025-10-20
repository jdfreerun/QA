*** Settings ***
Documentation    Ключевые слова для теста Stage CloudShop
Library          SeleniumLibrary
Resource         variables.robot

*** Variables ***
${ENV_FILE}    ./config/.env

*** Keywords ***
Open Stage Application
    [Documentation]    Открытие страницы авторизации
    Get Env Credentials
    Log    Opening browser with URL: ${URL}
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Title Should Be    Авторизация
    Log    Browser opened successfully

User Is Logged In
    [Documentation]    Авторизация пользователя
    Log    Attempting to log in with username: ${USERNAME}
    Input Text    ${LOGIN_INPUT}    ${USERNAME}
    Input Text    ${PASSWORD_INPUT}    ${PASSWORD}
    Click Element    ${LOGIN_BUTTON}
    ${status}=    Run Keyword And Return Status    Wait Until Page Contains Element    ${DASHBOARD_ELEMENT}    timeout=10s
    Run Keyword If    not ${status}    Handle Login Failure
    Log    Successfully logged in

Handle Login Failure
    Log    Login failed: Invalid credentials or the dashboard element was not found.    WARN
    Capture Page Screenshot
    Fail    Login failed due to invalid credentials or timeout waiting for the dashboard.

User Navigates To Product Page
    Click Element    ${PRODUCT_MENU}
    Wait Until Page Contains Element    ${PAGINATION_ELEMENT}    timeout=15s

Click Create Product
    Click Element    ${NEW_PRODUCT_BUTTON}
    Wait Until Page Contains Element    ${PRODUCT_MODAL}    timeout=10s

Input Product Name
    [Arguments]    ${name}
    Input Text    ${INPUT_NAME}    ${name}  timeout=20s

Click Generate Barcode
    Click Element    ${BUTTON_GENERATE_BARCODE}

Input Article
    [Arguments]    ${article}
    Input Text    ${INPUT_ARTICLE}    ${article}

Select Marking Type
    Wait Until Element Is Visible    ${MARKING_DROPDOWN}    timeout=10s
    Click Element    ${MARKING_DROPDOWN}
    Wait Until Element Is Visible    ${MARKING_DROPDOWN_ITEM}    timeout=10s
    Click Element    ${MARKING_DROPDOWN_ITEM}

Select Category
    Wait Until Element Is Visible    ${CATEGORIES_DROPDOWN}    timeout=10s
    Click Element    ${CATEGORIES_DROPDOWN}
    Wait Until Element Is Visible    ${CATEGORIES_DROPDOWN_ITEM}    timeout=10s
    Click Element    ${CATEGORIES_DROPDOWN_ITEM}

Input Purchase Price
    [Arguments]    ${price}
    Input Text    ${INPUT_PURCHASE}    ${price}

Toggle Checkbox
    [Arguments]    @{checkbox_locators}
    FOR    ${checkbox_locator}    IN    @{checkbox_locators}
        Click Element    ${checkbox_locator}
    END

Save Product
    Wait Until Element Is Visible    ${BUTTON_SAVE_PRODUCT}    timeout=10s
    Click Element    ${BUTTON_SAVE_PRODUCT}

Get Env Credentials
    ${env_file}=    Get File    ${CURDIR}/../config/.env
    @{lines}=    Split To Lines    ${env_file}
    FOR    ${line}    IN    @{lines}
        ${key}    ${value}=    Split String    ${line}    =
        Set Suite Variable    ${${key}}    ${value}
    END
    Log    Username: ${USERNAME}
    Log    Password: ${PASSWORD}