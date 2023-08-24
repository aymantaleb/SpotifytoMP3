import customtkinter
from PIL import Image

def button_callback():
    print("button pressed")


if __name__ == "__main__":
    app = customtkinter.CTk()

    app.title("my app")
    app.geometry("400x400")
    button_image = customtkinter.CTkImage(Image.open("AlbumArt/A.D.H.D.jpeg"), size=(160, 160))
    button = customtkinter.CTkButton(master = app, text="A.D.H.D \n By Kendrick Lamar", command=button_callback, image=button_image, compound="top")
    button.grid(row=0, column=0, padx=20, pady=20)
    app.mainloop()
