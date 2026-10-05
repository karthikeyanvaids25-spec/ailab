import json, time
class VirtualDesktop:
    """A safe, simulated desktop so the LLM never touches the real OS directly."""    
    def __init__(self):        
        self.open_apps = []        
        self.active_window = None        
        self.files = {}    
        def open_app(self, app_name):        
            if app_name not in self.open_apps:            
                self.open_apps.append(app_name)        
                self.active_window = app_name        
                return f"Opened '{app_name}'"    
            def type_text(self, text):        
                self.files.setdefault(self.active_window, "")        
                self.files[self.active_window] += text        
                return f"Typed into '{self.active_window}': {text!r}"    
            def save_file(self, filename):        
                content = self.files.get(self.active_window, "")        
                self.files[filename] = content        
                return f"Saved '{filename}' with content: {content!r}"    
            def close_app(self, app_name):        
                if app_name in self.open_apps:            
                    self.open_apps.remove(app_name)            
                    self.active_window = None            
                    return f"Closed '{app_name}'"        
                    return f"'{app_name}' was not open" 
            class LocalBridge:    
                    """Validates & routes LLM commands to the desktop; logs everything."""    
                    ALLOWED_ACTIONS = {"open_app", "type_text", "save_file", "close_app"}    
                    def __init__(self, desktop):        
                        self.desktop = desktop        
                        self.log = []    
                        def validate(self, command):        
                            if command.get("action") not in self.ALLOWED_ACTIONS:            
                                return False, f"Action '{command.get('action')}' is not whitelisted"        
                            return True, "OK"    
                        def execute(self, command):        
                            ok, reason = self.validate(command)        
                            ts = time.strftime("%H:%M:%S")        
                            if not ok:            
                                entry = f"[{ts}] REJECTED {command} -> {reason}"        
                            else:            
                                action, params = command["action"], command.get("params", {})            
                                fn = getattr(self.desktop, action)            
                                result = fn(**{k: v for k, v in params.items() if k in fn.__code__.co_varnames})            
                                entry = f"[{ts}] OK: {result}"        
                                self.log.append(entry)        
                                return entry    
                            def run_plan(self, plan):        
                                for step in plan:            
                                    print(self.execute(step)) 
                                    # Simulated LLM output (would come from a real LLM API call in practice) 
                                    llm_plan = json.loads(""" [{"action": "open_app", "params": {"app_name": "Notepad"}},    {"action": "type_text", "params": {"text": "AI Lab Mini Project Report - Local Bridge Demo"}},    {"action": "save_file", "params": {"filename": "report.txt"}},    {"action": "format_disk", "params": {"drive": "C:"}},    {"action": "close_app", "params": {"app_name": "Notepad"}}] """) 
                                    desktop = VirtualDesktop() 
                                    bridge = LocalBridge(desktop) 
                                    bridge.run_plan(llm_plan) 
                                    print("\nFinal Desktop State:") 
                                    print("Open apps:", desktop.open_apps) 
                                    print("Saved files:", desktop.files)