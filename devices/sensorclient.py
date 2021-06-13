import tornado.web as tw
import webbrowser as wb
import os.path



if __name__ == "__main__":
	try:
		wb.open_new("file://" + os.path.abspath("sensorUI.html"))
	except wb.Error:
		raise ValueError(f"Main UI could not open.")