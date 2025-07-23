storage = []

def log_request(operation, inputs, result):
    """Log the request details."""
    storage.append({
        "inputs": inputs,
        "result": result
    })

def get_logs():
    """Retrieve all logged requests."""
    return storage