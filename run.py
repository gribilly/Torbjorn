from torbjorn import app
import argparse

parser = argparse.ArgumentParser(description='Runs our WebApp.')
parser.add_argument('-debug',action="store_true")
args = parser.parse_args()

app.run(debug=args.debug)