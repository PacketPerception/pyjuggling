if __name__ == '__main__':
    from .utils_tests import *  # noqa
    from .siteswap_tests import *  # noqa
    from .pattern_tests import *  # noqa
    import unittest
    import logging

    logging.basicConfig(level=logging.DEBUG, fromat='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

    unittest.main()
