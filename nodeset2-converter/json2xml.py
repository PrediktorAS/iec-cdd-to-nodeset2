import sys
sys.path.append("./node")

import re
from xml.dom import minidom
from node import Node
import json
from datetime import datetime

node_list = []

#reads the JSON file and adds the nodes to the node_list
def read_json():
    f = open('nodes.json', 'r')
    data = json.load(f)
    for data_dict in data:
        n = Node(data_dict['code'], data_dict['id'], data_dict['name'], data_dict['definition'], data_dict['version'], data_dict['revision'], data_dict['superclass'], data_dict['library'])
        node_list.append(n)
    f.close()

#Loops through the node_list then each node adds themselves to the children fields of their parent
def create_tree():
    for node in node_list:
        if node.superclass is not None:
            for parent in node_list:
                if parent.code == node.superclass:
                    parent.addChild(node)
                    break

#This function is the main function for building and creating the xml file
def build_xml(folder_name):
    #Gets the first number in the folder name. This number is equal to the dictionary code
    dictionary_code = re.findall(r'\d+', folder_name)[0]
    #Some dictionaries have two numbers to identify the dictionary
    #This code gets both numbers, if the dictionary has two of them
    whole_dictionary_code = re.findall(r'\d+', folder_name)[0] + ('-' + re.findall(r'\d+', folder_name)[1] if len(re.findall(r'\d+', folder_name)) == 2 else '')
    #Creates the xml and UANodeSet tag
    root = minidom.Document()  
    ua_node_set = root.createElement('UANodeSet') 
    ua_node_set.setAttribute('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    ua_node_set.setAttribute('xmlns:uax', 'http://opcfoundation.org/UA/2008/02/Types.xsd')
    ua_node_set.setAttribute('xmlns', 'http://opcfoundation.org/UA/2011/03/UANodeSet.xsd')
    ua_node_set.setAttribute('xmlns:s1', 'http://opcfoundation.org/UA/Dictionary/IRDI/IEC' + whole_dictionary_code + '/Types.xsd')
    ua_node_set.setAttribute('xmlns:xsd', 'http://www.w3.org/2001/XMLSchema')
    root.appendChild(ua_node_set)
    
    #Helper functions for specific parts of the xml document
    build_xml_base(root, ua_node_set, whole_dictionary_code)
    build_xml_dictionary_folder(root, ua_node_set, folder_name)
    build_xml_ua_objects(root, ua_node_set, folder_name, dictionary_code)
    build_xml_ua_variables(root, ua_node_set, dictionary_code)
    print_xml(root, whole_dictionary_code)


#Builds the base of the xml document
def build_xml_base(root, ua_node_set, dictionary_code):
    namespace_uris = root.createElement('NamespaceUris')
    ua_node_set.appendChild(namespace_uris)

    uri = root.createElement('Uri')
    txt_uri = root.createTextNode('http://opcfoundation.org/UA/Dictionary/IRDI/IEC' + dictionary_code + '/')
    uri.appendChild(txt_uri)
    namespace_uris.appendChild(uri)

    models = root.createElement('Models')
    ua_node_set.appendChild(models)

    model = root.createElement('Model')
    model.setAttribute('ModelUri','http://opcfoundation.org/UA/Dictionary/IRDI/IEC' + dictionary_code + '/')
    model.setAttribute('PublicationDate', datetime.utcnow().isoformat() + 'Z')
    model.setAttribute('Version','1.0.0')
    models.appendChild(model)

    requiredModel = root.createElement('RequiredModel')
    requiredModel.setAttribute('ModelUri', 'http://opcfoundation.org/UA/')
    requiredModel.setAttribute('PublicationDate', '2019-09-09T00:00:00Z')
    requiredModel.setAttribute('Version', '1.04.3')
    model.appendChild(requiredModel)
    
    aliases = root.createElement('Aliases')
    ua_node_set.appendChild(aliases)

    #Used to genereate the alias xml-elements
    aliasesValues = {
        'Boolean':'i=1',
        'UInt64':'i=9',
        'Double':'i=11',
        'String':'i=12',
        'DateTime':'i=13',
        'QualifiedName':'i=20',
        'LocalizedText':'i=21',
        'Organizes':'i=35',
        'HasModellingRule':'i=37',
        'HasTypeDefinition':'i=40',
        'HasSubtype':'i=45',
        'HasProperty':'i=46',
        'HasComponent':'i=47',
        'IdType':'i=256',
        'NumericRange':'i=291',
        'Range':'i=884',
        'EUInformation':'i=887',
        'HasInterface':'i=17603'
    }
    for key in aliasesValues:
        alias = root.createElement('Alias')
        alias.setAttribute('Alias', key)
        txt_alias = root.createTextNode(aliasesValues[key])
        alias.appendChild(txt_alias)
        aliases.appendChild(alias)

#Creates the dictionary folder type
def build_xml_dictionary_folder(root, ua_node_set, folder_name):
    ua_folder = root.createElement('UAObject')
    ua_folder.setAttribute('ParentNodeId','i=17594')
    ua_folder.setAttribute('NodeId','ns=1;s=' + folder_name)
    ua_folder.setAttribute('BrowseName', '1:' + folder_name)
    ua_node_set.appendChild(ua_folder)

    displayname_folder = root.createElement('DisplayName')
    txt_displayname_folder = root.createTextNode(folder_name)
    displayname_folder.appendChild(txt_displayname_folder)
    ua_folder.appendChild(displayname_folder)

    #Creates a list with references that will be added in the add_references method
    references = {
        'i=17594': {
            'ReferenceType': 'HasComponent',
            'IsForward': 'false'
        },
        'i=17591': {
            'ReferenceType': 'HasTypeDefinition'
        }
    }
    add_references(root, ua_folder, references)


#Builds every UAObject from the node information
def build_xml_ua_objects(root, ua_node_set, folder_name, dictionary_code):
    for node in node_list:
        #Checks if the node belongs to the dictionary
        if node.dictionary_code == dictionary_code:
            ua_object = root.createElement('UAObject')
            #If the node do not have a parent, the dictionary folder will be set to its parent
            ua_object.setAttribute('ParentNodeId', 'ns=1;s=' + (folder_name if (node.superclass == None) else node.superclass))
            ua_object.setAttribute('NodeId', 'ns=1;s=' + node.code)
            ua_object.setAttribute('BrowseName', '1:' + node.code)
            ua_node_set.appendChild(ua_object)

            display_name = root.createElement('DisplayName')
            txt_display_name = root.createTextNode(node.name)
            display_name.appendChild(txt_display_name)
            ua_object.appendChild(display_name)

            description = root.createElement('Description')
            txt_description = root.createTextNode(node.definition)
            description.appendChild(txt_description)
            ua_object.appendChild(description)
            
            #Creates a list with references that will be added in the add_references method
            references = {
                'ns=1;s=' + (folder_name if node.superclass == None else node.superclass): {
                    'ReferenceType': 'HasComponent',
                    'IsForward': 'false'
                },
                'i=17598': {
                    'ReferenceType': 'HasTypeDefinition'
                },
                'i=11508': {
                    'ReferenceType': 'HasModellingRule'
                }
            }
            add_references(root, ua_object, references)


#Builds every UAVariable from the node information
#The UAVariables represents properties 
def build_xml_ua_variables(root, ua_node_set, dictionary_code):
    #Creates a list with the different variable types
    #The method will add one property for each variable type to each node
    for node in node_list:
        #Checks if the node belongs to the dictionary
        if node.dictionary_code == dictionary_code:
            variable_types = [
                'Version',
                'Revision'
            ]
            for variable_type in variable_types:
                ua_variable = root.createElement('UAVariable')
                ua_variable.setAttribute('DataType', 'String')
                ua_variable.setAttribute('ParentNodeId', 'ns=1;s=' + node.code)
                ua_variable.setAttribute('NodeId', 'ns=1;s=' + node.code + variable_type[:1])
                ua_variable.setAttribute('BrowseName', '1:' + variable_type)
                ua_variable.setAttribute('AccessLevel', '3')
                ua_variable.setAttribute('WriteMask', '0')
                ua_variable.setAttribute('ValueRank', '-2')
                ua_node_set.appendChild(ua_variable)

                display_name = root.createElement('DisplayName')
                txt_display_name = root.createTextNode(variable_type)
                display_name.appendChild(txt_display_name)
                ua_variable.appendChild(display_name)

                #Creates a list with references that will be added in the add_references method
                references = {
                    'ns=1;s=' + node.code: {
                        'ReferenceType': 'HasProperty',
                        'IsForward': 'false'
                    },
                    'i=68': {
                        'ReferenceType': 'HasTypeDefinition'
                    }
                }
                add_references(root, ua_variable,references)

                value = root.createElement('Value')
                ua_variable.appendChild(value)

                uax_string = root.createElement('uax:String')
                uax_string.setAttribute('xmlns:uax', 'http://opcfoundation.org/UA/2008/02/Types.xsd')
                txt_uax_string = root.createTextNode(node[variable_type.lower()])
                uax_string.appendChild(txt_uax_string)
                value.appendChild(uax_string)

def add_references(root, ua_element, references):
    references_element = root.createElement('References')
    ua_element.appendChild(references_element)

    #For loop for generating the reference xml-element
    #It is programmed after a set structure of the 'references' variable. It follows these rules:
    #The main key for each reference is corresponding to what is supposed to be within the text-field of the tag
    #The value of the key is a dictionary representing attributes connected to the reference xml-element
    #The key of the inner dictionary is the attribute-name and the value is the corresponding value
    for reference in references:
        reference_element = root.createElement('Reference')
        for attribute in references[reference]:
            reference_element.setAttribute(attribute,references[reference][attribute])
        txt_reference = root.createTextNode(reference)
        reference_element.appendChild(txt_reference)
        references_element.appendChild(reference_element)


#Function for printing the builded xml to file
def print_xml(root, dictionary_code):
    xml_str = root.toprettyxml(indent ='\t', encoding='utf-8')
    save_path_file = 'Dictionary IEC ' + dictionary_code + '.xml'
    with open(save_path_file, 'wb') as f:
        f.write(xml_str) 

def main():
    read_json()
    create_tree()
    #A list with all the folder names
    dictionaries = ['Electric/electronic components (IEC 61360-4)', 'Process automation (IEC 61987 series)', 'Low voltage switchgear (IEC 62683 series)']

    #Creates a xml-file for each folder
    for dictionary in dictionaries:
        build_xml(dictionary)

    print('Finished building xml-files')


if __name__ == '__main__':
    main()

