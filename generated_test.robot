*** Settings ***
Resource    keywords.resource

*** Test Cases ***
# Tests a sequence of loading TDS, checking temperature, setting PV, checking temperature again, tapping water, and finally setting PV.
Perform Sequence Of Loading, Checks, PV Adjustments, And Tapping
    Load Tds
    Check Cylinder Temperature
    Set Pv
    Check Cylinder Temperature
    Tap Water
    Set Pv