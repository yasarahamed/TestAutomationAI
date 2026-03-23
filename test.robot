*** Keywords ***

Load Tds
    # Groups repeated steps under one readable name
    Log To Console    Tds Loaded with ncfg

Set Pv
    Log To Console    DC Power Set

Check Cylinder Temperature
    Log To Console    Checking temp 

Tap Water
    Log To Console    Tap water 


*** Test Cases ***

Test
    Load Tds
    Set Pv
    Check Cylinder Temperature
    Tap Water