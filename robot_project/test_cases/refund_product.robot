*** Settings ***
Library    SeleniumLibrary

Documentation    Test suite for refund all products from trash

Suite Teardown   Close All Browsers



*** Test Cases ***
Refund Products From Trash
    Open Stage CloudShop
    Open Trash
    Load All Products And Restore
    
    


*** Keywords ***
Open Stage CloudShop
    Open Browser    https://web-stage.cloudshop.ru/anonymous/login/    chrome
    Maximize Browser Window
    Title Should Be    Авторизация
    Input Text  ${USERNAME_INPUT}     demo@cloudshop.ru
    Input Text  ${PASSWORD_INPUT}      demo
    Click Element   ${LOGIN_BUTTON}
    ${status}=    Run Keyword And Return Status    Wait Until Page Contains Element    ${DASHBOARD_ELEMENT}    timeout=30s
    Run Keyword If    not ${status}    Handle Login Failure
    Log    Successfully logged in

Open Trash
    Click Element   ${TRASH_BUTTON}
    Wait Until Page Contains Element    ${TRASH_TITLE}    timeout=30s
    
Check New Count Increased
    [Arguments]    ${old_count}
    ${new_count}=    Get Element Count    ${PRODUCT_ROW}
    Should Be True    ${new_count} > ${old_count}

Load All Products And Restore
    [Documentation]    Загружает все товары, затем выбирает чекбоксы и восстанавливает товары
    ${prev_count}=    Get Element Count    ${PRODUCT_ROW}
    Log To Console    Начальное количество строк: ${prev_count}

    FOR    ${i}    IN RANGE    1    5
        ${clicked}=    Run Keyword And Return Status    Click Element    ${LOAD_MORE_BUTTON}
        Run Keyword If    not ${clicked}    Log To Console    Кнопка "Загрузить ещё" недоступна — конец списка.    AND    Exit For Loop

        Sleep    5s
        ${new_count}=    Get Element Count    ${PRODUCT_ROW}
        Run Keyword If    ${new_count} == ${prev_count}    Log To Console    Новых строк нет — конец списка.    AND    Exit For Loop

        ${prev_count}=    Set Variable    ${new_count}
        Log To Console    После итерации ${i}: ${prev_count} строк
    END

    Log To Console    Всего загружено строк: ${prev_count}

    # --- Выбор всех чекбоксов ---
    FOR    ${index}    IN RANGE    1    ${rows}+1
        ${label}=    Get WebElement    xpath=(//td[contains(@class,"table-checkbox")]/label)[${index}]
        Execute JavaScript    arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});    ${label}
        Sleep    0.1s

        ${clicked}=    Run Keyword And Return Status    Click Element    ${label}
        Run Keyword If    not ${clicked}    Execute JavaScript    arguments[0].click();    ${label}
        Sleep    0.1s

        ${input}=    Get WebElement    xpath=//*[@id="sidebar"]/div/ui-view/div[2]/div/div/table/tbody/tr[1]
        ${checked}=    Execute JavaScript    return arguments[0].checked;    ${input}

        Run Keyword If    ${checked}    Log To Console    ✅ Checkbox ${index} отмечен.
        Run Keyword Unless    ${checked}    Log To Console    ⚠️ Checkbox ${index} не удалось отметить.
    END

    # --- Клик на кнопку восстановления ---
    Click Element    ${RESTORE_BUTTON}
    Log To Console    Клик по кнопке "Восстановить"

    # --- Проверка результата ---
    Sleep    2s
    ${no_rows}=    Run Keyword And Return Status    Element Should Not Be Visible    ${PRODUCT_ROW}
    Run Keyword If    ${no_rows}    Log To Console    ✅ Все товары восстановлены (нет строк в списке)
    Run Keyword Unless    ${no_rows}    Log To Console    ⚠️ После восстановления остались строки



*** Variables ***
#Locators
${USERNAME_INPUT}   xpath=/html/body/div[2]/div/div/div[2]/div[2]/div/div[1]/div[1]/form/div[2]/div/input
${PASSWORD_INPUT}   xpath=/html/body/div[2]/div/div/div[2]/div[2]/div/div[1]/div[1]/form/div[3]/div[1]/input
${LOGIN_BUTTON}    xpath=/html/body/div[2]/div/div/div[2]/div[2]/div/div[1]/div[1]/form/button
${DASHBOARD_ELEMENT}    xpath=//*[@id="subMenu"]/div/div[2]/div/div/div[1]/a/span
${TRASH_BUTTON}    xpath=//*[@id="subMenu"]/div/div[2]/div/div/div[12]/a/span
${TRASH_TITLE}    xpath=//*[@id="globalMenu"]/div[1]/div/div/div/span
${LOAD_MORE_BUTTON}    xpath=//*[@id="sidebar"]/div/ui-view/div/div/div/a/span[1]/span
${PRODUCT_ROW}         xpath=//*[@id="sidebar"]/div/ui-view/div[2]/div/div/table/tbody/tr[1]
${PRODUCT_CHECKBOX}          xpath=//*[@id="sidebar"]/div/ui-view/div[2]/div/div/table/tbody/tr[1]
${RESTORE_BUTTON}      xpath=//*[@id="sidebar"]/div/ui-view/span/div/div[1]/div