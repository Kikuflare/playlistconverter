import tkinter
import random
from tkinter import ttk, Frame, messagebox, filedialog, StringVar
import os

class PlaylistConverter(object):
    def __init__(self):
        self.root = tkinter.Tk()
        self.style = ttk.Style()
        self.style.theme_use('vista')
        self.root.title("Playlist Converter")
        self.root.resizable(0,0)
        self.root.iconbitmap("icon.ico")

        self.root.geometry("400x100")

        self.filename = tkinter.Entry(self.root, width=60)
        self.filename.grid(row=0, column=0, columnspan=2, padx=18, pady=(12,7))
        
        self.browse = tkinter.Button(self.root, text="Browse", command=self.browse_files, padx=15)
        self.browse.grid(row=1, column=0)

        self.convert = tkinter.Button(self.root, text="Convert", command=self.convert, padx=15)
        self.convert.grid(row=1, column=1)

        self.status_text = StringVar()
        self.status_text.set("Ready.")
        self.status = tkinter.Label(self.root, textvariable=self.status_text)
        self.status.grid(row=2, column=0, columnspan=2, sticky=tkinter.W, padx=13, pady=5)

    def browse_files(self):
        filename = filedialog.askopenfilename()
        if filename != "":
            self.filename.delete(0,tkinter.END)
            self.filename.insert(0,filename)
            self.status_text.set("Ready.")

    def convert(self):
        old_name = os.path.basename(self.filename.get())
        if old_name == "":
            print("Invalid filename.")
            tkinter.messagebox.showinfo("Error","Invalid filename.")
            
        elif os.path.splitext(old_name)[1] != ".m3u8":
            self.status_text.set("Invalid filetype.")
        
        else:
            new_file_name = os.path.splitext(old_name)[0] + ".wpl"
            
            if (os.path.exists(new_file_name)):
                if (tkinter.messagebox.askyesno("Convert", "File already exists, replace?")):
                    self._convert(old_name)
            
            else:
                self._convert(old_name)

    def _convert(self, old_name):
        try:
            new_file_name = os.path.splitext(old_name)[0] + ".wpl"
            with open(self.filename.get(), 'r', encoding='utf-8-sig') as f:
                lines = f.readlines()
                
                with open(new_file_name, 'w', encoding='utf-8-sig') as new_file:
                    new_file.write('<?wpl version="1.0"?>\n')
                    new_file.write('<smil>\n')
                    new_file.write('\t<head>\n')
                    new_file.write('\t\t<meta name="Generator" content="Microsoft Windows Media Player -- 12.0.7601.18526"/>\n')
                    new_file.write('\t\t<meta name="ItemCount" content="' + str(len(lines)) +'"/>\n')
                    new_file.write('\t\t<author/>\n')
                    new_file.write('\t\t<title>' + os.path.splitext(old_name)[0] + '</title>\n')
                    new_file.write('\t</head>\n')
                    new_file.write('\t<body>\n')
                    new_file.write('\t\t<seq>\n')
        
                    for line in lines:
                        line = line.rstrip('\n')
                        line = line.replace("&", "&amp;")
                        line = line.replace("'", "&apos;")
            
                        new_file.write('\t\t\t<media src="' + line + '"/>\n')
            
                    new_file.write('\t\t</seq>\n')
                    new_file.write('\t</body>\n')
                    new_file.write('</smil>\n')
        
                new_file.closed
            
            f.closed
            self.status_text.set("Finished converting.")

        except:
            self.status_text.set("Error: File not found.")
            
if __name__ == '__main__':
    playlistconverter = PlaylistConverter()
    playlistconverter.root.mainloop()
