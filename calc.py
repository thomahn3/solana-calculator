import requests
import json
from time import strftime, localtime

# Example signiture: 57oMGi1qoHynV6a9cXgyNuHaVTgLCPny5eEi255m793FyTAiZQs2R4B7QdWrgr6CCeo2G6eGxpFUqiEDYJ5NAK3E
signiture = input("What is the transaction signiture? ")

url = f'https://api.solana.fm/v0/transfers/{signiture}'

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)

data = json.loads(response.text)
try:
    for entry in data["result"]["data"]:
        if entry["instructionIndex"] == 5 and entry["innerInstructionIndex"] == 1:
            amounts = round(int(entry["amount"]) * 1e-6, 6) # Convert to actual amount of currency
            timestamps = round(int(entry["timestamp"]) * 1e3) #Convert to epoch time with milliseconds\
        if entry["instructionIndex"] == -1 and entry["innerInstructionIndex"] == -1:
            gasFee = round(int(entry["amount"]) * 1e-9, 9)
        if entry["instructionIndex"] == 8 and entry["innerInstructionIndex"] == -1:
            prioFee = round(int(entry["amount"]) * 1e-9, 9)
        if entry["instructionIndex"] == 5 and entry["innerInstructionIndex"] == 0:
            solPurchase = round(int(entry["amount"]) * 1e-9, 9)
    time = strftime('%Y-%m-%d %H:%M:%S', localtime(timestamps*1e-3))

    # Convert timestamps to start and end
    url = f'https://api.binance.com/api/v3/klines?symbol=SOLUSDC&interval=1s&startTime={timestamps}&endTime={timestamps+999}'

    payload = {}
    headers = {
    'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
        
    solPrice = float(json.loads(response.text)[0][1])

    totalFees = round(gasFee + prioFee, 9)
    solAmount = (solPurchase - totalFees)
    moneySpent = round((solPurchase * solPrice), 2)
    avgBuy = float((solPurchase * solPrice)/amounts)

    print("Timestamp of purchase:", time)
    print("Sol Price at purchase:", solPrice)
    print("Sol purchase amount:", solPurchase)
    print (f'Purchase Price: ${moneySpent}')
    print("Amount of tokens:", amounts)
    print("Fees:", totalFees)
    print("Average Buy Price: ", avgBuy)
except:
    print('Invalid transaction signiture')

