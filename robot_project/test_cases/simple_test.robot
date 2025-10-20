*** Settings ***
Documentation    Test suite for product creation in Ainur application
Resource         ../resources/keywords.robot
Suite Setup      Open Stage Application
Suite Teardown   Close All Browsers

*** Test Cases ***
Create Product Successfully
    [Documentation]    Verify successful product creation in Ainur
    [Tags]             product    regression
    Given User Is Logged In
    When User Navigates To Product Page
    And User Creates New Product
    ...    name=AinurAutoTest
    ...    article=1027514
    ...    purchase_price=450.5

*** Keywords ***
User Creates New Product
    [Arguments]    ${name}    ${article}    ${purchase_price}
    Click Create Product
    Input Product Name    ${name}
    Click Generate Barcode
    Input Article    ${article}
    Select Marking Type
    # Select Category
    Input Purchase Price    ${purchase_price}
    Toggle Checkbox    ${CHECKBOX_EXCISABLE_PRODUCT}    ${CHECKBOX_WEIGHT_GOODS}
    Save Product