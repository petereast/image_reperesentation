#Text to image thing
from image_tools import *
import time

def load_character_file(filename="characters.txt"):
    with open(filename) as charfile:
        chars_lines = charfile.readlines()
    current_char = ""
    total_chars = []
    alphabet = list("abcdefghijklmnopqrstuvwxyz0".upper())
    letters = dict()
    for line in chars_lines:
        if line != "\n":
            current_char += line
        else:
            total_chars.append(current_char)
            current_char = ''
    for letter, char in zip(alphabet,total_chars):
        letters.update({letter:char})
        print(letter, char)
    return letters

def get_line_in_string(string, line_id = 0):
    lines = string.rsplit("\n")
    return lines[line_id]

def combine_letters(word, letters): #word as a list or as a string
    word = list(word.upper())
    #Get Each line from each character and append it
    string_letters = []
    for char in word:
        #go though each line in each letter to do stuff
        if char != " ":
            string_letters.append(letters[char])
        else:
            string_letters.append(letters["0"])
        #now we've got an array of the binary reperesentations of the leters, it's time to go through each of them, line by line
    #All of the letters should be the same height.
    height = string_letters[0].count("\n")
    #go through the and join each line from each character
    output = ''
    for count in range(height):
        for letter in string_letters:
            output+=get_line_in_string(letter, count)+" "
        output+="\n"
    return output

def get_image_width(img):
    rawlen = len(img[:img.find("\n")])
    if rawlen % 2 == 0:
        return rawlen // 2
    else:
        return (rawlen //2)+1

def gen_image_format(img):
    height = img.count("\n")
    width = get_image_width(img)
    towrite = "P1\n{0} {1}\n".format(width, height)+img
    return towrite

def save_image(img):
    towrite = gen_image_format(img)
    #get filename
    print("Enter the filename, or press enter to use the date")
    filename = input(">>>")
    if filename == "":
        filename = time.asctime()

    if filename[-4] != "." and filename[:-4] != ".pbm":
        filename += ".pbm"
    with open(filename, "w") as output:
        output.write(towrite)
    print("File writing successful")
    
def main_program():
    #load the character definitions from a file
    letters = load_character_file()

    #get some text from the user

    print("Enter the text you want as an image - allowed characters: a-Z and space")
    
    word = input(">>>")
    
    img = combine_letters(word, letters)
    save_image(img)

main_program()
    
