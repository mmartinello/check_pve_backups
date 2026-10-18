"""

"""

import check_pve_backups as check
import os
import unittest
from unittest.mock import Mock, patch, MagicMock


class ParserTest(unittest.TestCase):
    """
    """
    def test_get_node_vms_with_existing_node(self):
        checker = check.Checker()
        checker._proxmox = MagicMock()
        checker._proxmox.get.return_value = {
            "data": [
                {
                    "vmid": 9999,
                    "name": "test-not-backed-up",
                    "type": "qemu"
                },
                {
                    "name": "ct1",
                    "vmid": 100,
                    "type": "lxc"
                }
            ]
        }

        node_name = 'foo_node'
        vms = check._get_node_vms(node_name)


if __name__ == "__main__":
    unittest.main()
