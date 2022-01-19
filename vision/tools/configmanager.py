import configparser
import os
import sys



class ConfigurationManager:
    """
    Projeye ait tüm ilk ayarların yazılı olduğu config_file.yaml dosyasını okuma ve bazı parametrelerini değiştirmek için yaratılan sınıftır.
    """

    def __init__(self):
        self.config_readable, self.config_changeable = self.read_config_file()

    def read_config_file(self):
        """
        Parameters
        ------------
        None:

        Returns
        ------------
        config_readable : configparser - config okunabilir bloğu
        config_changeable : configparser - config değiştirilebilir bloğu
        """

        path_of_the_config_yaml = os.path.dirname(sys.argv[0]) + '/config/config_file.yaml'
        config_f1 =configparser.ConfigParser()
        config_f1.read(path_of_the_config_yaml)
        config_readable = config_f1['readable']
        config_changeable = config_f1['changeable']
        return config_readable, config_changeable

    def set_lastframe(self, last_frame):
        """
        Parameters
        ------------
        last_frame: string - üzerinde çalışılan en son frame numarası
        
        Returns
        ------------
        rtn: Boolean - config verinin yazılma durumu
        """

        path_of_the_config_yaml = os.path.dirname(sys.argv[0]) + '/config/config_file.yaml'
        parser = configparser.ConfigParser()
        parser.read(path_of_the_config_yaml)
        parser.set('changeable', 'last_frame', str(last_frame))
        try:
            with open(path_of_the_config_yaml, "w+") as configfile:
                parser.write(configfile)
                return True
        except:
            return False