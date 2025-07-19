import base64

# Steps of the software development lifecycle
steps = ["plan", "code", "test", "delivery", "deploy", "monitor"]

for step in steps:
    # Encode the string to bytes, then to Base64 bytes
    encoded = base64.b64encode(step.encode("utf-8"))
    # Print the result (will be in b'...' format)
    print(encoded)