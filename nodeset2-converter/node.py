class Node:

    def __init__(self, code, id, name, definition, version, revision, superclass, dictionary_code):
        self.code = code
        self.id = id
        self.name = name
        self.definition = definition
        self.version = version
        self.revision = revision
        self.superclass = superclass
        self.children = []
        self.dictionary_code = dictionary_code


    def to_string(self):
        return 'code: ' + self.code + ', id: ' + self.id

    def addChild(self, node):
        self.children.append(node)

    def __getitem__(self, key):
        return getattr(self, key)