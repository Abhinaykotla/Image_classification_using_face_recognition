import face_recognition
import cv2

from tkinter import *
from tkinter import filedialog, ttk
from ttkthemes import ThemedTk as tk


from os import listdir


dirName_base = 'select folder'
dirName_output = None
fileName = None
image_count = 0


def open_file():
    file = filedialog.askopenfilename(filetypes=[("Image Files", ("*.jpeg", "*png", "*.jpg", "*.jfif", "*.tiff", "*.bmp",
                                                                  "*.webp", "*.JPEG", "*.PNG", "*.JPG", "*.JFIF", "*.TIFF", "*.BMP", "*.WEBP"))])
    if file != None:
        global fileName
        fileName = file


def open_dir_base():
    dir = filedialog.askdirectory()
    if dir != None:
        global dirName_base
        dirName_base = dir

        # Show base folder path on tkinter window
        file_explorer_base_show = Label(root, text='Chosen path: ' + dirName_base, width=100, height=1, anchor='w', fg="red", bg='black', font=('Helvetica', 12, 'italic'))
        file_explorer_base_show.place(x=90, y=100)

        # total image count in base folder
        global image_count
        image_count = len([name for name in listdir(dirName_base) if name.endswith(
            '.jpg' or '.png' or '.jpeg' or '.JPG' or '.PNG' or '.JPEG' or '.jfif' or '.JFIF' or '.tiff' or '.TIFF' or '.bmp' or '.BMP' or '.webp' or '.WEBP')])
        # create progress bar


def open_dir_output():
    dir = filedialog.askdirectory()
    if dir != None:
        global dirName_output
        dirName_output = dir

        file_explorer_output_show = Label(root, text='Chosen path: ' + dirName_output, width=100, height=1, anchor='w', fg="red", bg='black', font=('Helvetica', 12, 'italic'))
        file_explorer_output_show.place(x=90, y=200)


def start():
    if dirName_base == 'select folder' or dirName_output == None or fileName == None:
        print('Please select all the files')
    else:
        global progress_bar
        progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=image_count, mode='determinate', length=980)
        print(image_count)
        create_copy(fileName, dirName_base, dirName_output)


def create_copy(base_img_path, folder_selected, output_foulder):
    print('Starting')
    print('base_img: ' + base_img_path)
    print('folder_selected: ' + folder_selected)
    print('output_foulder: ' + output_foulder)

    # pack progress bar after start clicked
    progress_bar.place(x=10, y=400)

    base_img = face_recognition.load_image_file(base_img_path)

    img_encoding_base = face_recognition.face_encodings(base_img)[0]

    progress_count = 0

    for image in listdir(folder_selected):

        if (image.endswith('.jpg' or '.png' or '.jpeg' or '.JPG' or '.PNG' or '.JPEG' or '.jfif' or '.JFIF' or '.tiff' or '.TIFF' or '.bmp' or '.BMP' or '.webp' or '.WEBP')):
            print(image)

            img = face_recognition.load_image_file(folder_selected + '/' + image)

            # progress bar update variables
            progress_var.set(progress_count)
            progress_count += 1
            root.update_idletasks()

            # Get the face encodings for each face in each image file
            face_locations = face_recognition.face_locations(img)
            for i in range(0, len(face_locations)):

                img_encoding = face_recognition.face_encodings(img)[i]

                if face_recognition.compare_faces([img_encoding_base], img_encoding)[0]:
                    print('Match found')
                    # bgr to rgb
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    # Save image to target folder
                    cv2.imwrite(output_foulder + '/Copy_' + image, img)
                    break

                else:
                    print('No match found')
    progress_var.set(0)
    print('done')


root = tk(theme='arc')

root.geometry("1000x500")
root.title("Face Recognition")
#icon = cv2.imread('icon.ico')
#root.iconbitmap(icon)

# set background to black
root.configure(background='black')

progress_var = DoubleVar()
dirName_base_show = StringVar()

Text = Label(root, text="Photo segregation made easier ", width=60, height=1, font=("Helvetica", 20), fg="white", bg="black")
Text.place(x=0, y=0)

# Base folder select text
file_explorer_base = Label(root, text="Select base folder", width=15, height=2, anchor='w', fg="white", bg='black', font=('Helvetica', 12, 'bold'))
file_explorer_base.place(x=10, y=50)

# Base folder select button
Button(root, text="Choose path", command=open_dir_base).place(x=10, y=100)


# Output folder select text
file_explorer_output = Label(root, text="Select output folder",  width=15, height=2, anchor='w', fg="white", bg='black', font=('Helvetica', 12, 'bold'))
file_explorer_output.place(x=10, y=150)

# Output folder select button
Button(root, text="Choose path", command=open_dir_output).place(x=10, y=200)


# Target image select text
file_explorer_file = Label(root, text="Select Image with target face", width=23, height=2, anchor='w', fg="white", bg='black', font=('Helvetica', 12, 'bold'))
file_explorer_file.place(x=10, y=250)

# Target image select button
Button(root, text="Choose file", command=open_file).place(x=10, y=300)


# exit button
button_exit = Button(root, text="Exit", command=exit)
button_exit.pack(anchor=E, side=BOTTOM, padx=20, pady=20)

# start button
button_start = Button(root, text="Start", command=start, bg='white', fg='black', font=('Helvetica', 30, 'bold'))
Button(root, text="Start", command=start).place(x=10, y=350)

root.mainloop()