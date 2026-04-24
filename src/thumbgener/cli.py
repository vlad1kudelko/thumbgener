import typer

from .ThumbgenerBlob import ThumbgenerBlob

app = typer.Typer()


@app.command()
def blob(title: str, filename: str) -> None:
    """Создание обложки с каплями"""
    thumb = ThumbgenerBlob()
    thumb.draw(title, filename)


def main():
    app()
