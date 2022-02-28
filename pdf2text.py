import pytesseract
from pdf2image import convert_from_path
import typer
from rich.console import Console

console = Console()
app = typer.Typer()

def transform_images(input_path: str):
    import tempfile
    with tempfile.TemporaryDirectory():
        images_from_path = convert_from_path(input_path)
        return images_from_path

def ocr_core(input_path: str, output_path: str):
    images = transform_images(input_path)
    file = open(output_path, "w")
    for image in images:
        text = pytesseract.image_to_string(image)
        file.write(text)

@app.command(short_help='extract text from pdf, first argument input path, second output path')
def extract(input_path: str, output_path: str):
    console.print("[bold green]starting...[/bold green]")
    ocr_core(input_path, output_path)
    console.print("[bold green]finished...[/bold green]")

if __name__ == '__main__':
    app()
