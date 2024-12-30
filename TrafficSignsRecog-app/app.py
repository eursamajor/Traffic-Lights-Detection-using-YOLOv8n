from flask import Flask, redirect, request, render_template, url_for
from ultralytics.engine.results import Results  # Menggunakan Results dari engine
from ultralytics import YOLO
import os
import cv2

app = Flask(__name__)

# Path untuk menyimpan file upload
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Path untuk menyimpan hasil video dan gambar
OUTPUT_FOLDER = 'static/results'
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Load YOLOv8 model
model = YOLO('last.pt')

def process_video(video_path, output_path):
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Run YOLO inference
        results = model(frame)

        # Tambahkan confidence score pada bounding box
        for box in results[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cls = int(box.cls)
            label = model.names[cls]
            conf = float(box.conf)
            text = f"{label} {conf:.2f}"
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        out.write(frame)
    
    cap.release()
    out.release()

def predict_image(img_path):
    # Melakukan inferensi pada gambar
    results = model(img_path)
    
    # Mendapatkan gambar dengan bounding box
    img_with_boxes = results[0].plot()
    
    # Path untuk menyimpan hasil gambar
    output_path = os.path.join(OUTPUT_FOLDER, os.path.basename(img_path))
    
    # Simpan gambar hasil
    cv2.imwrite(output_path, img_with_boxes)
    print(f"Hasil gambar disimpan di: {output_path}")
    
    return results

def predict_video(video_path):
    output_path = os.path.join(OUTPUT_FOLDER, 'output_video.mp4')
    process_video(video_path, output_path)  # Process video dan simpan
    return True  # Placeholder untuk video selesai diproses

@app.route("/", methods=['GET', 'POST'])
def main():
    return render_template('index.html')

@app.route("/deteksi", methods=['GET', 'POST'])
def deteksi():
    return render_template('deteksi.html', video_path=None)

@app.route('/submit', methods=['POST'])
def submit():
    img_file = request.files.get('file')
    if img_file:
        file_ext = img_file.filename.split('.')[-1].lower()
        if img_file and img_file.content_type.startswith('image'):
            img_path = os.path.join(UPLOAD_FOLDER, img_file.filename)
            img_file.save(img_path)
            results = predict_image(img_path)
            output_image = os.path.join(OUTPUT_FOLDER, os.path.basename(img_path))
            return render_template(
                'deteksi.html', 
                img_data=url_for('static', filename=f'results/{os.path.basename(output_image)}'),
                results=results
            )
        elif img_file and img_file.content_type.startswith('video'):
            video_path = os.path.join(UPLOAD_FOLDER, img_file.filename)
            img_file.save(video_path)
            results = predict_video(video_path)
            return render_template(
                'deteksi.html', 
                video_path=url_for('static', filename='results/output_video.mp4'),
                results=results
            )
        else:
            return redirect(url_for('deteksi'))
    return redirect(url_for('deteksi'))

if __name__ == '__main__':
    app.run(debug=True)
