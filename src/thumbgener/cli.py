import typer

from .ThumbgenerBlob import ThumbgenerBlob

app = typer.Typer()


@app.command()
def blob(
    title: str,
    filename: str,
    width: int = 800,
    height: int = 400,
    padding: int = 50,
    font_size: int = 50,
    line_padding: int = 10,
) -> None:
    """Создание обложки с каплями"""
    thumb = ThumbgenerBlob(
        width=width,
        height=height,
        padding=padding,
        font_size=font_size,
        line_padding=line_padding,
    )
    thumb.draw(title, filename)


def main():
    app()
