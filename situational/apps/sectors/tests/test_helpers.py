from situational.testing import BaseCase

from sectors.helpers import LMIForAllClient, LMIForAllException


class TestLMIForAllClient(BaseCase):
    WORKING_SOC_CODE = '5323'
    FAKE_SOC_CODE = '9999999'

    def setUp(self):
        self.lmi = LMIForAllClient()

    def test_clean_add_titles(self):
        data = self.lmi.soc_code_info(self.WORKING_SOC_CODE)
        self.assertTrue('Furniture Polisher' in data['add_titles'])

    def test_soc_info_404(self):
        self.assertRaises(
            LMIForAllException, self.lmi.soc_code_info, self.FAKE_SOC_CODE)

    def test_hours_worked(self):
        self.assertEqual(self.lmi.hours_worked(self.WORKING_SOC_CODE), 43)

    def test_pay(self):
        self.assertEqual(self.lmi.pay(self.WORKING_SOC_CODE), 550)

    def test_jobs_breakdown(self):
        self.assertEqual(
            self.lmi.jobs_breakdown('SW1A 1AA')[0]['description'],
            "Protective Service Occupations"
        )
