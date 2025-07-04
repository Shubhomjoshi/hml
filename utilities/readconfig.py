import configparser
import os

config_path = os.path.join(os.path.dirname(__file__), '..', 'configfiles', 'config.ini')
config_path = os.path.abspath(config_path)  # Get absolute path


class ReadConfigData:
    def get_config_data(self, section_name, variable):
        self.config = configparser.RawConfigParser()
        self.config.read(config_path)
        return self.config.get(section_name, variable)
