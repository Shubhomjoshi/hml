import configparser
config_path = "..\\configfiles\\config.ini"


class ReadConfigData:
    def get_config_data(self, section_name, variable):
        self.config = configparser.RawConfigParser()
        self.config.read(config_path)
        return self.config.get(section_name, variable)
