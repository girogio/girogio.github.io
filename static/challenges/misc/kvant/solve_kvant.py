def str2bin(s):
    return ''.join(bin(ord(i))[2:].zfill(8) for i in s)


def bin2str(a):
    return ''.join(chr(int(a[i:i+8], 2)) for i in range(0, len(a), 8))

def decrypt_1(enc_1):
    dec = ""
    for i in range(0, len(enc_1), 2):
        state = [int(x) for x in enc_1[i:i+2]]
        dec += str(bin(state.index(0))[2:])
    return dec

def decrypt_2(enc_2):
    dec = ""
    for i in range(0, len(enc_2), 4):
        state = [int(x) for x in enc_2[i:i+4]]
        state[1], state[3] = state[3], state[1]
        dec += str(bin(state.index(1))[2:].zfill(2))
    return dec

def decrypt_3(enc_3):
    dec = ""
    for i in range(0, len(enc_3), 8):
        state = [int(x) for x in enc_3[i:i+8]]
        state[3], state[7] = state[7], state[3]
        dec += str(bin(state.index(1))[2:].zfill(3))
    return dec

with open("enc.txt", "r") as f:
    flag = str2bin(f.read())

decrypted = bin2str(decrypt_1(decrypt_2(decrypt_3(flag))))

print(decrypted)