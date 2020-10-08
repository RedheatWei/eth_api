from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
import json
import requests


class Accounts(View):
    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        # passwd = request.POST.get("password")
        body = json.loads(request.body.decode('utf-8'))
        res = requests.post(
            url="http://127.0.0.1:8545/",
            json={"method": "personal_newAccount", "params": [body["password"]], "id": 67, "jsonrpc": "2.0"},
            headers={"Content-Type": "application/json"}
        )
        data = json.loads(res.content.decode("utf-8"))
        return JsonResponse(data, safe=False)


class Trans(View):
    def post(self, request):
        # passwd = request.POST.get("password")
        body = json.loads(request.body.decode('utf-8'))
        res = requests.post(
            url="http://127.0.0.1:8545/",
            json={"jsonrpc": "2.0", "method": "eth_sendTransaction", "params": [{
                "from": "0xb60e8dd61c5d32be8058bb8eb970870f07233155",
                "to": "0xd46e8dd67c5d32be8058bb8eb970870f07244567",
                "gas": "0x76c0",
                "gasPrice": "0x9184e72a000",
                "value": "0x9184e72a",
                "data": "0xd46e8dd67c5d32be8d46e8dd67c5d32be8058bb8eb970870f072445675058bb8eb970870f072445675"
            }], "id": 1},
            headers={"Content-Type": "application/json"}
        )
        data = json.loads(res.content.decode("utf-8"))
        return JsonResponse(data, safe=False)
