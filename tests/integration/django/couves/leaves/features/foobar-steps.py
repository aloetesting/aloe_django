from aloe import before, after, step


@before.all
def couves_before():
    print("Couves before all")


@after.all
def couves_after():
    print("Couves after all")


@step(r'Given I say foo bar')
def given_i_say_foo_bar(step):
    yeah


@step(r'Then it works')
def then_it_works(step):
    pass
