#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: hassio_host
author: "marksie1988 / TotalDebug (@marksie1988)"
short_description: Manage Home Assistant (HassIO) host
version_added: "2.0.1"
description:
  - Manage Home Assistant (HassIO, hass.io) host - restart, update, stop
options:
  state:
    description:
      - State of host
    required: true
    choices: ['restarted', 'updated', 'stop']
"""

EXAMPLES = """
# restart HassIO Core
- hassio_host:
    state: restarted
"""

# ===========================================
# Module execution.
#
import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native

hassio = "ha"
host = "ha"


def join(*args):
    return " ".join(list(args))


def restart(ansible):
    cmd = join(hassio, host, "restart")
    return ansible.run_command(cmd)


def update(ansible):
    cmd = join(hassio, host, "update")
    return ansible.run_command(cmd)


def stop(ansible):
    cmd = join(hassio, host, "stop")
    return ansible.run_command(cmd)


def __raise(ex):
    raise ex


def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(required=True, choices=["restarted", "updated", "stop"])
        ),
        # TODO
        supports_check_mode=False,
    )

    switch = {"restarted": restart, "stop": stop, "updated": update}
    state = module.params["state"]

    try:
        action = switch.get(state, lambda: __raise(Exception("Action is undefined")))
        result = action(module)
        module.exit_json(msg=result)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=traceback.format_exc())


if __name__ == "__main__":
    main()
