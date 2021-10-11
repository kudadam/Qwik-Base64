"""
Qwik Base64 is an application which can convert files into Base64 format
"""

# Imported Modules
import click
import pybase64
from os import path


@click.group()
def app():
	pass

def get_file_contents(path):
	"""This function returns the contents of a file"""
	try:
		with open(path,"r") as file:
			return file.read()
	except UnicodeDecodeError:
		with open(path,"rb") as file:
			return file.read()

def write_to_file(path,contents,data_type):
	# This function writes data to a file
	# It takes the path, the contents to write and the type of the data [str or bytes]
	try:
		if data_type == bytes:
			with open(path,"wb") as file:
				file.write(contents)
		else:
			with open(path,"w") as file:
				file.write(contents)
	except:
		print("Error")

@click.option("-t","--text",help = "Takes the input as text", type=bool, default = False, show_default = True,is_flag = True)
@click.option("-o","--output",help = "Writes the output into the provided file path")
@click.argument("INPUT")
@app.command()
def encode(input,text,output):
	output_value = [] #This list will hold the processed data
	if text:
		output_value = [pybase64.b64encode(input.encode()).decode(),str]
	elif input:
		if not path.exists(input):
			click.echo("Error: File does not exist",err = True)
			exit()
		else:
			contents = get_file_contents(input)
			if type(contents) == bytes:
				output_value = [pybase64.b64encode(contents),bytes]
			else:
				output_value = [ pybase64.b64encode(contents.encode()).decode(), str]
	if not output:
		click.echo(output_value[0])
	else:
		write_to_file(output, output_value[0],output_value[1])



#==================================================


@click.option("-t","--text",help = "Takes the input as text", type=bool, default = False, show_default = True,is_flag = True)
@click.option("-o","--output",help = "Writes the output into the provided file path")
@click.argument("INPUT")
@app.command()
def decode(input,text,output):
	output_value = []
	if text:
		try:
			output_value = [pybase64.b64decode(input.encode()).decode(),str]
		except:
			click.echo("Error: Text is not base64")
			exit()
	elif input:
		if not path.exists(input):
			click.echo("Error: File does not exist",err = True)
			exit()
		else:
			try:
				contents = get_file_contents(input)
				if type(contents) == bytes:
					output_value = [pybase64.b64decode(contents),bytes]
				else:
					try:
						output_value = [pybase64.b64decode(contents.encode()).decode(),str]
					except:
						#This means that even though the contents was stored in string format
						#it's contents are actually binary data. So we need to convert it into binary
						output_value = [pybase64.b64decode(contents.encode()),bytes]
			except Exception as e:
				print(e)
				click.echo("Error: File is not base64")
	if not output:
		click.echo(output_value[0])
	else:
		write_to_file(output,output_value[0],output_value[1])




app.add_command(decode)
app.add_command(encode)

if __name__ == "__main__":
	app();