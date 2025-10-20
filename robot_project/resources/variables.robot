*** Settings ***
Library    OperatingSystem
Library    String

*** Variables ***
# Application Settings
${URL}                 https://web-stage.cloudshop.ru/anonymous/login/
${BROWSER}             chrome

# Locators
${LOGIN_INPUT}         login
${PASSWORD_INPUT}      password
${LOGIN_BUTTON}        xpath=//BUTTON[@ng-class='{disabled: loading}']
${DASHBOARD_ELEMENT}   xpath=//*[@id="globalMenu"]/div[1]/div

${PRODUCT_MENU}        xpath=//*[@id="subMenu"]/div/div[2]/div/div/div[3]/a/span
${PAGINATION_ELEMENT}  xpath=//*[@id="pagination"]
${NEW_PRODUCT_BUTTON}  xpath=//*[@id="sidebar"]/div/ui-view/ui-view/div[1]/div[3]/div/a[1]
${PRODUCT_MODAL}       xpath=//*[@id="state-modal"]/div[2]/div[2]/div/form

# Product Locators
${INPUT_NAME}          xpath=//*[@id="state-modal"]/div[2]/div[2]/div/form/ng-include[1]/div/div[2]/input
${INPUT_ARTICLE}       xpath=//*[@id="state-modal"]/div[2]/div[2]/div/form/ng-include[1]/div/div[3]/div[3]/input
${INPUT_PURCHASE}      xpath=//input[@ng-model='data.purchase']
${BUTTON_SAVE_PRODUCT}         xpath=//*[@id="state-modal"]/div[2]/div[1]/div[2]/div/a
${BUTTON_GENERATE_BARCODE}    xpath=//*[@id="state-modal"]/div[2]/div[2]/div/form/ng-include[1]/div/div[3]/div[2]/label/span[2]/a

${MARKING_DROPDOWN}    xpath=//*[@id="state-modal"]/div[2]/div[2]/div/form/ng-include[1]/div/div[4]/div[3]/div
${MARKING_DROPDOWN_ITEM}    xpath=//*[@id="state-modal"]/div[2]/div[2]/div/form/ng-include[1]/div/div[4]/div[3]/div/div[2]/div[29]

${CATEGORIES_DROPDOWN}    xpath=//*[@id="state-modal"]/div[2]/div[2]/div/form/ng-include[1]/div/div[7]/div
${CATEGORIES_DROPDOWN_ITEM}    xpath=///*[@id="state-modal"]/div[2]/div[2]/div/form/ng-include[1]/div/div[7]/div

${CHECKBOX_EXCISABLE_PRODUCT}    xpath=//*[@id="state-modal"]/div[2]/div[2]/div/form/ng-include[1]/div/div[5]/div/label
${CHECKBOX_WEIGHT_GOODS}    xpath=//*[@id="state-modal"]/div[2]/div[2]/div/form/ng-include[1]/div/div[8]/div[2]

