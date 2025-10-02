"""
TEST VECTOR:

PLAIN TEXT VERSION  (pt_bitsize, key_bitsize)
plaintext = [0x32, 0x43, 0xf6, 0xa8, 0x88, 0x5a, 0x30, 0x8d, 0x31, 0x31, 0x98, 0xa2, 0xe0, 0x37, 0x07, 0x34] 
key = [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c] 
ciphertext = [0x39, 0x25, 0x84, 0x1d, 0x2, 0xdc, 0x9, 0xfb, 0xdc, 0x11, 0x85, 0x97, 0x19, 0x6a, 0xb, 0x32]

"""

import struct

"""
The t1 to t5 can be hard coded 

"""


class AES_ENCRYPTION: #for now it is assumed (128,128) configuration only 
    
    def __init__(self, key, plaintext):
        self.key = key 
        self.plaintext = plaintext
        self.rcon = [None, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]
        self.sbox = [0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
            0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
            0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
            0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
            0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
            0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
            0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
            0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
            0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
            0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
            0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
            0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
            0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
            0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
            0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
            0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16]
        self.generate_t_tables()
        self.ek_words = 0 
        self.nk = 0 
        if len(key)==16:#128
            self.ek_words = 44 
            self.nk = 4 
            self.rounds = 10
        elif len(key)==24:#192 
            self.ek_words = 52
            self.nk = 6 
            self.rounds = 12
        elif len(key)== 32:#256
            self.ek_words = 60
            self.nk = 8 
            self.rounds = 14

    def generate_t_tables(self):#this is fixed 
        """Generates the tables used for the AES lookup table method."""
        self.t1 = []
        self.t2 = []
        self.t3 = []
        self.t4 = []
        self.t5 = []
        for i in range(len(self.sbox)):
            word1 = [self.gmul(self.sbox[i], 2), self.sbox[i],
                    self.sbox[i],self.gmul(self.sbox[i], 3)]
            word2 = [self.gmul(self.sbox[i], 3),self.gmul(self.sbox[i], 2),
                    self.sbox[i], self.sbox[i]]
            word3 = [self.sbox[i],self.gmul(self.sbox[i], 3),
                   self.gmul(self.sbox[i], 2), self.sbox[i]]
            word4 = [self.sbox[i], self.sbox[i],
                   self.gmul(self.sbox[i], 3),self.gmul(self.sbox[i], 2)]
            word5 = [self.sbox[i]] * 4
            self.t1.append(struct.unpack('>I', bytes(word1))[0])
            self.t2.append(struct.unpack('>I', bytes(word2))[0])
            self.t3.append(struct.unpack('>I', bytes(word3))[0])
            self.t4.append(struct.unpack('>I', bytes(word4))[0])
            self.t5.append(struct.unpack('>I', bytes(word5))[0])
    
    def gmul(self,a, b):
        """Special AES function used for multiplication
        Args:
            a (int): Integer to multiply
            b (int): Integer to multiply

        Returns:
            int: The product of the values
        """
        p = 0
        for c in range(8):
            if b & 1:
                p ^= a
            a <<= 1
            if a & 0x100:
                a ^= 0x11b
            b >>= 1
        return p
    
    def subword(self, word):
        """AES SubWord Method.

        Args:
            word (list): Word to transform

        Returns:
            int: Transformed word
        """
        bs = struct.pack('>I', word)
        nw = []
        for b in bs:
            nw.append(self.sbox[b])
        nw = struct.unpack('>I', bytes(nw))[0]
        return nw

    def rotword(self, word):
        """AES RotateWord Method.

        Args:
            word (list): Word to transform

        Returns:
            int: Transformed word
        """
        bs = list(struct.pack('>I', word))
        bs.append(bs.pop(0))
        nw = struct.unpack('>I', bytes(bs))[0]
        return nw

    def expanded_keys(self):
        ek = []
        i = 0
        # Nk words, each 4 bytes
        while i < self.nk:
            b = bytes(self.key[i*4:(i*4)+4])  # always 4 bytes per word
            w = struct.unpack('>I', b)[0]
            ek.append(w)
            i += 1

        # expand until we have Nb*(Nr+1) words
        while i < self.ek_words:
            tmp = ek[i-1]
            if i % self.nk == 0:  # generalize Nk here
                rcon_val = struct.unpack(
                    '>I', bytes([self.rcon[i//self.nk], 0, 0, 0])
                )[0]
                tmp = self.subword(self.rotword(tmp)) ^ rcon_val
            elif self.nk > 6 and i % self.nk == 4:#special case for 256 bit key
                tmp = self.subword(tmp)

            nw = tmp ^ ek[i - self.nk]
            ek.append(nw)
            i += 1

        return ek
    
    def encrypt(self):
        """
        Lookup Table AES implementation.
        Args:
            pt (bytes): Plaintext to encrypt
        Returns:
            bytes: Encrypted Ciphertext
        """
        ct = []
        a = [0, 0, 0, 0]
        # t is a temporary array to avoid us changing array a while performing the algorithm
        t = [0, 0, 0, 0]
        self.ek = self.expanded_keys()
        a[0] = struct.unpack('>I', bytes(self.plaintext[0:4]) )[0] ^ self.ek[0]
        a[1] = struct.unpack('>I', bytes(self.plaintext[4:8]))[0] ^ self.ek[1]
        a[2] = struct.unpack('>I', bytes(self.plaintext[8:12]))[0] ^ self.ek[2]
        a[3] = struct.unpack('>I', bytes(self.plaintext[12:16]))[0] ^ self.ek[3]
        for round in range(1, self.rounds):
            """
            can further split in to byte level manipulation
            """
            t[0] = (self.t1[(a[0] >> 24) & 0xff] ^
                        self.t2[(a[1] >> 16) & 0xff] ^
                        self.t3[(a[2] >> 8) & 0xff] ^
                        self.t4[(a[3]) & 0xff] ^
                        self.ek[(round*4)])
            t[1] = (self.t1[(a[1] >> 24) & 0xff] ^
                        self.t2[(a[2] >> 16) & 0xff] ^
                        self.t3[(a[3] >> 8) & 0xff] ^
                        self.t4[(a[0]) & 0xff] ^
                        self.ek[(round*4)+1])
            t[2] = (self.t1[(a[2] >> 24) & 0xff] ^
                        self.t2[(a[3] >> 16) & 0xff] ^
                        self.t3[(a[0] >> 8) & 0xff] ^
                        self.t4[(a[1]) & 0xff] ^
                        self.ek[(round*4)+2])
            t[3] = (self.t1[(a[3] >> 24) & 0xff] ^
                        self.t2[(a[0] >> 16) & 0xff] ^
                        self.t3[(a[1] >> 8) & 0xff] ^
                        self.t4[a[2] & 0xff] ^
                        self.ek[(round*4)+3])
            a = t.copy()
        # Final round of encryption
        for i in range(4):
            ct.append(self.sbox[(a[i] >> 24) & 0xff] ^
                    ((self.ek[-4+i] >> 24) & 0xff))
            ct.append(self.sbox[(a[(i + 1) % 4] >> 16) & 0xff] ^
                    ((self.ek[-4+i] >> 16) & 0xff))
            ct.append(self.sbox[(a[(i + 2) % 4] >> 8) & 0xff] ^
                    ((self.ek[-4+i] >> 8) & 0xff))
            ct.append(self.sbox[(a[(i + 3) % 4]) & 0xff] ^
                    ((self.ek[-4+i]) & 0xff))
        return ct
    
plaintext = [0x32, 0x43, 0xf6, 0xa8, 0x88, 0x5a, 0x30, 0x8d, 0x31, 0x31, 0x98, 0xa2, 0xe0, 0x37, 0x07, 0x34] 
key = [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c] 
obj = AES_ENCRYPTION(key, plaintext)
ciphertext = [0x39, 0x25, 0x84, 0x1d, 0x2, 0xdc, 0x9, 0xfb, 0xdc, 0x11, 0x85, 0x97, 0x19, 0x6a, 0xb, 0x32]
print(obj.encrypt()==ciphertext)