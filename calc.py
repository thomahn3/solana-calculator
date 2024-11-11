import requests
import json
from time import strftime, localtime

# Example signiture: 57oMGi1qoHynV6a9cXgyNuHaVTgLCPny5eEi255m793FyTAiZQs2R4B7QdWrgr6CCeo2G6eGxpFUqiEDYJ5NAK3E
signiture = input("What is the transaction signiture? ")
prioFee = 0

url = f'https://api.solana.fm/v0/transfers/{signiture}'

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)
#print(response)
data = json.loads(response.text)


for entry in data["result"]["data"]:
    if entry["instructionIndex"] == -1 and entry["innerInstructionIndex"] == -1:
        timestamps = round(int(entry["timestamp"]) * 1e3) #Convert to epoch time with milliseconds
        gasFee = round(int(entry["amount"]) * 1e-9, 9)
        time = strftime('%Y-%m-%d %H:%M:%S', localtime(timestamps*1e-3))
        print("Timestamp of purchase:", time)
        
        # Convert timestamps to start and end
        url = f'https://api.binance.com/api/v3/klines?symbol=SOLUSDC&interval=1s&startTime={timestamps}&endTime={timestamps+999}'
        payload = {}
        headers = {
        'Accept': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        solPrice = float(json.loads(response.text)[0][1])
        print("Sol Price at purchase:", solPrice)

    if entry["instructionIndex"] == 5 and entry["innerInstructionIndex"] == 1: #buy transaction (SOL to token)
        print("Buy Transaction")
        amounts = round(int(entry["amount"]) * 1e-6, 6) # Convert to actual amount of currency

        for entry in data["result"]["data"]:
            if entry["instructionIndex"] == 5 and entry["innerInstructionIndex"] == 0:
                solAmount = round(int(entry["amount"]) * 1e-9, 9)
                moneySpent = round((solAmount * solPrice), 2)  
                avgBuy = float((solAmount * solPrice)/amounts)

            if entry["instructionIndex"] == 8 and entry["innerInstructionIndex"] == -1:
                prioFee = round(int(entry["amount"]) * 1e-9, 9)

                print("Sol purchase amount:", solAmount)
                print (f'Purchase Price: ${moneySpent}')
                print("Average Buy Price: ", avgBuy)

    elif entry["instructionIndex"] == 4 and entry["innerInstructionIndex"] == 0: # Sell (Raydium) transaction (token to SOL)
        print("Sell Transaction")
        amounts = round(int(entry["amount"]) * 1e-6, 6)

        for entry in data["result"]["data"]:
            if entry["instructionIndex"] == 4 and entry["innerInstructionIndex"] == 1:
                solAmount = round(int(entry["amount"]) * 1e-9, 9)
                moneySold = round((solAmount * solPrice), 2)
                avgSell =  float((solAmount * solPrice)/amounts)

                print("Sol sold amount:", solAmount)
                print (f'Sell Price: ${moneySold}')
                print('Average Sell Price:', avgSell)

    elif entry["instructionIndex"] == 3 and entry["innerInstructionIndex"] == 1: # Sell Jupiter router
        amounts = round(int(entry["amount"]) * 1e-6, 6)

        for entry in data["result"]["data"]:
            if entry["instructionIndex"] == 3 and entry["innerInstructionIndex"] == 2:
                solAmount = round(int(entry["amount"]) * 1e-9, 9)
                moneySold = round((solAmount * solPrice), 2)
                avgSell =  float((solAmount * solPrice)/amounts)

                print("Sol sold amount:", solAmount)
                print (f'Sell Price: ${moneySold}')
                print('Average Sell Price:', avgSell)

            if entry["instructionIndex"] == 3 and entry["innerInstructionIndex"] == 4: 
                prioFee = round(int(entry["amount"]) * 1e-9, 9)
            
           

totalFees = round(gasFee + prioFee, 9)

print("Amount of tokens:", amounts)
print("Fees:", totalFees)

#print('Invalid transaction signiture')

# Add status code error handling
# Prioritization fee CU limtit * CUbudget*10^9