from rsa import RSA

mouse_data = [
    (10, 20, 1000),
    (15, 25, 1010),
    (18, 30, 1020),
]

# Test 1: seed er deterministisk
seed1 = RSA._generate_seed(mouse_data)
seed2 = RSA._generate_seed(mouse_data)

print("Seed 1:", seed1)
print("Seed 2:", seed2)
print("Same seed:", seed1 == seed2)