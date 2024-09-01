TEST_MESSAGE="Test Message"

RESPONSE=$(echo "$TEST_MESSAGE" | nc "server:12345")

if [ "$RESPONSE" = "$TEST_MESSAGE" ]; then
    echo "action: test_echo_server | result: success"
else
    echo "action: test_echo_server | result: fail"
fi