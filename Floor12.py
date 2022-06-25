import json
from os import chdir, path
chdir(path.dirname(path.realpath(__file__)))

# Initiate Variables
MainMenu = MM = ['Process', 'Rules', 'Exit']

Types = T = ['Information', 'Denunciation', 'Complaint', 'Request', 'Exit']

Ministries = M = ['Culture and Sports', 'Order',
                  'Patriotism', 'Social Care', 'Science and Technology', 'Labor', 'Exit']

RuleTypes = RT = ['Appeal', 'Person', 'Form', 'Exit']
# -- Appeal
AppealStamps = AS = ['Approve', 'Reject', 'Task Force', 'Classify', 'Check']


def load_rules(name, rules):
    try:
        with open(f'{name}_{rules}.json', 'r') as pkl:
            return json.load(pkl)
    except FileNotFoundError:
        return {}
    except Exception as e:
        print(f"ERROR: {e}")


AppealRules = load_rules('Appeal', 'Rules')
AppealAllRules = load_rules('Appeal', 'AllRules')

# -- Person
PersonStamps = PS = ['Arrest Warrant',
                     'Firing Squad', 'Note in Personal File', 'Reward', 'Community Service']


PersonRules = load_rules('Person', 'Rules')
PersonAllRules = load_rules('Person', 'AllRules')

# -- Form
FormStamps = FS = ['Archive',
                   'Enact', 'Clarify', 'Destroy']


FormRules = load_rules('Form', 'Rules')
FormAllRules = load_rules('Form', 'AllRules')


# Get Inputs
def get_input(what_to_choose, l):
    inp = False
    out = False
    while not out:
        try:
            inp = int(input('{}\nChoose Your {}: '.format('\n'.join(
                [f'{n} - {i}' for (n, i) in enumerate(l)]), what_to_choose)))
            out = l[inp]
            print('\n')
        except Exception:
            print('WRONG INPUT!\n')

    return out


def main_menu():
    menuInp = True
    while menuInp != False:
        menuInp = get_input('Action', MainMenu)
        print(menuInp)
        if menuInp == MM[0]:
            process()
        elif menuInp == MM[1]:
            print_rules()
        elif menuInp == MM[2]:
            menuInp = False


def process():
    InputType = get_input('Appeal Type', Types)
    InputMinistry = get_input('Ministry', Ministries)

    # Print Outputs
    def get_output(allrules, rules, out_type):
        out = allrules.get(InputType, allrules.get(
            InputMinistry, rules.get(InputMinistry, {}).get(InputType, 'ANY')))

        print('{} Process: {}'.format(out_type, out))

    # -- Appeal Process
    get_output(AppealAllRules, AppealRules, 'Appeal')

    # -- Person Process
    get_output(PersonAllRules, PersonRules, 'Person')

    # -- Form Process
    get_output(FormAllRules, FormRules, 'Form')

    print('\n')


def print_rules():
    global AppealAllRules, AppealRules, PersonAllRules, PersonRules, FormAllRules, FormRules

    def print_rule(d):
        for (key, value) in d.items():
            print(f'--- {key}:')
            for (a, b) in value.items():
                print(f'    {a} => {b}')
            print('\n')

    def print_all_rule(d):
        for (key, value) in d.items():
            print(f'    {key} => {value}')

    def print_everything(allrules, rules):
        print(f'___ All Rules for {rt} ___')
        print_all_rule(allrules)
        print('\n')
        print(f'___ Rules for {rt} ___')
        print_rule(rules)

    def add_rule(typeStamps, typeRules, typeName, typeAllRules):
        done = False
        while not done:
            InputMinistry = get_input('Ministry', Ministries + ['ANY'])
            if InputMinistry == Ministries[-1]:
                done = True
                break
            InputType = get_input('Appeal Type', Types + ['ANY'])
            InputStamp = get_input('Stamp', typeStamps)
            if InputMinistry == 'ANY' or InputType == 'ANY':
                if InputMinistry == 'ANY':
                    typeAllRules[InputType] = InputStamp
                else:
                    typeAllRules[InputMinistry] = InputStamp

                with open(f'{typeName}_AllRules.json', 'w') as pkl:
                    json.dump(typeAllRules, pkl, indent=4)

            else:
                if not typeRules.get(InputMinistry, False):
                    typeRules[InputMinistry] = {}

                typeRules[InputMinistry][InputType] = InputStamp
                with open(f'{typeName}_Rules.json', 'w') as pkl:
                    json.dump(typeRules, pkl, indent=4)

    rule_menu = ['Delete All', 'Add', 'Exit']
    rt = False
    while rt != RT[-1]:
        rt = get_input('Rule Type', RuleTypes)
        if rt == RT[0]:
            print_everything(AppealAllRules, AppealRules)

            rt_menu_inp = get_input('Action', rule_menu)
            if rt_menu_inp == rule_menu[0]:
                AppealAllRules = {}
                AppealRules = {}
            elif rt_menu_inp == rule_menu[1]:
                add_rule(AppealStamps, AppealRules, 'Appeal', AppealAllRules)

        elif rt == RT[1]:
            print_everything(PersonAllRules, PersonRules)
            rt_menu_inp = get_input('Action', rule_menu)
            if rt_menu_inp == rule_menu[0]:
                PersonAllRules = {}
                PersonRules = {}
            elif rt_menu_inp == rule_menu[1]:
                add_rule(PersonStamps, PersonRules, 'Person', PersonAllRules)

        elif rt == RT[2]:
            print_everything(FormAllRules, FormRules)
            rt_menu_inp = get_input('Action', rule_menu)
            if rt_menu_inp == rule_menu[0]:
                FormAllRules = {}
                FormRules = {}
            elif rt_menu_inp == rule_menu[1]:
                add_rule(FormStamps, FormRules, 'Form', FormAllRules)

    # main_menu()


# Run
main_menu()
