from lxml import etree as ET

def generate_response(status, status_message):
    """
    Generate a response in the format required by the API
    """
    response = ET.Element('response')
    code = ET.SubElement(response, 'code')
    code.text = status
    message = ET.SubElement(response, 'message')
    message.text = status_message
    return ET.tostring(response, pretty_print=True)
