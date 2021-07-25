import os

if os.environ.get("IS_RASPI",None) is None:
    from agent_py.srv.pubs.cmd_gpio_raspi.dummy import *
else:
    from agent_py.srv.pubs.cmd_gpio_raspi.driver import *