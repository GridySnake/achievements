from models.api.chess_com import Chesscom
from models.api.twitch_tv import Twitch
from models.api.youtube import Youtube
from models.api.steam_games import Steam
from models.api.stepik import Stepik
from models.api.fitnesspal import Fitnesspal
from models.api.api_parameters import *
import inspect


class ServicesConfig:
    service_classes = {
        0: Chesscom,
        1: Twitch,
        2: Youtube,
        4: Steam,
        5: Stepik,
        6: Fitnesspal
    }
    service_functions = {}

    @classmethod
    def update(cls, func):
        cls.service_functions = func


service_class_parameter = {
        0: ChesscomParameter,
        1: TwitchParameter,
        2: YoutubeParameter,
        4: SteamParameter,
        5: StepikParameter,
        6: FitnesspalParameter
    }
ll = []
for i in service_class_parameter.values():
    func = {j[0]: j[1] for j in inspect.getmembers(i)}
    func = dict(filter(lambda x: x[0] in list(func.keys())[list(func.keys()).index('__weakref__')+1:], func.items()))
    for j in func.keys():
        args = {k[0]: k[1] for k in inspect.signature(func[j]).parameters.items()}
        ll.append(i.__name__.replace('Parameter', '') + j + ''.join([k for k in args.keys()]))
l = []
for i in ServicesConfig.service_classes.values():
    func1 = {j[0]: j[1] for j in inspect.getmembers(i)}
    func1 = dict(filter(lambda x: x[0] in list(func1.keys())[list(func1.keys()).index('__weakref__')+1:], func1.items()))
    for j in func1.keys():
        l.append(func1[j])
service_functions = {ll[i]: l[i] for i in range(len(l))}
update = 0
# if update == 1:
ServicesConfig.update(service_functions)
