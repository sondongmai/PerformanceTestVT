# payload_generator.py

def generate_user_payload(i):
    return {"name": f"User{i}"}

# Dùng dict map tên 
PAYLOAD_FUNCTIONS = {
    "user": generate_user_payload,
   

}