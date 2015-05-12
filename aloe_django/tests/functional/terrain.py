from splinter.browser import Browser
from aloe import before, after, world


@before.harvest
def setup(server):
    world.browser = Browser()


@after.harvest
def cleanup(server):
    world.browser.quit()
