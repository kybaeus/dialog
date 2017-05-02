from functional import seq

# Constants

special_words = [
  '^', '$',            # start/end markers
  'INIT', 'WAIT',      # action types not in data
  'NO_OUTPUT',         # filler when copy or match word is not available
  'NO_USER_ACTION',    # initial value of lastUserAction
  'NO_WORKSPACE_WORD'
]


# Data Objects

class Workspace():
    def __init__(self, tree):
        # assert tree is array
        self.tree = tree

    def add(address, content):
        assert isinstance(address, (str))
        assert isinstance(content, (str))

        def _add(tree):
            if not isinstance(tree, (list)):
                return tree
            elif tree[0] == address:
                return tree.concat([[content]])
            else:
                return map(tree, _add)

        return Workspace(_add(self.tree))

    def update(self, action):
        if action.what == 'INIT':
            return Workspace(['root'])
        elif action.what == 'MSG':
            return self
        elif action.what == 'ADD':
            tmp = action.content.split(' ')
            assert (len(tmp) == 2)
            address = tmp[0]
            address = tmp[1]
            return this.add(address, content)

    # TODO: Figure out how to flattenDeep
    def to_words():
        return "NOT IMPLEMENTED YET"
    def to_tree():
        return this.tree


class Action():
    def __init__(self, who, what, content=False):
        self.who = who
        self.what = what
        self.content = content

    def to_words(self):
        return [f"{self.who}:", self.what] + (self.content.split(' ') if self.content else [])

    def to_string(self):
        if self.content:
            return f'{self.who}: {self.what} {self.content}'
        else:
            return f'{self.who}: {self.what}'


# Data Generation Functions

# TODO: Refactor to not open file directly
def file_to_dialogs(filename):
    """
    Convert filename string to dialog

    Args:
        param: filename: Path to file (from data directory)
    """
    init_entry = {
        "workspace": Workspace([]),
        "action": Action(who='A', what='INIT')
    }

    dialog_list = []
    current_workspace = init_entry["workspace"]

    for dialog in open(filename).read().split('\n\n'):
        action_list = [init_entry]
        for action in dialog.split("\n"):
            action_list.append({"workspace": current_workspace,
                                "action": string_to_action(action)})
        dialog_list.append(action_list)

    return dialog_list


# TODO: Refactor to not open file directly
def file_to_words(filename):
    """
    Convert filename to a list of words

    Args:
        param: filename: Path to file (from data directory)
    """

    out = seq(filename)\
    .map(lambda filename: open(filename).read().split())\
        .flatten()\
        .distinct()\
        .sorted()\
        .to_list()

    return out


def string_to_action(s):
    """
    Convert string to action

    Params:
        param: s: string


    """
    i = s.index(" ")
    line = s[i+1:]
    j = line.index(" ")

    who = s[0]
    what = line[0:j]
    content = line[j+1:]

    return Action(who, what, content)


def load_babl_data(training_file, dev_file):
    """
    Load local version of bAbl dataset


    Args:
        param: data_path: Path of data directory
        param: training_file: Path of training file (in data directory)
        param: dev_file: Path of dev file (in data directory)
    """

    types_and_tokens = [
            { "type": 'cuisine', "tokens": ['french', 'italian', 'british', 'spanish', 'indian'] },
            { "type": 'location', "tokens": ['rome', 'london', 'bombay', 'paris', 'madrid'] },
            { "type": 'price', "tokens": ['cheap', 'moderate', 'expensive'] },
            { "type": 'people', "tokens": ['two', 'four', 'six', 'eight'] },
        ]

    data = {
      "training": file_to_dialogs(training_file),
      "dev": file_to_dialogs(dev_file),
      "words": file_to_words(training_file) + special_words,
      "types_and_tokens": types_and_tokens
    }

    return data
