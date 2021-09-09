from datetime import datetime
from typing import ContextManager
from django import http
from django.http import response
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .api import *
from julo import jwt
from rest_framework import status as httpstatus
from rest_framework.permissions import IsAuthenticated, AllowAny
# Create your views here.
# create account


@api_view(['POST'])
@permission_classes([AllowAny])
def CreateAccount(request):
    dataPost = UserWalletSerializer(data=request.data)
    if dataPost.is_valid():
        try:
            dataPost.save()
        except Exception as e:
            return Response({"fail": dataPost.errors})
    return Response({"success": "created", "data": {"token": jwt.generate_access_token(dataPost.data)}}, status=httpstatus.HTTP_201_CREATED)


@api_view(['POST', 'GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def EnablingTheWallet(request):
    if request.method == "POST":
        user = jwt.jwt_decode(request)
        # get user wallet
        status = 1
        wallet = Wallet.objects.filter(owner=user)
        respon = None
        # if wallet wallet count == 0 then create enabled wallet
        if wallet.count() == 0:
            newWallet = {
                "owner": user,
                "status": status,
            }
            walletSerial = WalletSerializer(data=newWallet)
            if walletSerial.is_valid():
                walletSerial.save()
                respon = Response(
                    {"status": "success", "data": walletSerial.data}, status=httpstatus.HTTP_201_CREATED)

        # if not cek the wallet status
        else:
            print("wallet is not 0")
            if wallet.last().status != 0:
                jsonwallet = WalletSerializer(wallet.last())
                respon = Response({"status": "Failed", "data": jsonwallet.data,
                                  "message": "Wallet Already Enabled"}, status=httpstatus.HTTP_500_INTERNAL_SERVER_ERROR)
        return respon
    elif request.method == "GET":
        user = jwt.jwt_decode(request)
        respon = None
        # get wallet
        wallet = Wallet.objects.filter(owner=user)
        if wallet.count() == 0:
            respon = Response({"status": "Failed", "data": {
            }, "msg": "Wallet Not Found"}, status=httpstatus.HTTP_404_NOT_FOUND)
        else:
            walletjson = WalletSerializer(wallet.last(), many=False)
            respon = Response(
                {"status": "Success", "data": walletjson.data}, status=httpstatus.HTTP_200_OK)
        return respon
    elif request.method == "PATCH":
        user = jwt.jwt_decode(request)
        dataWalet = {
            "status": 0,
            "owner": user,
        }
        walletData = WalletSerializer(data=dataWalet)
        if walletData.is_valid():
            walletData.save()
        else:
            return Response({"status": "Failed", "msg": walletData.errors}, status=httpstatus.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"success": "success", "data": {"wallet": walletData.data}}, status=httpstatus.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def DepositVMoney(request):
    user = jwt.jwt_decode(request)
    # cek walet status
    waletStatus = Wallet.objects.filter(owner=user).last()
    if waletStatus.status == "0":
        return Response({"status": "Failed", "msg": "Walet Is Not Enable"}, status=httpstatus.HTTP_500_INTERNAL_SERVER_ERROR)


    amount = request.POST.get("amount")
    reference_id = request.POST.get("reference_id")
    dataKoran = {
        "wallet_id": Wallet.objects.get(owner=user).pk,
        "reference_id": reference_id,
        "deposit_by": user.pk,
        "deposit_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "amount": amount,
    }
    lb = None
    last_balance = Koran.objects.filter(wallet_id=dataKoran["wallet_id"])
    if last_balance.count() == "0":
        lb = 0
    else:
        lb = last_balance.last().balance

    balance = lb + int(amount)
    dataKoran["balance"] = balance

    print("dataKoran =>", dataKoran)
    json = DepositSerializer(data=dataKoran)
    if json.is_valid():
        json.save()
    else:
        return Response({"data": {"deposit": {}}, "status": "fail", "msg": json.errors}, status=httpstatus.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({"data": {"deposit": json.data}, "status": "success"}, status=httpstatus.HTTP_200_OK)




@api_view(["POST"])
@permission_classes([IsAuthenticated])
def WithDrawVMoney(request):
    user = jwt.jwt_decode(request)
    # cek walet status
    waletStatus = Wallet.objects.filter(owner=user).last().status
    if waletStatus == 0:
        return Response({"status": "Failed", "msg": "Walet Is Not Enable"}, status=httpstatus.HTTP_500_INTERNAL_SERVER_ERROR)

    amount = request.POST.get("amount")
    reference_id = request.POST.get("reference_id")
    dataKoran = {
        "wallet_id": Wallet.objects.get(owner=user).pk,
        "reference_id": reference_id,
        "withdrawal_by": user.pk,
        "withdrawal_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "amount": amount,
    }
    lb = None
    last_balance = Koran.objects.filter(wallet_id=dataKoran["wallet_id"])
    if last_balance.count() == 0:
        lb = 0
    else:
        lb = last_balance.last().balance

    balance = lb - int(amount)
    dataKoran["balance"] = balance

    json = WithdrawalSerializer(data=dataKoran)
    if json.is_valid():
        json.save()
    else:
        return Response({"data": {"withdraw": {}}, "status": "fail", "msg": json.errors}, status=httpstatus.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({"data": {"withdraw": json.data}, "status": "success"}, status=httpstatus.HTTP_200_OK)
