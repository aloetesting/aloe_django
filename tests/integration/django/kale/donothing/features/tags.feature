Feature: Test harvesting tags
    As a programmer
    I want to run only some tags
    So that I can choose a group of tests related to a feature

    Scenario: untagged
        Given step passes

    @passes
    Scenario: tagged (works)
        Given step passes

    @fails
    Scenario: tagged (fails)
        Given step fails
