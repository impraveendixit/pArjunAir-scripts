import tkinter as tk
from tkinter import *
import os
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import shutil
import os.path
from os.path import basename
import paramiko

def setup_connection(root, host, user, passwd, filename):

    ssh = paramiko.SSHClient()

    # This is to be remove where host are known 
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Do ssh connection
    try:
        ssh.connect(host, username=user, password=passwd)
    except:
        messagebox.showerror("Error", "Failed to connect..!!", parent = root)
        root.destroy()
        return

    # Open sftp
    try:
        sftp = ssh.open_sftp()
        remotepath = "/home/pkd/Projects/pArjunAir/" + filename
        sftp.put(filename, remotepath)
        messagebox.showinfo("Job submission", "Job submitted successfully", parent = root)
    except:
        messagebox.showerror("Copy error", "File cannot be sent..", parent = root)
        root.destroy()

    # close
    if sftp: sftp.close()
    if ssh: ssh.close()
    if root: root.destroy()

def submit_job(root, project_name):
    shutil.make_archive(project_name, 'zip', project_name)
    win = tk.Toplevel()
    win.wm_title("Submit job")

    zip_file = project_name + '.zip'

    host = tk.StringVar()
    user = tk.StringVar()
    passwd = tk.StringVar()

    host_label = tk.Label(win, text = 'Host Address: ')
    host_entry = tk.Entry(win, textvariable = host)

    user_label = tk.Label(win, text = 'Username: ')
    user_entry = tk.Entry(win, textvariable = user)

    passwd_label = tk.Label(win, text = 'Password: ')
    passwd_entry = tk.Entry(win, textvariable = passwd, show = '*')

    zip_label = tk.Label(win, text = "zip file: ")
    name_label = tk.Label(win, text = zip_file + " ✓")

    sub_btn = tk.Button(win, text = 'Submit',
            command = lambda: setup_connection(win, host.get(),
                user.get(), passwd.get(), zip_file))

    zip_label.grid(row = 0, column = 0, pady = 5)
    name_label.grid(row = 0, column = 1, pady = 5)
    host_label.grid(row = 1, column = 0, pady = 5)
    host_entry.grid(row = 1, column = 1, pady = 5)
    user_label.grid(row = 2, column = 0, pady = 5)
    user_entry.grid(row = 2, column = 1, pady = 5)
    passwd_label.grid(row = 3, column = 0, pady = 5)
    passwd_entry.grid(row = 3, column = 1, pady = 5)
    sub_btn.grid(row = 4, column = 0, padx = 15, pady = 5)

def upload_control_file(root, project_name, file_label):
    path = os.path.join("./", project_name)

    if not os.path.exists(path):
        os.mkdir(path)

    try:
        name = askopenfilename(parent = root, title = 'Choose .cfl file',
                filetypes=[("Control files", "*.cfl")])
    except SameFileError:
        res = messagebox.askquestion("askquestion", "Do you want to replace existing file?", parent = root)
        if res == 'no':
            return
    # copy the file
    shutil.copy2(name, path)
    file_label.set(basename(name) + " ✓")

def upload_inv_file(root, project_name, file_label):
    path = os.path.join("./", project_name)

    if not os.path.exists(path):
        os.mkdir(path)

    name = askopenfilename(parent = root, title = 'Choose .inv file',
            filetypes=[("Inversion files", "*.inv")])

    # copy the file
    shutil.copy2(name, path)
    file_label.set(basename(name) + " ✓")

def back_btn_callback(root, frame, prev_frame):
    frame.destroy()
    prev_frame.pack()
    root.title('Prepare and Submit job')

def forward_modelling(root, prev_frame):
    prev_frame.pack_forget()

    frame = Frame(root)
    root.title('Forward Modelling')

    project_name = tk.StringVar()
    file_name = tk.StringVar()

    project_name_label = tk.Label(frame, text = 'Project Name: ', font = ('calibre', 10, 'bold'))
    project_name_entry = tk.Entry(frame, textvariable = project_name, font = ('calibre', 10, 'normal'))

    upload_btn = tk.Button(frame, text = 'Upload .cfl file', width = 25,
            command = lambda: upload_control_file(frame, project_name.get(), file_name))
    name_label = tk.Label(frame, textvariable = file_name)

    submit_btn = tk.Button(frame, text = 'Submit Job', width = 25,
            command = lambda: submit_job(frame, project_name.get()))

    back_btn = tk.Button(frame, text = 'Back', width = 25,
            command = lambda: back_btn_callback(root, frame, prev_frame))

    project_name_label.grid(row = 0, column = 0, pady = 10)
    project_name_entry.grid(row = 0, column = 1, pady = 10)
    upload_btn.grid(row = 1, column = 0, pady = 10)
    name_label.grid(row = 1, column = 1, pady = 10)
    submit_btn.grid(row = 2, column = 0, pady = 10)
    back_btn.grid(row = 3, column = 0, pady = 10)
    frame.pack()

def inversion(root, prev_frame):
    prev_frame.pack_forget()

    frame = Frame(root)
    root.title('Inversion')

    project_name = tk.StringVar()
    cfl_file_name = tk.StringVar()
    inv_file_name = tk.StringVar()

    project_name_label = tk.Label(frame, text = 'Project Name: ', font = ('calibre', 10, 'bold'))
    project_name_entry = tk.Entry(frame, textvariable = project_name, font = ('calibre', 10, 'normal'))

    cfl_upload_btn = tk.Button(frame, text = 'Upload .cfl file', width = 25,
            command = lambda: upload_control_file(frame, project_name.get(), cfl_file_name))
    cfl_name_label = tk.Label(frame, textvariable = cfl_file_name)

    inv_upload_btn = tk.Button(frame, text = 'Upload .inv file', width = 25,
            command = lambda: upload_inv_file(frame, project_name.get(), inv_file_name))
    inv_name_label = tk.Label(frame, textvariable = inv_file_name)

    submit_btn = tk.Button(frame, text = 'Submit Job', width = 25,
            command = lambda: submit_job(frame, project_name.get()))

    back_btn = tk.Button(frame, text = 'Back', width = 25,
            command = lambda: back_btn_callback(root, frame, prev_frame))

    project_name_label.grid(row = 0, column = 0, pady = 10)
    project_name_entry.grid(row = 0, column = 1, pady = 10)
    cfl_upload_btn.grid(row = 1, column = 0, pady = 10)
    cfl_name_label.grid(row = 1, column = 1, pady = 10)
    inv_upload_btn.grid(row = 2, column = 0, pady = 10)
    inv_name_label.grid(row = 2, column = 1, pady = 10)
    submit_btn.grid(row = 3, column = 0, pady = 10)
    back_btn.grid(row = 4, column = 0, pady = 10)
    frame.pack()

def main():
    root = tk.Tk()
    root.geometry('640x480')
    root.title('Prepare and Submit job')

    frame = Frame(root)
    frame.pack(side = "top", expand = True, fill = "both")

    btn = tk.Button(frame, text = 'Forward Modelling', width = 25, command = lambda: forward_modelling(root, frame))
    btn.pack(side = TOP, pady = 30)
    btn = tk.Button(frame, text = 'Inversion', width = 25, command = lambda: inversion(root, frame))
    btn.pack(side = TOP, pady = 30)

    root.mainloop()


if __name__ == '__main__':
    main()
