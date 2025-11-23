# import the chardet library
import chardet

# use the detect method to find the encoding
# 'rb' means read in the file as binary
with open("datasets/Ladesaeulenregister.csv", 'rb') as file:
    print(chardet.detect(file.read()))