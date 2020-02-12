import requests


class RequestsHandler:
    url = "https://yagame-backend.herokuapp.com/"
    # url = "http://localhost:5000/"

    def __init__(self):
        self.session = requests.Session()
        self.test()

    def test(self) -> bool:
        res = self.session.get(RequestsHandler.url)
        return res.text == '<h1>running</h1>'

    def get_json_response(self, url, data: dict) -> dict:
        res = self.session.post(RequestsHandler.url + url, json=data)
        if res.status_code == 200:
            return res.json()
        return res.status_code


handler = RequestsHandler()
if __name__ == "__main__":
    print(handler.test())