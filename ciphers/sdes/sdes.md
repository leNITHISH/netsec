# Simplified DES
[Input]     block(plaintext)   : 8bits
[Output]    block(ciphertext)  : 8bits

key size: 10bits
goes through 2 rounds. (actual DES undergoes 16)

generate round keys / sub keys

Left Half (4 bits)        Right Half (4 bits)
             |                        |
             |                   Expand (EP) -> 8 bits
             |                        |
             |                   XOR with Key (K1 or K2)
             |                        |
             |                  Split into 2 parts
             |                 /             \
             |           S-Box 0           S-Box 1
             |                 \             /
             |                  Combine (4 bits)
             |                        |
             |                   Permute (P4)
             |                        |
        XOR <-------------------------+
             |
        New Right Half
