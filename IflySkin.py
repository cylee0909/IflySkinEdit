import sublime, sublime_plugin, os, re

adapter_map = {
				"AREA_SET":"AREA",
		   		"KEY_SET" :"KEY",
		   		"LAYOUT_SET" :"LAYOUT"
		   }

class SkinEditCommand(sublime_plugin.TextCommand):
	def file_exist(self,path):
		return os.path.exists(path)
	def run(self, edit):
		_v = self.view
		win = self.view.window()
		folder = os.path.dirname(_v.file_name())
		line_region = _v.line(_v.sel()[0])
		line_str = _v.substr(line_region)
		file_handle_data =  line_str.split("=")
		if (len(file_handle_data) < 2):
			sublime.status_message("line not has an '=', please check it!")
			return
		file_name_sel = file_handle_data[0]
		if file_name_sel in adapter_map :
			file_name_sel = adapter_map[file_name_sel]
		file_name = file_name_sel.lower() + ".ini"
		file_path = os.path.join(folder,file_name)
		if (self.file_exist(file_path)):
			sublime.status_message("File -> "+file_path+" exist, opening...")
			_nv = win.open_file(file_path, sublime.ENCODED_POSITION)
			def loading_file():
				if _nv.is_loading():
					sublime.status_message("loading...")
					sublime.set_timeout(loading_file, 100)
				else :
					handle_new_file()
			def handle_new_file():
				sublime.status_message("")
				key_data = file_handle_data[1]
				key_regions = []
				if key_data.find(',') == -1 :
					key = '\['+key_data+'\]'
					key_region = _nv.find(key,0)
					if key_region != None:
						key_regions.append(key_region)
				else:
					keys = key_data.split(',')
					for k in keys:
						sk = '\['+k+'\]'
						sk_r = _nv.find(sk,0)
						if sk_r != None:
							key_regions.append(sk_r)
				# sel = _nv.sel()
				# sel.clear()
				# for r in key_regions:
				# 	sel.add(r)
				draw = sublime.DRAW_EMPTY
				_nv.add_regions(file_path, key_regions, "string", "", sublime.DRAW_OUTLINED)
				self.view.run_command("expand_selection", {"to": "brackets"})
				if (len(key_regions) > 0):
					_nv.show_at_center(key_regions[0])
			loading_file()
		else:
			sublime.status_message("File -> "+file_path+" not exist, please check it!")
