Feature: Check models existence
  Background:
    Given I have a garden in the database:
      | name          | area | raining |
      | Secret Garden | 45   | false   |
    And I have gardens in the database:
      | name             | area | raining |
      | Octopus's Garden | 120  | true    |
      | Covent Garden    | 200  | true    |
      | 颐和园           | 500  | false   |
    And garden with name "Secret Garden" has fruit in the database:
      | name  | ripe_by    |
      | Apple | 2013-07-02 |
    And I have geese in the database:
      | name |
      | Grey |
    And I have harvesters in the database:
      | make  |
      | Frank |
      | Crank |

  Scenario: Positive checks
    Given I have populated the database
    Then a garden should be present in the database:
      | name          |
      | Secret Garden |
    And gardens should be present in the database:
      | name          | area |
      | Covent Garden | 200  |
    And gardens should not be present in the database:
      | name          | area |
      | Covent Garden | 300  |
    And gardens should be present in the database:
      | @howbig | raining |
      | small   | false   |
      | medium  | true    |
      | big     | true    |
    And there should be 2 harvesters in the database
    And harvesters should be present in the database:
      | rego   |
      | fra001 |
    And harvesters should not be present in the database:
      | rego   |
      | fra002 |

  Scenario: Negative check
    Given I have populated the database
    Then a garden should be present in the database:
      | name            |
      | Botanic Gardens |

  Scenario: Negative check with attributes
    Given I have populated the database
    Then gardens should be present in the database:
      | name          | @howbig |
      | Secret Garden | huge    |

  Scenario: Negative count check
    Given I have populated the database
    Then there should be 2 geese in the database

  Scenario: Negative absence check
    Given I have populated the database
    Then a garden should not be present in the database:
      | name          | @howbig |
      | Secret Garden | small   |
