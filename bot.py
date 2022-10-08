from enum import Enum
import json
import string
from typing import Dict, List, Union
import urllib.request as request


class TelegramMethod(Enum):
    GET_ME = 'getMe'
    GET_UPDATES = 'getUpdates'


class GetMeResponse():
    def __init__(self, response: list) -> None:
        self.username = response['username']


class UpdateResponse():
    def __init__(self, response: Dict[str, Union[str, int]]) -> None:
        self.id = response['update_id']

        try:
            self.message = response['message']['text']
        except KeyError:
            self.message = 'NO MESSAGE! I THINK IT IS STICKER OR SMTH...'


class TelegramBot:
    def __init__(self, token: string) -> None:
        self.tgUrl = "https://api.telegram.org/bot%s/{method}" % (token)

        self.__last = None

    def listenUpdates(self) -> None:
        while (True):
            lastUpdate = self.getUpdates()[-1]

            if self.__last == lastUpdate.id:
                continue
            else:
                self.__last = lastUpdate.id

            print(lastUpdate.message)

    def getMe(self) -> GetMeResponse:
        response = self.__sendRequest(TelegramMethod.GET_ME)

        return GetMeResponse(response)

    def getUpdates(self) -> List[UpdateResponse]:
        response = self.__sendRequest(TelegramMethod.GET_UPDATES)

        return list(map(lambda update: UpdateResponse(update), response))

    def __sendRequest(self, method: TelegramMethod) -> Dict[str, Union[str, int]]:
        response = request.urlopen(self.tgUrl.format(method=method.value))

        return json.loads(response.read().decode())['result']
