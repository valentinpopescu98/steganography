from PIL import Image

# converts string to binary
def messageToBits(msg, encryptionFormat):
    chars = []
    for x in bytearray(msg, encryptionFormat):
        chars.append(format(x, 'b').zfill(8))
    return chars

# converts binary to string
def bitsToMessage(chars, decryptionFormat):
    return bytearray.decode(chars, decryptionFormat)

def encryptMessage(msg, image, encryptionFormat):
    lst = [list(x) for x in image.getdata()]

    chars = messageToBits(msg, encryptionFormat)
    print(chars)

    for pixel in range(0, len(chars) * 3):
        for channel in range(3):
            # pixel 3, channel blue (corresponding to bit 9) reached
            if (pixel % 3 == 2 and channel == 2):
                # if this is the last pixel to be encrypted,
                # set bit 9 to 1
                if (pixel == len(chars) * 3 - 1):
                    lst[pixel][channel] = 1
                # otherwise set it to 0
                else:
                    lst[pixel][channel] = 0
                # break because we do not want to overwrite the bit
                break

            # if the pixel is different to char's bit,
            # decrementing it will make both values even or odd
            if (lst[pixel][channel] % 2 != int(chars[int(pixel / 3)][pixel % 3 * 3 + channel])):
                # when the pixel has value = 0, it cannot be decremented to negative values
                if (lst[pixel][channel] == 0):
                    lst[pixel][channel] = 1
                    continue
                lst[pixel][channel] -= 1

    lst = [tuple(x) for x in lst]
    im_out = Image.new(image.mode, image.size)
    im_out.putdata(lst)
    return im_out


def decryptMessage(image, decryptionFormat):
    lst = [list(x) for x in image.getdata()]
    chars = bytearray()
    charsIndex = -1

    while(True):
        # add new binary value for new character;
        # set it to 0 and increment it if you need to
        chars.append(0)
        charsIndex += 1

        # create 3 new pixels for a char
        for pixel in range (3):
            for channel in range(3):
                # pixel 3, channel blue (corresponding to bit 9) reached
                if(pixel==2 and channel==2):
                    # search in the encrypted image list for the required
                    # 9th bit, based on the character to be decrypted;
                    # if it is equal to 1, stop
                    if(lst[charsIndex*3 + 2][2]%2 == 1):
                        msg = bitsToMessage(chars, decryptionFormat)
                        print(msg)
                        return
                    # break because we do not want to overwrite the bit
                    break

                # decrypting is easy, we need to get the modulo 2 value and multiply
                # it with each bits index to the power of 7 - current index;
                # we start from 7 because we read from MSB to LSB and we have 8 bits;
                # we have no 9th bit, so no 2 ^ (-1) because program breaks on last index
                chars[charsIndex] += (lst[charsIndex*3 + pixel][channel] % 2) * (2 ** (7-pixel*3-channel))

imageFormat = 'utf-16'
message = 'Steganography'

im = Image.open('butterfly.png')
im_out = encryptMessage(message, im, imageFormat)
im_out.save("butterfly_encrypted.png")

im_out = Image.open('butterfly_encrypted.png')
decryptMessage(im_out, imageFormat)