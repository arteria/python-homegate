import ftplib
import tempfile
import datetime
import os
import codecs
from __init__ import __version__


FTP_HOST = 'ftp.homegate.ch'
DATA_DIR = '/data'
IMAGES_DIR = '/images' 
MOVIES_DIR = '/movies'
DOC_DIR = '/doc'


class Homegate(object):
    ''' 
    This implements the IDX3.01 API for Homegate. 
    The full documentation can be found here: https://github.com/arteria/python-homegate/
    '''
    _images = ["picture_"+str(x+1)+"_filename" for x in range(13)]
            
    def __init__(self, agancyID, host=FTP_HOST, username=None, password=None):
        ''' 
        Establish connection to Homegate's FTP server.
        '''
        print host, username, password
        self.agancyID = agancyID
        self.session = ftplib.FTP(host, username, password)
        
        
    def push(self, idxRecords):
        ''' 
        Transfer (push, upload) this record(s) and it's file to Homegate.
        autoUpdate: set 
        '''
        idx_f = tempfile.NamedTemporaryFile(delete=False)
        idx_filename = idx_f.name
        idx_f.close()
        with codecs.open(idx_filename, 'w+b', encoding="ISO-8859-1") as idx_f:
            last_modified = datetime.datetime.now().strftime("%d.%m.%Y")
        
            if not isinstance(idxRecords, list):
                idxRecords = [idxRecords, ]
        
            for idxRecord in idxRecords:
                if self.agancyID != '' and self.agancyID is not None:
                    idxRecord.update({'agency_id': self.agancyID}) 
                idxRecord.update({'last_modified': last_modified})
        
                for field in idxRecord.fields:
                    if field[0] in self._images and field[1] != '':
                        # upload images
                        f = open(field[1], 'rb')
                        fname = idxRecord.prefix + os.path.basename(field[1])
                        self.session.cwd("/{agancyID}{directory}/".format(agancyID=self.agancyID, directory=IMAGES_DIR))
                        self.session.storbinary('STOR {fname}'.format(fname=fname), f) 
                        f.close()
                        # Modify field - set filename.ext instead of full path after uploading.
                        idxRecord.update({field[0]: fname})
        
                    elif field[0] == 'movie_filename' and field[1] != '':
                        # upload movies
                        f = open(field[1], 'rb')
                        fname = idxRecord.prefix + os.path.basename(field[1])
                        self.session.cwd("/{agancyID}{directory}/".format(agancyID=self.agancyID, directory=MOVIES_DIR))
                        self.session.storbinary('STOR {fname}'.format(fname=fname), f) 
                        f.close()
                        # Modify field - set filename.ext instead of full path after uploading.
                        idxRecord.update({field[0]: fname})
                
                    # upload docs
                    elif field[0] == 'document_filename' and field[1] != '':
                        # upload movies
                        f = open(field[1], 'rb')
                        fname = idxRecord.prefix + os.path.basename(field[1])
                        self.session.cwd("/{agancyID}{directory}/".format(agancyID=self.agancyID, directory=DOC_DIR))
                        self.session.storbinary('STOR {fname}'.format(fname=fname), f) 
                        f.close()
                        # Modify field - set filename.ext instead of full path after uploading.
                        idxRecord.update({field[0]: fname})
                    
                # append to idx file
                for field in idxRecord.fields:
                    idx_f.write(field[1])                
                    idx_f.write("#")         
                idx_f.write("\n\r")
                idx_f.flush()
        
            # upload idx file
            idx_f.close()
            idx_f = open(idx_filename, 'rb')
            self.session.cwd("/{agancyID}{directory}/".format(agancyID=self.agancyID, directory=DATA_DIR))
            self.session.storbinary('STOR unload.txt', idx_f) 
            os.unlink(idx_filename)
            return True
        return False
        
    def __del__(self):
        ''' 
        Clean up and close. 
        '''
        self.session.quit()    
        print "good bye"
    
class IdxRecord(object):
    def __init__(self, prefix=''):
        self.prefix = prefix
        self.fields = [
                ['version', 'IDX3.01'],
                ['sender_id', 'python-homegate-'+__version__],
                ['object_category', ''],
                ['object_type', ''],
                ['offer_type', ''],
                ['ref_property', ''],
                ['ref_house', ''],
                ['ref_object', ''],
                ['object_street', ''],
                ['object_zip', ''],
                ['object_city', ''],
                ['object_state', ''],
                ['object_country', ''],
                ['region', ''],
                ['object_situation', ''],
                ['available_from', ''],
                ['object_title', ''],
                ['object_description', ''],
                ['selling_price', ''],
                ['rent_net', ''],
                ['rent_extra', ''],
                ['price_unit', ''],
                ['currency', ''],
                ['gross_premium', ''],
                ['floor', ''],
                ['number_of_rooms', ''],
                ['number_of_apartments', ''],
                ['surface_living', ''],
                ['surface_property', ''],
                ['surface_usable', ''],
                ['volume', ''],
                ['year_built', ''],
                ['prop_view', ''],
                ['prop_fireplace', ''],
                ['prop_cabletv', ''],
                ['prop_elevator', ''],
                ['prop_child-friendly', ''],
                ['prop_parking', ''],
                ['prop_garage', ''],
                ['prop_balcony', ''],
                ['prop_roof_floor', ''],
                ['distance_public_transport', ''],
                ['distance_shop', ''],
                ['distance_kindergarten', ''],
                ['distance_school1', ''],
                ['distance_school2', ''],
                ['picture_1_filename', ''],
                ['picture_2_filename', ''],
                ['picture_3_filename', ''],
                ['picture_4_filename', ''],
                ['picture_5_filename', ''],
                ['picture_1_title', ''],
                ['picture_2_title', ''],
                ['picture_3_title', ''],
                ['picture_4_title', ''],
                ['picture_5_title', ''],
                ['picture_1_description', ''],
                ['picture_2_description', ''],
                ['picture_3_description', ''],
                ['picture_4_description', ''],
                ['picture_5_description', ''],
                ['movie_filename', ''],
                ['movie_title', ''],
                ['movie_description', ''],
                ['document_filename', ''],
                ['document_title', ''],
                ['document_description', ''],
                ['url', ''],
                ['agency_id', ''],
                ['agency_name', ''],
                ['agency_name_2', ''],
                ['agency_reference', ''],
                ['agency_street', ''],
                ['agency_zip', ''],
                ['agency_city', ''],
                ['agency_country', ''],
                ['agency_phone', ''],
                ['agency_mobile', ''],
                ['agency_fax', ''],
                ['agency_email', ''],
                ['agency_logo', ''],
                ['visit_name', ''],
                ['visit_phone', ''],
                ['visit_email', ''],
                ['visit_remark', ''],
                ['publish_until', ''],
                ['destination', ''],
                ['picture_6_filename', ''],
                ['picture_7_filename', ''],
                ['picture_8_filename', ''],
                ['picture_9_filename', ''],
                ['picture_6_title', ''],
                ['picture_7_title', ''],
                ['picture_8_title', ''],
                ['picture_9_title', ''],
                ['picture_6_description', ''],
                ['picture_7_description', ''],
                ['picture_8_description', ''],
                ['picture_9_description', ''],
                ['picture_1_url', ''],
                ['picture_2_url', ''],
                ['picture_3_url', ''],
                ['picture_4_url', ''],
                ['picture_5_url', ''],
                ['picture_6_url', ''],
                ['picture_7_url', ''],
                ['picture_8_url', ''],
                ['picture_9_url', ''],
                ['distance_motorway', ''],
                ['ceiling_height', ''],
                ['hall_height', ''],
                ['maximal_floor_loading', ''],
                ['carrying_capacity_crane', ''],
                ['carrying_capacity_elevator', ''],
                ['isdn', ''],
                ['wheelchair_accessible', ''],
                ['animal_allowed', ''],
                ['ramp', ''],
                ['lifting_platform', ''],
                ['railway_terminal', ''],
                ['restrooms', ''],
                ['water_supply', ''],
                ['sewage_supply', ''],
                ['power_supply', ''],
                ['gas_supply', ''],
                ['municipal_info', ''],
                ['own_object_url', ''],
                ['billing_anrede', ''],
                ['billing_first_name', ''],
                ['billing_name', ''],
                ['billing_company', ''],
                ['billing_street', ''],
                ['billing_post_box', ''],
                ['billing_zip', ''],
                ['billing_place_name', ''],
                ['billing_land', ''],
                ['billing_phone_1', ''],
                ['billing_phone_2', ''],
                ['billing_mobile', ''],
                ['billing_language', ''],
                ['publishing_id', ''],
                ['delivery_id', ''],
                ['picture_10_filename', ''],
                ['picture_11_filename', ''],
                ['picture_12_filename', ''],
                ['picture_13_filename', ''],
                ['picture_10_title', ''],
                ['picture_11_title', ''],
                ['picture_12_title', ''],
                ['picture_13_title', ''],
                ['picture_10_description', ''],
                ['picture_11_description', ''],
                ['picture_12_description', ''],
                ['picture_13_description', ''],
                ['picture_10_url', ''],
                ['picture_11_url', ''],
                ['picture_12_url', ''],
                ['picture_13_url', ''],
                ['commission_sharing', ''],
                ['commission_own', ''],
                ['commission_partner', ''],
                ['agency_logo_2', ''],
                ['number_of_floors', ''],
                ['year_renovated', ''],
                ['flat_sharing_community', ''],
                ['corner_house', ''],
                ['middle_house', ''],
                ['building_land_connected', ''],
                ['gardenhouse', ''],
                ['raised_ground_floor', ''],
                ['new_building', ''],
                ['old_building', ''],
                ['under_building_laws', ''],
                ['under_roof', ''],
                ['swimmingpool', ''],
                ['minergie_general', ''],
                ['minergie_certified', ''],
                ['last_modified', ''],
                ['advertisement_id', ''],
                ['sparefield_1', ''],
                ['sparefield_2', ''],
                ['sparefield_3', ''],
                ['sparefield_4', ''],
        ]
    
    def update(self, obj):
        '''
        The argument 'obj' should be dictionary containing the new values to overwrites 'self._fields' partially.
        
        Example: Set city to 'Basel' and country to Switzerland, the result '(2, 0)' says that two fields were 
        updated successfully and no errors. 
            
            >>> rec.update({'object_city':'Basel', 'object_country':'CH'}) 
            (2, 0)
            >>>
            
        '''
        updates, errors = 0, 0
        for o in obj:
            found  = False
            for field in self.fields: 
                if o == field[0]:
                    field[1] = obj[o] 
                    updates += 1
                    found = True
                    break
            if not found:
                errors += 1 # not found 
        return updates, errors
        