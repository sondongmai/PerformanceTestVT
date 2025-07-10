# config.py

API_CONFIGS = [
    {
        "name": "Create User",
        "url": "http://127.0.0.1:5000/user",
        "method": "POST",
        "num_requests": 300000,
        "max_workers": 10000,
        "payload_func": "user"  # key trong PAYLOAD_FUNCTIONS
    },
    # {
    #     "name": "Get Users",
    #     "url": "http://127.0.0.1:5000/users",
    #     "method": "GET",
    #     "num_requests": 300000,
    #     "max_workers": 300,
    #     "payload_func": None  # GET không cần payload
    # }
]