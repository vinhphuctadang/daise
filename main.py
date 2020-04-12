from prompt_toolkit import prompt
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.completion import FuzzyWordCompleter
import os

WordCompleter = FuzzyWordCompleter
class Interpreter:
	'''
		Core system:
			- Underlying features 
			- Interactive Screen:
				+ Auto hint
	'''
	def getPromptString(self):
		return f'Daise {os.getcwd()}$ '

	def loadFilesIntoCompleter(self):
		root, dirs, files = next(os.walk('.'))
		self.prompt_completer = WordCompleter(dirs+files)
	def __init__(self):
		self.history = InMemoryHistory()
		self.commands = {}
		# Todo: add tab key for completion
		for func in dir(self):
			if func.startswith('cmd_'):
				self.history.append_string(func[4:])
				self.commands[func[4:]] = getattr(self, func)
	
	def cmd_exit(self, args):
		if len(args):
			status = args[0]
		else:
			status = 0
		os._exit(status)

	def cmd_cat(self, args):
		if not len(args):
			print('[ERROR] Must have input file')
		filename = args[0]
		try:
			f = open(filename, 'r')
		except Exception as e:  
			print('[ERROR]',e)
			return
		for _ in f.readlines():
			print(_,end='')
		print()
		f.close()
	def cmd_cd(self, args):
		target = '.'
		if len(args):
			target = args[0]
		try:
			os.chdir(target)
			self.loadFilesIntoCompleter()
		except: 
			print('[ERROR] Directory not exist')
		pass
	def executeCommand(self, cmd):
		cmd = cmd.strip()
		syntax  = cmd.split()
		if len(syntax):
			if syntax[0] in self.commands:
				self.commands[syntax[0]](syntax[1:])
			else:
				os.system(cmd)


	def run(self):
		self.loadFilesIntoCompleter()
		while True:
			try:
				text = prompt(self.getPromptString(), 
					history=self.history,
					auto_suggest=AutoSuggestFromHistory(),
					enable_history_search=True,
					completer=self.prompt_completer,
        			complete_while_typing=True,
				)
				self.executeCommand(text)
				self.history.append_string(text)
			except Exception as e:
				print('Exception')
			except KeyboardInterrupt:
				print('Keyboard interrupted')
				pass
def main():
	interpreter = Interpreter()
	interpreter.run()
if __name__ == "__main__":
	main()