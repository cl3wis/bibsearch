import configparser
import logging
import os
import platform
import tempfile

class Config():
    defaults = {
        "bibsearch" : {
              "bibsearch_dir": os.path.expanduser("~/.bibsearch")
            , "download_dir": os.path.expanduser("~/.bibsearch/papers")
            , "open_command": "xdg-open" if platform.system() == "Linux" else "open"
            , "database_url": "https://github.com/mjpost/bibsearch/raw/master/resources/"
            , "custom_key_format": "{surname}{year}{suffix}:{title}"
            , "default_output_format": "txt"
            , "editor": os.environ.get("EDITOR", "nano")
        }
        , "macros" : {
              '@acl': 'venue:"Annual Meeting of the Association for Computational Linguistics"'
            , '@emnlp': 'venue:"Conference on Empirical Methods in Natural Language Processing"'
            , '@wmt': '(venue:"Workshop on Statistical Machine Translation" OR venue:"Conference on Machine Translation")'
            , '@naacl': 'venue:"Conference of the North American Chapter of the Association for Computational Linguistics"'
            , '@cl': 'venue:"Computational Linguistics"'  # Probably useless because the terms comes up in several conferences as well
            , '@arxiv': 'venue:"Computing Research Repository"'
            , '@corr': 'venue:"Computing Research Repository"'
            , '@lrec': 'venue:"International Conference on Language Resources and Evaluation"'
        }
    }

    def __init__(self, config_file: str = None):
        config = configparser.ConfigParser()

        # Setup items from defaults
        config.read_dict(self.__class__.defaults)

        # Override those defaults from the config file
        if config_file is None:
            config_file = self._check_for_existing_config()
        config.read(config_file)

        # Make available as member variables
        for k, v in config["bibsearch"].items():
            if k in self.__class__.defaults["bibsearch"]:
                self.__setattr__(k, v)
            else:
                logging.warning("Unknown config option '%s'", k)

        self.macros = config["macros"]

    @classmethod
    def _check_for_existing_config(cls):
        # the default if XDG_CONFIG_HOME isn't set is  ~/.config
        xdg_config_home = os.environ.get("XDG_CONFIG_HOME") or os.path.expanduser("~/.config")
        # check there for a config file
        if os.path.exists(os.path.join(xdg_config_home, "bibsearch/config")):
            config_file = os.path.join(xdg_config_home, "bibsearch/config")
        # otherwise, use ~/.bibsearch/config
        config_file = os.path.expanduser("~/.bibsearch/config")
        return config_file

    @classmethod
    def get_default(cls, key: str) -> str:
        return cls.defaults['bibsearch'][key]
