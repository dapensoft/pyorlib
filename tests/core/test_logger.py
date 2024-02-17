from pyorlib.core.loggers import Logger


class TestLogger:

    def test_creation(self):
        # Arrange | Act
        logger = Logger(name="New Logger", debug=True)

        # Assert
        assert logger
        assert logger.debug_enabled
        logger.info("Test info log")
        logger.debug("Test debug log")
        logger.error("Test error log")
        logger.warning("Test warning log")
