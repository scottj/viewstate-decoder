#!/usr/bin/python3

from viewstate import ViewState
import argparse
import sys
import urllib.parse

# Handling of command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-vs", dest="encoded_vs", help="Base64 ViewState")
parser.add_argument(
    "-f",
    dest="infile",
    type=argparse.FileType("r"),
    help="Input File with Base64 ViewState",
)
parser.add_argument(
    "-o",
    dest="outfile",
    type=argparse.FileType("w"),
    default=sys.stdout,
    help="Name of the Output File with the Resulting ViewState",
)
args = parser.parse_args()

encoded_vs = ""

if not args.encoded_vs and not args.infile:
    print(
        "Usage: viewstate-decoder.py [-h] [-vs ENCODED_VS] [-f VS_FILENAME] [-o OUTPUT_FILENAME]"
    )
else:
    # Check if the input is given in the command line
    if args.encoded_vs:
        encoded_vs = args.encoded_vs
    else:  # If not, we have the input inside a file with name: args.infile
        encoded_vs = args.infile.read()
        args.infile.close()

        # Convert the URL encoded input into Base64 only (URL decode)
        encoded_vs = urllib.parse.unquote(encoded_vs)

    # Create ViewState object
    vs = ViewState(encoded_vs)
    decoded_vs = vs.decode()
    hmac = vs.mac
    sign = vs.signature

    # Write to output file
    args.outfile.write(
        "Decoded Viewstate: {}\n".format(str(decoded_vs))
    )  # We must set it as 'string' to write it because it's a tuple, not a string
    args.outfile.write("ViewState HMAC Signature Type: {}\n".format(hmac))
    if hasattr(sign, "hex"):
        args.outfile.write("ViewState HMAC Signature: {}\n".format(sign.hex()))
    if args.outfile.name != "<stdout>":
        print("Output file saved to: {}".format(args.outfile.name))
    args.outfile.close()
