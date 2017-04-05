import unittest, os
import acme_dns_tiny
from tests.config_factory import generate_acme_account_rollover_config
from tools.acme_account_delete import account_delete
import tools.acme_account_rollover

ACMEDirectory = os.getenv("GITLABCI_ACMEDIRECTORY", "https://acme-staging.api.letsencrypt.org/directory")

class TestACMEAccountRollover(unittest.TestCase):
    "Tests for acme_account_rollover"

    @classmethod
    def setUpClass(self):
        logassert.setup(self, 'acme_account_rollover')
        self.configs = generate_acme_account_rollover_config()
        super(TestACMEAccountRollover, self).setUpClass()

    # To clean ACME staging server and close correctly temporary files
    @classmethod
    def tearDownClass(self):
        # delete account key registration at end of tests
        account_delete(self.configs["newaccountkey"].name, ACMEDirectory)
        # close temp files correctly
        for tmpfile in self.configs:
            self.configs[tmpfile].close()
        super(TestACMEAccountRollover, self).tearDownClass()

    def test_success_account_rollover(self):
        """ Test success account key rollover """
        with self.assertLogs(level='INFO') as accountrolloverlog:
            tools.acme_account_rollover.main(["--current", self.configs['oldaccountkey'].name,
                                          	    "--new", self.configs['newaccountkey'].name,
                                          	    "--acme-directory", ACMEDirectory])
        self.assertIn("INFO:acme_account_rollover:Account keys rolled over !",
            accountrolloverlog.output)

if __name__ == "__main__":
    unittest.main()
