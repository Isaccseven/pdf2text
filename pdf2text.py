import os
import click_spinner
import pytesseract
from pdf2image import convert_from_path
import typer
from rich.console import Console
from gtts import gTTS

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


def speech(input_path_: str, output_path: str, language: str):
    lang = language
    if os.path.exists(output_path):
        os.remove(output_path)
        print("Successfully! The File has been removed")
    else:
        file = open(input_path_, 'r')
        mytext = file.read().replace("\n", " ")
        myobj = gTTS(text=mytext, lang=lang, slow=False, )
        myobj.save(output_path)


@app.command(short_help='extract text from pdf, first argument input path, second output path')
def extract(input_path: str, output_path: str):
    console.print("[bold green]extract text from pdf...[/bold green]")
    with click_spinner.spinner():
        ocr_core(input_path, output_path)
    console.print("[bold green]finished...[/bold green]")


@app.command(short_help='convert your generated text file to a mp3 file')
def generate(input_path_: str, output_path: str, language: str):
    console.print("[bold green]converting text to mp3...[/bold green]")
    with click_spinner.spinner():
        speech(input_path_, output_path, language)
    console.print("[bold green]finished...[/bold green]")


if __name__ == '__main__':
    app()
