# inventoryAgent

## Backend:
Python, Flask, 
Pycharm(IDE),
Ngrok for deployment : https://dashboard.ngrok.com/get-started/setup/macos

## LLM: 
bigscience/bloom-560m

## Frontend:
JavaScript, HTML, CSS,
Apps Script(IDE), 
Excel Sheet

##AppScripts: https://script.google.com/u/0/home/projects/19ZU4o-r-VZ6wsSFzyCvXHR3CRn7afTIDz1Xa_MZxPxkbJC2BRdCo-5pK/settings

##Excel Sheet: https://docs.google.com/spreadsheets/d/1_s-YfxuuZlzUzMz75eN54HbdOJanN-BvCaKt0q7_f_Y/edit?gid=0#gid=0

##Set up Instructions
1. Clone the repo
2. cd inventoryAgent
3. python3 -m venv .venv
4. source .venv/bin/activate
5. pip install -r requirements.txt
6. flask run
7. Run this command to test the API:

curl -X POST -H "Content-Type: application/json" \
-d '{
  "businessType": "Electronics",
  "skuCount": 5,
  "attributes": ["Quantity", "Location"],
  "comments": "Track batch numbers and manufacturers for quality control."
}' \
http://127.0.0.1:5000/generate-inventory-template

###
8. To test the frontend too,  set up ngrok https://dashboard.ngrok.com/get-started/setup/macos
9. change const apiUrl line 13 to the url you get after connecting your local to ngrok("ngrokurl/generate-inventory-template")







