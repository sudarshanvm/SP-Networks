#!/bin/python3

import sbox
import pbox
import keygen
import tkinter as tk

encrypted_text = []
decrypted_text = []
key_list = []
primes = []
key = ''
stages = 5

def Encrypter(plain_text,key):
    def encrypt(plain_text, key, prime, stage):
        print("plain text = ", plain_text)
        e_text_1 = pbox.encrypt(plain_text, prime)
        e_text_2 = sbox.substitute_encrypt(e_text_1, key)
        return e_text_2

    output_text.delete('1.0', tk.END)           #clean the output section


    encrypted_text.append(plain_text)

    print("--- Encryption ---")
    for i in range(stages):
        encrypted_text.append(encrypt(encrypted_text[i], key_list[i+1], primes[i], i+1))
        print(f"encrypted stage {i+1} text = ", encrypted_text[i+1])

    print("\n========================================\n")

    #here we change the output label as Encrypted message
    message = encrypted_text[-1]
    label['text'] = 'Encrypted\nMessage'
    output_text.insert(1.0, message)

def Decrypter(key):
    def decrypt(plain_text, encrypted_text, key, prime, stage):
        d_text_2 = sbox.substitute_decrypt(encrypted_text, key)
        padding = pbox.padding(plain_text, prime)
        d_text_1 = pbox.decrypt(d_text_2, prime, padding)
        return d_text_1

    output_text.delete('1.0', tk.END)           #clean the output section

    decrypted_text.insert(0, encrypted_text[-1])
    print("--- Decryption ---")
    print("text to be decypted = ", decrypted_text[0])

    for i in range(stages, 0, -1):
        decrypted_text.insert(0, decrypt(encrypted_text[i-1], encrypted_text[i], key_list[i], primes[i-1], i))
        print(f"decrypted stage {i} text = ", decrypted_text[0])

    #here we change the output label as Encrypted message
    message = decrypted_text[0]
    label['text'] = 'Encrypted\nMessage'
    output_text.insert(1.0, message)

if __name__ == '__main__':

    key = keygen.generate_final_key()
    key_list.append(key[:100])
    key_list.append(key[100:])

    # stages = int(input("how many stages? > "))
    for i in range(stages):
        key_list.append(sbox.substitute_encrypt(key_list[i+1], key_list[1]))

    primes = keygen.list_primes(stages)
    key = key[:10]
    print("key = ", key)
    print("primes = ", primes)
    print("\n========================================\n")
    root = tk.Tk()              #create tkinter window

    #creating the tkinter widgets
    canvas = tk.Canvas(root, height=250, width=650)
    head_label = tk.Label(canvas, text='Message Encrypter', font=('verdana', 20))
    message_label = tk.Label(canvas, text='Message: ', font=('verdana', 15))

    # key_label = tk.Label(canvas, text='Key: ', font=('verdana', 15))

    message_entry = tk.Entry(canvas, width=40, font=('verdana', 15))
    key_entry = tk.Entry(canvas, width=40, font=('verdana', 15))
    output_label = tk.Label(canvas, text='OutPut ↓', font=('verdana', 15))
    label = tk.Label(canvas, text='Encrypted\nMessage', font=('verdana', 15))
    output_text = tk.Text(canvas, height=1, width=40, borderwidth=1, font=('verdana', 15))
    # key_text = tk.Text(canvas, height=1, width=40, borderwidth=1, font=('verdana', 15))
    encrypt_button = tk.Button(canvas, text='Encrypt', font=('verdana', 15), command=lambda: Encrypter(message_entry.get(), key))
    decrypt_button = tk.Button(canvas, text='Decrypt', font=('verdana', 15), command=lambda: Decrypter(key))
    #
    #
    #placing the widgetes
    canvas.pack()
    head_label.place(y=1, relx=0.35)
    message_label.place(x=3, y=50, anchor='w')
    # key_label.place(x=3, y=85, anchor='w')

    message_entry.place(x=120, y=40)
    # key_entry.place(x=120, y=75)

    output_label.place(y=115, relx=0.45)
    label.place(x=3, y=170, anchor='w')
    output_text.place(x=120, y=150)
    encrypt_button.place(x=350, y=200)
    decrypt_button.place(x=470, y=200)

    root.mainloop()
