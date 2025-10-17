import os
from pdf2image import convert_from_path
import pytesseract

# Optional: Set path to tesseract executable (Windows only)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Input/output directories
input_folder = 'hindi_pdfs'      # Folder containing your scanned Hindi PDFs
output_folder = 'ocr_outputs'    # Folder to save extracted .txt files

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Loop through all PDF files in the input folder
for filename in os.listdir(input_folder):
    if filename.lower().endswith('.pdf'):
        pdf_path = os.path.join(input_folder, filename)
        print(f"🔍 Processing: {filename}")

        try:
            # Convert PDF pages to images
            images = convert_from_path(pdf_path, dpi=300)
        except Exception as e:
            print(f"❌ Failed to convert {filename} to images: {e}")
            continue

        all_text = ""

        # Perform OCR on each image page
        for page_num, img in enumerate(images, start=1):
            print(f"🧠 OCR on page {page_num}")
            try:
                text = pytesseract.image_to_string(img, lang='hin')
                all_text += f"\n\n--- Page {page_num} ---\n\n{text}"
            except Exception as e:
                print(f"⚠️ Error on page {page_num}: {e}")

        # Write extracted text to .txt file
        output_file = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(all_text)

        print(f"✅ Done: {filename} → {output_file}\n")

print("🎉 All PDFs processed.")
