from __future__ import annotations

# -----------------------------
# SKINNY-128 Sbox (hard-coded)
# -----------------------------
S8 = [
    0x65,0x4c,0x6a,0x42,0x4b,0x63,0x43,0x6b,0x55,0x75,0x5a,0x7a,0x53,0x73,0x5b,0x7b,
    0x35,0x8c,0x3a,0x81,0x89,0x33,0x80,0x3b,0x95,0x25,0x98,0x2a,0x90,0x23,0x99,0x2b,
    0xe5,0xcc,0xe8,0xc1,0xc9,0xe0,0xc0,0xe9,0xd5,0xf5,0xd8,0xf8,0xd0,0xf0,0xd9,0xf9,
    0xa5,0x1c,0xa8,0x12,0x1b,0xa0,0x13,0xa9,0x05,0xb5,0x0a,0xb8,0x03,0xb0,0x0b,0xb9,
    0x32,0x88,0x3c,0x85,0x8d,0x34,0x84,0x3d,0x91,0x22,0x9c,0x2c,0x94,0x24,0x9d,0x2d,
    0x62,0x4a,0x6c,0x45,0x4d,0x64,0x44,0x6d,0x52,0x72,0x5c,0x7c,0x54,0x74,0x5d,0x7d,
    0xa1,0x1a,0xac,0x15,0x1d,0xa4,0x14,0xad,0x02,0xb1,0x0c,0xbc,0x04,0xb4,0x0d,0xbd,
    0xe1,0xc8,0xec,0xc5,0xcd,0xe4,0xc4,0xed,0xd1,0xf1,0xdc,0xfc,0xd4,0xf4,0xdd,0xfd,
    0x36,0x8e,0x38,0x82,0x8b,0x30,0x83,0x39,0x96,0x26,0x9a,0x28,0x93,0x20,0x9b,0x29,
    0x66,0x4e,0x68,0x41,0x49,0x60,0x40,0x69,0x56,0x76,0x58,0x78,0x50,0x70,0x59,0x79,
    0xa6,0x1e,0xaa,0x11,0x19,0xa3,0x10,0xab,0x06,0xb6,0x08,0xba,0x00,0xb3,0x09,0xbb,
    0xe6,0xce,0xea,0xc2,0xcb,0xe3,0xc3,0xeb,0xd6,0xf6,0xda,0xfa,0xd3,0xf3,0xdb,0xfb,
    0x31,0x8a,0x3e,0x86,0x8f,0x37,0x87,0x3f,0x92,0x21,0x9e,0x2e,0x97,0x27,0x9f,0x2f,
    0x61,0x48,0x6e,0x46,0x4f,0x67,0x47,0x6f,0x51,0x71,0x5e,0x7e,0x57,0x77,0x5f,0x7f,
    0xa2,0x18,0xae,0x16,0x1f,0xa7,0x17,0xaf,0x01,0xb2,0x0e,0xbe,0x07,0xb7,0x0f,0xbf,
    0xe2,0xca,0xee,0xc6,0xcf,0xe7,0xc7,0xef,0xd2,0xf2,0xde,0xfe,0xd7,0xf7,0xdf,0xff
]

# Rounds for SKINNY-128-128
ROUNDS = 40

# ShiftRows permutation (new[i] = old[P_SR[i]])
P_SR = [0, 1, 2, 3,
        7, 4, 5, 6,
        10, 11, 8, 9,
        13, 14, 15, 12]

# TK permutation PT (new[i] = old[PT[i]])
PT = [9, 15, 8, 13,
      10, 14, 12, 11,
      0, 1, 2, 3,
      4, 5, 6, 7]


def skinny_128_128_encrypt(pt: bytes, key: bytes) -> bytes:
    """
    SKINNY-128-128 encryption only:
      - 16-byte plaintext
      - 16-byte key (TK1 only)
    Returns 16-byte ciphertext.
    """
    if len(pt) != 16:
        raise ValueError("Plaintext must be 16 bytes.")
    if len(key) != 16:
        raise ValueError("Key must be 16 bytes (TK1 only for 128-128).")

    # state and tk1 are 16 nibbles/bytes laid out row-wise (m0..m15, tk0..tk15)
    state = list(pt)
    tk1 = list(key)

    # 6-bit LFSR round constant rc5..rc0 stored as integer bits [0..5]
    rc = 0
    states = [] 

    for rd in range(ROUNDS):
        tmp = [] 
        # ---- SubCells ----
        for i in range(16):
            state[i] = S8[state[i]]
        tmp.append(state.copy())
        # ---- AddConstants ----
        # update rc BEFORE use each round:
        # (rc5 rc4 rc3 rc2 rc1 rc0) <- (rc4 rc3 rc2 rc1 rc0 rc5^rc4^1)#permute it
        #[rc5,rc4rc3,rc2,rc1,rc0] = 
        #[rc4, rc3, rc2, rc1, rc0, rc5^rc4^1]
        rc0 = (rc >> 0) & 1
        rc1 = (rc >> 1) & 1
        rc2 = (rc >> 2) & 1
        rc3 = (rc >> 3) & 1
        rc4 = (rc >> 4) & 1
        rc5 = (rc >> 5) & 1
        n_rc0 = rc5 ^ rc4 ^ 1
        rc = ((n_rc0 << 0) | (rc0 << 1) | (rc1 << 2) | (rc2 << 3) | (rc3 << 4) | (rc4 << 5)) & 0x3F
        print(rd,bin(rc))
        # For s=8:
        # c0 = 0000 rc3 rc2 rc1 rc0
        # c1 = 000000 rc5 rc4
        c0 = (((rc >> 3) & 1) << 3) | (((rc >> 2) & 1) << 2) | (((rc >> 1) & 1) << 1) | ((rc >> 0) & 1)
        c1 = (((rc >> 5) & 1) << 1) | (((rc >> 4) & 1) << 0)
        c2 = 0x02

        # XOR into first column only: rows 0..2
        state[0]  ^= c0
        state[4]  ^= c1
        state[8]  ^= c2
        # state[12] ^= 0
        tmp.append(state.copy())

        # ---- AddRoundTweakey (z=1 => TK1 only; XOR first 2 rows) ----
        # first two rows = indices 0..7
        for i in range(8):
            state[i] ^= tk1[i]
        tmp.append(state.copy())
        # ---- ShiftRows (inline) ----
        old = state[:]  # 16 bytes
        state[0]  = old[P_SR[0]]
        state[1]  = old[P_SR[1]]
        state[2]  = old[P_SR[2]]
        state[3]  = old[P_SR[3]]
        state[4]  = old[P_SR[4]]
        state[5]  = old[P_SR[5]]
        state[6]  = old[P_SR[6]]
        state[7]  = old[P_SR[7]]
        state[8]  = old[P_SR[8]]
        state[9]  = old[P_SR[9]]
        state[10] = old[P_SR[10]]
        state[11] = old[P_SR[11]]
        state[12] = old[P_SR[12]]
        state[13] = old[P_SR[13]]
        state[14] = old[P_SR[14]]
        state[15] = old[P_SR[15]]
        tmp.append(state.copy())
        # ---- MixColumns (per column) ----
        # [a0,a1,a2,a3] -> [a0^a2^a3, a0, a1^a2, a0^a2]
        for c in range(4):
            a0 = state[0 + c]
            a1 = state[4 + c]
            a2 = state[8 + c]
            a3 = state[12 + c]
            state[0 + c]  = (a0 ^ a2 ^ a3) & 0xFF
            state[4 + c]  = a0 & 0xFF
            state[8 + c]  = (a1 ^ a2) & 0xFF
            state[12 + c] = (a0 ^ a2) & 0xFF
        tmp.append(state.copy())
        # ---- Update TK1 for next round: TK1 <- Permute(TK1) (inline) ----
        oldtk = tk1[:]
        tk1[0]  = oldtk[PT[0]]
        tk1[1]  = oldtk[PT[1]]
        tk1[2]  = oldtk[PT[2]]
        tk1[3]  = oldtk[PT[3]]
        tk1[4]  = oldtk[PT[4]]
        tk1[5]  = oldtk[PT[5]]
        tk1[6]  = oldtk[PT[6]]
        tk1[7]  = oldtk[PT[7]]
        tk1[8]  = oldtk[PT[8]]
        tk1[9]  = oldtk[PT[9]]
        tk1[10] = oldtk[PT[10]]
        tk1[11] = oldtk[PT[11]]
        tk1[12] = oldtk[PT[12]]
        tk1[13] = oldtk[PT[13]]
        tk1[14] = oldtk[PT[14]]
        tk1[15] = oldtk[PT[15]]
        states.append(tmp)
    
    with open("output.txt", "w") as f:
        for rd in range(len(states)):
            f.write(f"ROUND: {rd}\n")
            for val in states[rd]:
                f.write(", ".join([hex(v) for v in val])+"\n")

    return bytes(state)


# -----------------------------
# Test vector from your screenshot
# -----------------------------
if __name__ == "__main__":
    pt = [0xf2, 0x0a, 0xdb, 0x0e, 0xb0, 0x8b, 0x64, 0x8a, 0x3b, 0x2e, 0xee, 0xd1, 0xf0, 0xad, 0xda, 0x14]
    key = [0x4f, 0x55, 0xcf, 0xb0, 0x52, 0x0c, 0xac, 0x52, 0xfd, 0x92, 0xc1, 0x5f, 0x37, 0x07, 0x3e, 0x93]
    ciphertext = [0x22, 0xff, 0x30, 0xd4, 0x98, 0xea, 0x62, 0xd7, 0xe4, 0x5b, 0x47, 0x6e, 0x33, 0x67, 0x5b, 0x74] 
    ct  = [hex(b) for b in skinny_128_128_encrypt(pt, key)]
    print("Ciphertext:", list(ct))
    print(all([ct[i]==hex(ciphertext[i]) for i in range(len(ct))]))
    # expected: 22ff30d498ea62d7e45b476e33675b74
