from taipy.gui import Html

html_page = Html("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>MatplotLib in HTML</title>
    </head>
    <body>
        <h1>Current Graph:</h1>
        <img src="plot.png" alt="graphy graph">
    </body>
    </html>
""")