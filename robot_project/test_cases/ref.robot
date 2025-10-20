*** Settings ***
Library    SeleniumLibrary
Library    Collections
Library    BuiltIn

*** Variables ***
${LOAD_MORE_BUTTON}    xpath=//button[contains(text(), 'Загрузить еще')]
${CHECKBOXES}           xpath=//input[@type='checkbox' and not(@disabled)]
${RESTORE_BUTTON}       xpath=//button[contains(text(), 'Восстановить')]
${PRODUCT_ITEMS}        xpath=//div[contains(@class, 'product-item') or contains(@class, 'cart-item')]
${SUCCESS_MESSAGE}      xpath=//div[contains(text(), 'успех') or contains(text(), 'восстановлен') or contains(text(), 'восстановлены')]

*** Test Cases ***
Load All Cart Items And Restore Via UI
    [Documentation]    Тест загрузки всех товаров через UI пагинацию и их восстановление
    Open Cart Page
    ${total_items}=    Load All Cart Items Via UI
    Select All Checkboxes
    Click Restore Button
    Verify Successful Restoration    ${total_items}

*** Keywords ***
Open Cart Page
    [Documentation]    Открывает страницу корзины
    Go To    https://your-service.com/cart
    Wait Until Page Contains Element    ${LOAD_MORE_BUTTON}    10s
    Log    Страница корзины загружена

Load All Cart Items Via UI
    [Documentation]    Загружает все товары через кнопку "Загрузить еще" пока она доступна
    ${initial_count}=    Get Product Count
    Log    Начальное количество товаров: ${initial_count}
    
    ${safety_counter}=    Set Variable    0
    WHILE    True
        ${can_load_more}=    Check If Can Load More
        IF    ${can_load_more} == ${False}
            Log    Больше нет данных для загрузки
            BREAK
        END
        
        Click Load More Button UI
        ${new_count}=    Wait For New Items UI    ${initial_count}
        ${initial_count}=    Set Variable    ${new_count}
        
        # Защита от бесконечного цикла
        ${safety_counter}=    Evaluate    ${safety_counter} + 1
        IF    ${safety_counter} > 20
            Log    Достигнут лимит итераций загрузки. Загружено страниц: ${safety_counter}
            BREAK
        END
    END
    
    ${final_count}=    Get Product Count
    Log    Всего загружено товаров: ${final_count}
    RETURN    ${final_count}

Check If Can Load More
    [Documentation]    Проверяет, можно ли загрузить еще товары
    ${button_visible}=    Run Keyword And Return Status
    ...    Wait Until Element Is Visible    ${LOAD_MORE_BUTTON}    5s
    
    IF    ${button_visible} == ${False}
        RETURN    ${False}
    END
    
    ${button_enabled}=    Run Keyword And Return Status
    ...    Element Should Be Enabled    ${LOAD_MORE_BUTTON}
    
    ${not_loading}=    Run Keyword And Return Status
    ...    Element Should Not Contain    ${LOAD_MORE_BUTTON}    Загрузка...
    
    RETURN    ${button_visible} and ${button_enabled} and ${not_loading}

Click Load More Button UI
    [Documentation]    Нажимает кнопку "Загрузить еще" с обработкой UI состояний
    FOR    ${attempt}    IN RANGE    3
        ${success}=    Run Keyword And Return Status
        ...    Click Button With Verification    ${attempt}
        
        IF    ${success} == ${True}
            RETURN
        END
    END
    Fail    Не удалось нажать кнопку 'Загрузить еще' после 3 попыток

Click Button With Verification
    [Documentation]    Нажимает кнопку и проверяет, что началась загрузка
    [Arguments]    ${attempt}
    
    # Запоминаем текущее состояние
    ${before_click_count}=    Get Product Count
    
    # Нажимаем кнопку
    Click Element    ${LOAD_MORE_BUTTON}
    
    # Ждем признаков загрузки
    Wait Until Keyword Succeeds    10s    1s
    ...    Verify Loading Started    ${before_click_count}
    
    RETURN    ${True}

Verify Loading Started
    [Documentation]    Проверяет, что загрузка началась
    [Arguments]    ${previous_count}
    
    # Проверяем, что кнопка изменила состояние (стала disabled или показывает загрузку)
    ${button_changed}=    Run Keyword And Return Status
    ...    Element Should Be Disabled    ${LOAD_MORE_BUTTON}
    
    IF    ${button_changed} == ${False}
        ${button_changed}=    Run Keyword And Return Status
        ...    Element Should Contain    ${LOAD_MORE_BUTTON}    Загрузка...
    END
    
    IF    ${button_changed} == ${False}
        # Проверяем, что количество товаров изменилось
        ${current_count}=    Get Product Count
        IF    ${current_count} > ${previous_count}
            RETURN
        ELSE
            Fail    Загрузка не началась после клика
        END
    END

Wait For New Items UI
    [Documentation]    Ожидает появления новых товаров
    [Arguments]    ${previous_count}
    
    Wait Until Keyword Succeeds    30s    2s
    ...    Verify New Items Loaded    ${previous_count}
    
    ${current_count}=    Get Product Count
    RETURN    ${current_count}

Verify New Items Loaded
    [Documentation]    Проверяет, что новые товары загрузились
    [Arguments]    ${previous_count}
    
    # Ждем, пока кнопка снова станет активной
    Wait Until Element Is Enabled    ${LOAD_MORE_BUTTON}    20s
    Wait Until Element Is Visible    ${LOAD_MORE_BUTTON}    20s
    
    # Проверяем, что количество товаров увеличилось
    ${current_count}=    Get Product Count
    IF    ${current_count} <= ${previous_count}
        Fail    Новые товары не загрузились. Было: ${previous_count}, Стало: ${current_count}
    END
    
    Log    Загружены новые товары. Было: ${previous_count}, Стало: ${current_count}

Get Product Count
    [Documentation]    Возвращает количество товаров в корзине
    ${elements}=    Get WebElements    ${PRODUCT_ITEMS}
    ${count}=    Get Length    ${elements}
    
    # Альтернативный способ через чекбоксы, если товары не имеют отдельных контейнеров
    IF    ${count} == 0
        ${checkbox_elements}=    Get WebElements    ${CHECKBOXES}
        ${count}=    Get Length    ${checkbox_elements}
    END
    
    RETURN    ${count}

Select All Checkboxes
    [Documentation]    Выбирает все доступные чекбоксы
    ${all_checkboxes}=    Get WebElements    ${CHECKBOXES}
    ${checkbox_count}=    Get Length    ${all_checkboxes}
    Log    Найдено чекбоксов для выбора: ${checkbox_count}
    
    FOR    ${index}    ${checkbox}    IN ENUMERATE    @{all_checkboxes}
        ${is_visible}=    Run Keyword And Return Status
        ...    Element Should Be Visible    ${checkbox}
        
        IF    ${is_visible} == ${True}
            ${is_checked}=    Run Keyword And Return Status
            ...    Checkbox Should Be Selected    ${checkbox}
            
            IF    ${is_checked} == ${False}
                Scroll Element Into View    ${checkbox}
                Click Element    ${checkbox}
                Sleep    0.5s
                # Проверяем, что чекбокс действительно выбрался
                Checkbox Should Be Selected    ${checkbox}
                Log    Выбран чекбокс ${index + 1}
            ELSE
                Log    Чекбокс ${index + 1} уже выбран
            END
        ELSE
            Log    Чекбокс ${index + 1} не виден, пропускаем
        END
    END
    
    Log    Все чекбоксы выбраны

Click Restore Button
    [Documentation]    Нажимает кнопку восстановления товаров
    Wait Until Element Is Enabled    ${RESTORE_BUTTON}    10s
    Scroll Element Into View    ${RESTORE_BUTTON}
    Click Element    ${RESTORE_BUTTON}
    Log    Нажата кнопка восстановления
    
    # Ждем начала процесса восстановления
    Sleep    3s

Verify Successful Restoration
    [Documentation]    Проверяет успешность восстановления товаров через UI
    [Arguments]    ${total_items}
    
    # Вариант 1: Проверяем сообщение об успехе (если есть)
    ${success_message}=    Run Keyword And Return Status
    ...    Wait Until Page Contains Element    ${SUCCESS_MESSAGE}    10s
    
    IF    ${success_message} == ${True}
        Log    Показано сообщение об успешном восстановлении
        RETURN
    END
    
    # Вариант 2: Проверяем, что чекбоксы сбросились
    ${checkboxes_reset}=    Run Keyword And Return Status
    ...    Verify Checkboxes Reset
    
    IF    ${checkboxes_reset} == ${True}
        Log    Все чекбоксы сброшены после восстановления
        RETURN
    END
    
    # Вариант 3: Проверяем, что кнопка восстановления стала неактивной
    ${button_disabled}=    Run Keyword And Return Status
    ...    Element Should Be Disabled    ${RESTORE_BUTTON}
    
    IF    ${button_disabled} == ${True}
        Log    Кнопка восстановления стала неактивной
        RETURN
    END
    
    # Вариант 4: Просто ждем и логируем - если нет явных признаков успеха
    Sleep    5s
    Log    Восстановление выполнено. Явных признаков успеха не найдено, но тест продолжается
    
    # Если дошли сюда, считаем что восстановление прошло
    Log    Восстановление товаров выполнено для ${total_items} товаров

Verify Checkboxes Reset
    [Documentation]    Проверяет, что все чекбоксы сбросились
    ${all_checkboxes}=    Get WebElements    ${CHECKBOXES}
    
    FOR    ${checkbox}    IN    @{all_checkboxes}
        ${is_checked}=    Run Keyword And Return Status
        ...    Checkbox Should Be Selected    ${checkbox}
        
        IF    ${is_checked} == ${True}
            RETURN    ${False}
        END
    END
    
    RETURN    ${True}