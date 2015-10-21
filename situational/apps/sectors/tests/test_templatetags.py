from situational.testing import BaseCase

from ..templatetags import friendly_socs


class TestFriendlySocs(BaseCase):
    def test_friendly_soc_title(self):
        with self.subTest("cleans n.e.c. socs"):
            friendly = friendly_socs.friendly_soc_title(
                "Customer service occupations n.e.c.")
            self.assertEqual(friendly, "Customer service occupations")

        with self.subTest("leaves non-n.e.c. socs alone"):
            friendly = friendly_socs.friendly_soc_title(
                "Crane drivers")
            self.assertEqual(friendly, "Crane drivers")

    def test_friendly_soc_description(self):
        with self.subTest("cleans n.e.c. socs"):
            friendly = friendly_socs.friendly_soc_description(
                "Job holders in this unit group perform a variety of customer "
                "service occupations not elsewhere classified in MINOR GROUP "
                "721: Customer Service Occupations.")
            self.assertEqual(
                friendly,
                "Job holders in this unit group perform a variety of customer "
                "service occupations.")

        with self.subTest("leaves non-n.e.c. socs alone"):
            friendly = friendly_socs.friendly_soc_description(
                "Van drivers collect, transport and deliver goods in vehicles "
                "up to 7.5 tonnes in weight.")
            self.assertEqual(
                friendly,
                "Van drivers collect, transport and deliver goods in vehicles "
                "up to 7.5 tonnes in weight.")
