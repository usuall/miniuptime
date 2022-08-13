from mini.config import get_Config
import mini.library as lib


properties = get_Config()
config_sys = properties['SYSTEM']
config_log = properties['LOG']
config_db = properties['DATABASE']

# print(config_sys['LIB_PATH'], config_log['DEBUG_LEVEL'], config_db['HOST'])

lib.set_Logger(config_log['LOG_LEVEL'])
