*** Settings ***
Library    OperatingSystem
Library    String

*** Variables ***
# Application Settings
${URL}                 https://web.ainur.app/anonymous/login/
${BROWSER}             chrome

# Locators
${LOGIN_INPUT}         login
${PASSWORD_INPUT}      password
${LOGIN_BUTTON}        xpath=//BUTTON[@ng-class='{disabled: loading}']
${DASHBOARD_ELEMENT}   xpath=(//SPAN[@translate=''][text()='Dashboard'])[1]

${PRODUCT_MENU}        xpath=//*[@id="subMenu"]/div/div[2]/div/div/div[2]/a
${PAGINATION_ELEMENT}  xpath=//*[@id="pagination"]
${NEW_PRODUCT_BUTTON}  xpath=//*[@id="sidebar"]/div/ui-view/ui-view/div[1]/div[3]/div/a[1]
${PRODUCT_MODAL}       xpath=//*[@id="state-modal"]/div[2]

${INPUT_NAME}          xpath=//input[@ng-model='data.name']
${INPUT_ARTICLE}       xpath=//*[@id="state-modal"]/div[2]/div[2]/div/form/ng-include[1]/div/div[3]/div[3]/input
${INPUT_PURCHASE}      xpath=//input[@ng-model='data.purchase']
${SAVE_BUTTON}         xpath=//a[contains(@class, 'ui button green') and not(contains(@class, 'disabled'))]//span[text()='Save']

${MARKING_DROPDOWN}    xpath=//*[@id="state-modal"]/div[2]/div[2]/div/form/ng-include[1]/div/div[4]/div[6]/div
${MARKING_DROPDOWN_ITEM}    xpath=//*[@id="state-modal"]/div[2]/div[2]/div/form/ng-include[1]/div/div[4]/div[6]/div/div[2]/div[3]

*** Keywords ***
Get Env Credentials
    ${env_file}=    Get File    ${CURDIR}/../config/.env
    @{lines}=    Split To Lines    ${env_file}
    FOR    ${line}    IN    @{lines}
        ${key}    ${value}=    Split String    ${line}    =
        Set Suite Variable    ${${key}}    ${value}
    END
    Log    Username: ${USERNAME}
    Log    Password: ${PASSWORD}