from flask import Flask, render_template, request, redirect, url_for, send_file,send_from_directory
import markdown
import os
import zipfile




app = Flask(__name__)

files = []


@app.route('/')
def home():
    return redirect(url_for('upload'))
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        filename = f.filename
        file_content = f.read()
        processed_content = process_markdown(file_content)

        # Save processed file on server
        save_file(filename, processed_content)

        # Save filename to the list for later access
        files.append(filename)

        return redirect(url_for('view_files'))
    return render_template('upload.html')

@app.route('/view_files')
def view_files():
    # Show all files on server
    return render_template('view_files.html', files=list(set(files)))

@app.route('/download_all_files')
def download_all_files():
    # return "21312"
    # Download all files from server
    zip_filename = 'processed_files.zip'
    create_zip(zip_filename,files)
    # return send_file(zip_filename, as_attachment=True)
    return send_from_directory("", zip_filename, as_attachment=True)
@app.route('/download/<filename>')
def download_file(filename):
    # 从服务器上下载文件
    return send_from_directory("processed_files", filename, as_attachment=True)

def process_markdown(file_content):
    # process markdown content here
    processed_content = markdown.markdown(file_content)
    return processed_content

def save_file(filename, content):
    # Save the file on server
    file_path = os.path.join('processed_files', filename)
    content = content.encode('utf-8')
    with open(file_path, 'wb') as f:
        f.write(content)

# def zipdir(path, zipname):
#     """
#     将指定路径下的所有文件和文件夹打包为zip文件
#     :param path: 要打包的文件夹路径
#     :param zipname: 打包后的zip文件名
#     """
#     with zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED) as zipf:
#         for root, dirs, files in os.walk(path):
#             for file in files:
#                 zipf.write(os.path.join(root, file))
def create_zip(zip_filename,files):
    # Create a zip file of all processed files
    file_paths = [os.path.join('processed_files', f) for f in files]
    with zipfile.ZipFile(zip_filename, 'w',zipfile.ZIP_DEFLATED) as zf:
        for f in file_paths:
            zf.write(f)
app.run(debug=False)