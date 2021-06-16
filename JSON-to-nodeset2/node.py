class node:

    def __init__(self, code, id, name, definition, version, revision, superclass):
        self.code = code
        self.id = id
        self.name = name
        self.definition = definition
        self.version = version
        self.revision = revision
        self.superclass = superclass
        self.children = []


    def to_string(self):
        return 'code: ' + self.code + ', id: ' + self.id

    def addChild(self, node):
        self.children.append(node)