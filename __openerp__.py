# -*- encoding: utf-8 -*-
##############################################################################
#
#    Alexander Cuellar Morales

##############################################################################

{
    'name': 'Validador de Ruc',
    'version': '1.0',
    'category': 'Generic Modules/Base',
    'description': """
    Este addon valida el ruc de los clientes con la SUNAT

    Librerias necesarias:

    sudo apt-get install tesseract-ocr tesseract-ocr-eng python-imaging python-pip python-bs4 && sudo pip install pytesseract
    
 
    """,
    'author': 'Alexander Cuellar Morales alexcuellar@live.com',
    'depends': ['base_vat'],
    'website': '',
    'installable': True,
    'active': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: