import sys
import PyPDF2
import gtts
import docx2txt
from playsound import playsound

# --- Global Variables --- #
file_name = ""
file_format = ""
extract_text_page = []
user_lang = ""
available_lang = gtts.tts.tts_langs()
continue_analysis = True


# --- Function ---#
def read_pdf(filepath):
    try:
        file = open(filepath, 'rb')
        pdf_read = PyPDF2.PdfFileReader(file)
        for num in range(0, pdf_read.numPages):
            extract_text_page.append(pdf_read.getPage(num).extractText())
    except FileNotFoundError as e:
        print(f"File {filepath} not found!", file=sys.stderr)
        return


def read_txt(filepath):
    try:
        file = open(filepath, "r")
        extract_text_page.append(file.read())
    except FileNotFoundError as e:
        print(f"File {filepath} not found!", file=sys.stderr)


def read_docx(filepath):
    try:
        my_text = docx2txt.process(filepath)
        extract_text_page.append(my_text)
    except FileNotFoundError as e:
        print(f"File {filepath} not found!", file=sys.stderr)


def read_file(filepath):
    global file_name
    global file_format

    if len(filepath) > 0:
        # File name
        if "/" in filepath:

            file_name = filepath.rsplit('/', 1)[1]
        else:
            file_name = filepath.rsplit('/', 1)[0]
        # File format
        if "." in filepath:
            file_format = filepath.rsplit('.', 1)[1]
            # Check that the file is PDF/text format
            if file_format == "pdf":
                read_pdf(filepath)
            elif file_format == "txt":
                read_txt(filepath)
            elif file_format == "docx":
                read_docx(filepath)
            else:
                print("Please choose a PDF/TXT/DOCX file.")
                sys.exit()

        else:
            print("Please check that the file has file format separated by a '.'")
            sys.exit()
    else:
        print("No input was inserted.")
        sys.exit()


def check_lang(lang):
    if lang in available_lang.keys():
        return lang
    elif lang in list(available_lang.values()):
        key_lang = [k for k, v in available_lang.items() if v == lang]
        return key_lang
    else:
        print("Please choose one of the available languages.")
        return ""


# --- START --- #
# Get the text saved inside the list
file_path = input("Insert the file's path (PDF/TXT/DOCX): ")
read_file(file_path)

# Get the language
print("List of available languages")
for key, value in available_lang.items():
    print(key, ': ', value)
user_lang = input("Choose one language: ")

if check_lang(user_lang) != "":
    for num in range(0, len(extract_text_page)):
        tts = gtts.gTTS(extract_text_page[num])
        tts.save(f"{file_name}_page{num}.mp3")  # save the audio file
        listen_now = input("Do you want to listen it now? Yes/No")
        if listen_now in ["Yes", "yes", "y"]:
            playsound(f"{file_name}_page{num}.mp3")  # play the audio file
        else:
            print("Good-Bye :)!")
