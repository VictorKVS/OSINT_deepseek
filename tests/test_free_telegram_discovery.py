import unittest
from types import SimpleNamespace
from tools.free_telegram_discovery import candidate

class FreeDiscoveryTests(unittest.TestCase):
    def test_public_broadcast(self):
        row=candidate(SimpleNamespace(username="PublicOSINT",broadcast=True,title="OSINT Lab"),"forensics","now")
        self.assertEqual(row["channel_id"],"publicosint")
        self.assertEqual(row["status"],"candidate")
        self.assertEqual(row["subscribers"],"")
    def test_private_and_groups_rejected(self):
        self.assertIsNone(candidate(SimpleNamespace(username=None,broadcast=True),"osint","now"))
        self.assertIsNone(candidate(SimpleNamespace(username="GroupName",broadcast=False),"osint","now"))
        self.assertIsNone(candidate(SimpleNamespace(username="bad!",broadcast=True),"osint","now"))

if __name__=="__main__":unittest.main()
