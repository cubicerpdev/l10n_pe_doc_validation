# coding= utf-8


from PIL import Image
import requests
import pytesseract
from bs4 import BeautifulSoup
import StringIO

import string
from openerp import tools, api
from openerp.osv import osv, fields
from openerp.tools.translate import _


class res_partner(osv.Model):
    _inherit = 'res.partner'
	
    @api.multi
    def vat_change(self, vat):

        if vat:
            if len(vat)>3:
            	vat_type=vat[0:3]
            	
                tdireccion=""
                tnombre=""
        	
                if vat_type and vat_type.upper() == 'PED':
                    #DNI
                    return True
                elif vat_type and vat_type.upper() == 'PER':
                    #verify RUC
                    factor = '5432765432'
                    sum = 0
                    dig_check = False
                    
                    if len(vat) != 14:
                        raise osv.except_osv(
                		    _('Error'),
                		    _(vat+"eL RUC incorrecto"))
                    vat = vat[3:14]
                    try:
                        int(vat)
                    except ValueError:
                        raise osv.except_osv(
                		    _('Error'),
                		    _(vat+"eL RUC debe contener solo numeros enteros"))
                                 
                    for f in range(0,10):
                        sum += int(factor[f]) * int(vat[f])
                        
                    subtraction = 11 - (sum % 11)
                    if subtraction == 10:
                        dig_check = 0
                    elif subtraction == 11:
                        dig_check = 1
                    else:
                        dig_check = subtraction
                    
                    if int(vat[10]) == dig_check:
                        s = requests.Session() 
                        
                        url = 'http://www.sunat.gob.pe/cl-ti-itmrconsruc/captcha?accion=image'
                        nombre_imagen = '/tmp/captcha.jpeg'
                        r = s.get(url, stream=True)
                        with open (nombre_imagen, 'wb') as f:
                            for chunk in r.iter_content():
                                f.write(chunk)
                        captcha_val=pytesseract.image_to_string(Image.open(nombre_imagen))
                        captcha_val=captcha_val.strip().upper()

                        if(captcha_val.isalpha()):

                            consuta = s.get("http://www.sunat.gob.pe/cl-ti-itmrconsruc/jcrS00Alias?accion=consPorRuc&razSoc=&nroRuc="+vat+"&nrodoc=&contexto=rrrrrrr&tQuery=on&search1="+vat+"&codigo="+captcha_val+"&tipdoc=1&search2=&coddpto=&codprov=&coddist=&search3=")
                            texto_error='Surgieron problemas al procesar la consulta'
                            texto_consulta=consuta.text
                            #busqueda_error=texto_consulta.find(texto_error)
                            
                            if texto_error in (texto_consulta):
                                raise osv.except_osv(
                                    _('Error'),
                                    _('Consulte nuevamente'))
                            else:
                                #consulta(ruc)
                                texto_consulta=StringIO.StringIO(texto_consulta).readlines()

                                temp=0;

                                for li in texto_consulta:
                                    if temp==1:
                                        soup = BeautifulSoup(li)
                                        tdireccion= soup.td.string
                                        #tdireccion=tdireccion.string

                                        break
                                
                                    if li.find("Domicilio Fiscal:") != -1:
                                        temp=1
                                #print texto_consulta
                                for li in texto_consulta:
                                    if li.find("desRuc") != -1:
                                        soup = BeautifulSoup(li)
                                        tnombre=soup.input['value']

                                        break 
                                #raise osv.except_osv(
                                #    _(tnombre),
                                #    _(tdireccion))
                            
                                return {
                                    'value': {'name': tnombre,'street': tdireccion}
                                }

                        else:
                            raise osv.except_osv(
                                _('Error'),
                                _('Ruc captcha no reconocido intente nuevamente'))
                    else:
                        raise osv.except_osv(
                            _('Error'),
                            _(vat+"El RUC ingresado no es correcto"))

                else:
                    return False
            else:
                return False
        return False


res_partner()
