Feature: Hello World

    Scenario: Hello World page
        Given I visit site page "/hello/"
        Then I should see "World"
