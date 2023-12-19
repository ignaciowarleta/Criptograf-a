import hashlib
from ecdsa import SigningKey, VerifyingKey, SECP256k1

def verify_signature(A, B, C, R, S, y, h):
    try:
        print(f"Verifying signature for A={A}, B={B}, C={C}, R={R}, S={S}, y={y}, h={h}")
        vk = VerifyingKey.from_string(bytes.fromhex(C), curve=SECP256k1)
        vk.verify(bytes.fromhex(y), bytes.fromhex(h + R), hashfunc=hashlib.sha256)
        vk.verify(bytes.fromhex(y), bytes.fromhex(h + A), hashfunc=hashlib.sha256)
        return True
    except Exception as e:
        print(f"Error during signature verification: {e}")
        return False

def verify_deposit(A, B, C, R, S, y, y1, y2, d, IM):
    try:
        print(f"Verifying deposit for A={A}, B={B}, C={C}, R={R}, S={S}, y={y}, y1={y1}, y2={y2}, d={d}, IM={IM}")
        h = hashlib.sha256((A + B + C + R + S).encode()).hexdigest()
        if not verify_signature(A, B, C, R, S, y, h):
            print("Invalid Signature")
            return False

        h0 = hashlib.sha256((A + B + IM + d).encode()).hexdigest()
        if not (int(y1, 16) * 123 + int(y2, 16) * 456 == int(h0, 16) * 789 + 101112):  # Replace with actual parameters
            print("(5) equation verification failed")
            return False

        return True

    except Exception as e:
        print(f"Error during deposit verification: {e}")
        return False

# Example usage:
A = "1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b"  # User's parameter (64 characters)
B = "5e6f7d8a9b0c1d2e3f4a5b6c7d8e9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6"  # User's parameter (64 characters)
C = "9f8e7d6c5b4a3b2c1d0e1f2a3b4c5d6e7f8"  # User's parameter (32 characters)
R = "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0"  # User's parameter (64 characters)
S = "e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0"  # User's parameter (32 characters)
y = "123abc456def78901234567890abcdef1234567890abcdef1234567890abcdef"  # User's parameter (64 characters)
y1 = "789def0123456789012345678901234567890123456789012345678901234"  # User's parameter (64 characters)
y2 = "345xyz6789012345678901234567890123456789012345678901234567890123"  # User's parameter (64 characters)
d = "2023-01-01T12:00:00"  # User's parameter (date and time)
IM = "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0"  # Merchant's account number (64 characters)

if verify_deposit(A, B, C, R, S, y, y1, y2, d, IM):
    print("Deposit Accepted")
else:
    print("Deposit Rejected")
