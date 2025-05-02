#!/bin/bash
# curl_random.sh
# Randomly send either a valid or an invalid POST request to /api/check

for i in {1..20}; do
  # Generate a random number: either 0 or 1.
  if [ $(( RANDOM % 2 )) -eq 0 ]; then
    echo "$(date): Sending valid request"
    # Valid request: includes the required "musthave" key in JSON.
    curl -s -X POST -H "Content-Type: application/json" \
         -d '{ "customerName" : "ACME", "dateOfTransaction" : "04/17/2025", "amount": 30000 }' \
         http://$1/api/check -v
    echo ""  # Optional: adds a newline for clarity.
  else
    echo "$(date): Sending invalid request"
    # Invalid request: missing the "musthave" key.
    curl -s -X POST -H "Content-Type: application/json" \
         -d '{ "customerName" : "ACME", "dateOfTransaction" : "04/17/2025", "amount": 20000 }' \
         http://$1/api/check -v
    echo ""
  fi
done
