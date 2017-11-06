import json
import os

class WafRules(object):
    def __init__(self,rules_path):
        super(WafRules,self).__init__()
        self._rules_path=rules_path
        self.get_path()

    def __can__(self):
        pass

    def get_path(self):
        if os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)),"rules")):
            self._rules_real_path=os.path.join(os.path.dirname(os.path.realpath(__file__)),"rules")
        else:
            self._rules_real_path=None
        
    def get_json_rules(self,json_name):
        json_path="{json_name}.json".format(json_name=json_name)
        if self._rules_real_path:
            if os.path.exists(os.path.join(self._rules_real_path,json_path)) and self.rules_status(self.load_json_data(os.path.join(self._rules_real_path,json_path))['status']):
                return self.get_actions_rules(self.load_json_data(os.path.join(self._rules_real_path,json_path))['actions'])
                
            else:
                return None

    def load_json_data(self,json_file):
        with open(json_file) as f:
            data = json.load(f,encoding='utf-8')
        return data

    def get_actions_rules(self,actions):
        return [action['pattern'] for action in actions]

    def rules_status(self,status):
        try:
            if status == 'on':
                return True
            elif status == 'off':
                return False
        except Exception,e:
            print e

    def __get__(self):
        pass

if __name__=='__main__':
    x=WafRules("rules")
    rules=x.get_json_rules("waf_2017_http_methods_forbidden")
    print rules.qsize()