import requests


class RequestsHandler:
    url = "https://gamebackend.pokatilov0802.now.sh/"

    @staticmethod
    def test() -> bool:
        res = requests.get(RequestsHandler.url)
        return res.text == 'running'

    @staticmethod
    def get_json_response(url, data: dict) -> dict:
        res = requests.post(RequestsHandler.url + url, json=data)
        if res.status_code == 200:
            return res.json
        return False


if __name__ == "__main__":
    handler = RequestsHandler
    print(handler.test())