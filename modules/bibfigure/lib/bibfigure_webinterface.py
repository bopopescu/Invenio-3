## This file is part of Invenio.
## Copyright (C) 2009, 2010, 2011 CERN.
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
from invenio.bibclassify_config import CFG_TMPDIR

# pylint: disable=C0103
"""Invenio BibEdit Administrator Interface."""

__revision__ = "$Id"

__lastupdated__ = """$Date: 2008/08/12 09:26:46 $"""

from invenio.jsonutils import json, json_unicode_to_utf8, CFG_JSON_AVAILABLE

from invenio.config import \
     CFG_SITE_LANG, \
     CFG_TMPSHAREDDIR, \
     CFG_TMPDIR
     
from invenio.messages import gettext_set_language
'''
from invenio.access_control_engine import acc_authorize_action
from invenio.bibedit_engine import perform_request_ajax, perform_request_init, \
    perform_request_newticket, perform_request_compare, \
    perform_request_init_template_interface, perform_request_ajax_template_interface
from invenio.bibedit_utils import user_can_edit_record_collection
from invenio.config import CFG_SITE_LANG, CFG_SITE_SECURE_URL, CFG_SITE_RECORD

from invenio.urlutils import redirect_to_url
'''
from invenio.webinterface_handler import WebInterfaceDirectory, wash_urlargd
from invenio.webpage import page
from invenio.webuser import getUid
from invenio.bibdocfile import BibRecDocs, BibDoc

from invenio.dbquery import run_sql
import poppler
import cStringIO
import gtk
import os
from invenio import webinterface_handler_config as apache

import bibfigure_captionextractor as ce
import bibfigure_similarity as simi
import bibfigure_config as config
import bibfigure_template as template
import tempfile
import logging
logger =  logging.getLogger("BibfigureLogger")
logger.setLevel(logging.DEBUG)
#logger.addHandler(logging.StreamHandler(sys.stderr))
logger.addHandler(logging.FileHandler("/home/pete/src/invenio/modules/bibfigure/testimg/log.log"))
   

class WebInterfacePageImages(WebInterfaceDirectory):
    """Defines the set of /edit pages."""

    _exports = ['']
    _JSON_DATA_KEY = 'jsondata'
    _title = ""
    
    def __init__(self, recid=None):
        """Initialize."""
        self.recid = recid 
        self.page_num = 0 # page_num to output as an image
        self.img_width = 800 # width to render the page_num to
        self.debug = ""

    def index(self, req, form):
        """Handle all requests and generate the output page
        """
        
        argd = wash_urlargd(form, { \
                    'approve' : (int, 0)})
        approveid = argd['approve']
        
        js_files = ['bibfig.windowifyer.js',
                'bibfig.selector.js',
                'bibfig.pageViewArea.js',
                'bibfig.pagesSelector.js',
                'bibfig.main.js',
                'bibfig.interface.js',
                'bibfig.imageView.js',
                'bibfig.handlers.js',
                'bibfig.graphicalOps.js',
                'bibfig.figuresSelector.js',
                'bibfig.figureControlsArea.js',
                'bibfig.data.js',
                'bibfig.buslogger.js',
                'jquery-ui.min.js',
                'addons/imgareaselect/jquery.imgareaselect.min.js']
        
        css_files = ['/css/bibfig.basicStyles.css',
                     '/css/bibfig.selecting.css',
                     '/js/addons/imgareaselect/imgareaselect-default.css',
                     '/img/jquery-ui/themes/base/jquery.ui.all.css']
         
        head_builder = cStringIO.StringIO()
        for css in css_files:
            head_builder.write('<link rel="stylesheet" href="'+css+'">\n')
            
        for js in js_files:
            head_builder.write('<script type="text/javascript" src="/js/' + js + '"></script>\n')
        
        
        head_builder.write('<script type = "text/javascript">\n \
                        var recid = '+str(self.recid)+';\n \
                        var approvalid = '+str(int(approveid))+';\n \
                        var pdfDocument = new PdfDocument();\n \
                        var eventsBus = new EventsBus();\n \
                        new BusLogger(eventsBus); \
                    </script>')    
        head = head_builder.getvalue()
        head_builder.close()
        
        p = page(metaheaderadd=head, title=self._title,
                    body=template.body,
                    #description=_("%s Personalize, Display searches") % CFG_SITE_NAME_INTL.get(argd['ln'], CFG_SITE_NAME),
                    #keywords=_("%s, personalize") % CFG_SITE_NAME_INTL.get(argd['ln'], CFG_SITE_NAME),
                    #uid=uid,
                    #language=argd['ln'],
                    req=req,
                    lastupdated=__lastupdated__,
                    #navmenuid='youralerts',
                    #secure_page_p=1
                    )
        return p
    
    def _create_image(self, req, form):
        """
        Generates an image of pdf page number self.page_num or
        returns an error page if the page cannot be processed
        """
        temp_path = CFG_TMPSHAREDDIR
        cache_file = "imgcache_r%d_p%d_res%d.png" % (self.recid, self.page_num, self.img_width)
        if(os.path.isfile(temp_path +"/"+ cache_file)):
            req.headers_out["content-type"] = "image/png"
            f = open(temp_path +"/"+ cache_file, "r")
            req.write(f.read())
            f.close()
        else:
            pdfdata = self._get_main_pdf_data()
            
            doc = poppler.document_new_from_data(pdfdata, password='')
            
            try:
                p = doc.get_page(self.page_num)

                pwidth, pheight = p.get_size()
                pwidth = int(pwidth)
                pheight = int(pheight)
                
                width = self.img_width
                height = int(self.img_width / float(pwidth) * pheight)
            
                pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, width, height)
                
            
                p.render_to_pixbuf(0, 0, width, height, self.img_width / float(pwidth), 0, pixbuf)
            
                # There has to be a better way to get the image?
                lst = []
                pixbuf.save_to_callback(lambda b, l: l.append(b), 'png', user_data=lst)
                #png = ''.join(lst)
                b = cStringIO.StringIO()
                for chunk in lst:
                    b.write(chunk)
                f = open(temp_path +"/"+ cache_file, "w")
                f.write(b.getvalue())
                f.close()
                req.headers_out["content-type"] = "image/png"
                req.write(b.getvalue())
                b.close()
            except:
                argd = wash_urlargd(form, { \
                    'ln': (str, CFG_SITE_LANG), \
                    'rev1' : (str, ''), \
                    'rev2' : (str, ''), \
                    'recid': (int, self.recid)})
    
                ln = argd['ln']
                _ = gettext_set_language(ln)
                uid = getUid(req)
                #_ = gettext_set_language(ln)
  
                req.status = apache.HTTP_NOT_FOUND
                return page(title=_("Error"),
                        body="Error while processing page %d, the page does not exist.  " % self.page_num,
                        #errors = ["test"],
                        #warnings = warnings,
                        #uid = uid,
                        language=ln,
                        #navtrail    = navtrail,
                        #lastupdated = __lastupdated__,
                        req=req)

    def _get_main_pdf_data(self):
        bRD = BibRecDocs(self.recid)
        
        for bdoc in bRD.list_bibdocs():
            for bfile in bdoc.list_latest_files():
                if(bfile.get_format() == ".pdf"):
                    return bfile.get_content()  
        return None
    
    def _meta_info(self, req, form):
        argd = wash_urlargd(form, { \
                    'approve' : (int, 0)})
        approvalid = argd['approve']
        
        
        json_response = {}
        pdfdata = self._get_main_pdf_data()
        
        if(pdfdata is None):
            json_response.update({'error': 'no pdf'})
            return json.dumps(json_response)
            
        doc = poppler.document_new_from_data(pdfdata, password='')
        
        page_resolution = {}
        for i in range(doc.get_n_pages()):
            p = doc.get_page(self.page_num)
            pwidth, pheight = p.get_size()
            page_resolution[i] = "%d, %d" % (pwidth, pheight)
            
        json_response.update({'pageResolution': page_resolution})
        json_response.update({'pages': doc.get_n_pages()})
        
        if(approvalid > 0):
            res = run_sql("SELECT recid, jsondata FROM  bibfigure_approvalrequests WHERE approvalid = '%s'", (approvalid, ))
            
            if(len(res) == 1):
                recid, jsondata = res[0]
                json_data_unicode = json.loads(jsondata)
                json_data = json_unicode_to_utf8(json_data_unicode)
                json_response.update(json_data)
                return json.dumps(json_response)
            else:
                json_response.update({'error': 'no approval'})
                return json.dumps(json_response)
            
        else:
            doc = self._get_bibdoc()
            
            links = doc.get_incoming_relations('is_extracted_from')

            count = 1
            for rel in links:
                figure = simi.Figure.from_moreinfo(rel.more_info)
                bibdocFig  = BibDoc(rel.bibdoc1_id)
                figure.set_recid(bibdocFig.bibrec_links[0]["recid"])
                fig = {"figure%d" % count : figure.get_dict()}
                json_response.update(fig)
                count+=1
            return json.dumps(json_response)
    
    def _get_bibdoc(self):
        bRD = BibRecDocs(self.recid)
        doc = None
        found = False
        for bdoc in bRD.list_bibdocs():
            if (found):
                break
            
            for bfile in bdoc.list_latest_files():
                if(bfile.get_format() == ".pdf"):
                    doc = bdoc
                    found = True
        return doc
    
    """
    expects json with page and boundary polygon
    """
    def _extract_caption(self, req, form):
        argd = wash_urlargd(form, {
                                   self._JSON_DATA_KEY: (str, ""),
                                   })
        json_response = {}
        if not argd.has_key(self._JSON_DATA_KEY):
            json_response.update({"error": "nojson"})
            return json.dumps(json_response)
          
        # load json data
        json_data_string = argd[self._JSON_DATA_KEY]
        if(json_data_string == ""):
            json_response.update({"error": "nojson"})
            return json.dumps(json_response)
        json_data_unicode = json.loads(json_data_string)
        json_data = json_unicode_to_utf8(json_data_unicode)
        points = [] # extract polygon in order of drawing
        
        page_num = int(json_data['page'])
        
        # extract the points of the caption polygon
        for i in range(0, 4):
            x, y = json_data['p'+str(i)].split(',')
            points.append((float(x), float(y)))
        
        doc = self._get_bibdoc()
        
        boxes = doc.more_info.get_data("", "annotated_text")
        captiontext = ""
        if (boxes is not None):
            cb = ce.CaptionExtractor(boxes[page_num]['boxes'], config.PAGE_WIDTH, boxes[page_num]["resolution"]["width"])
            cb.remove_non_intersecting_boxes(points)
            cb.merge_near_boxes()
            captiontext =  cb.get_caption_text()
        
        json_response = {}
        json_response.update({'caption': captiontext})
        return json.dumps(json_response)
    
    def _meta_info_save(self, req, form):
        # save information of page
        argd = wash_urlargd(form, {
                                   self._JSON_DATA_KEY: (str, ""),
                                   })
        json_response = {}
        if not argd.has_key(self._JSON_DATA_KEY):
            json_response.update({"error": "nojson"})
            return json.dumps(json_response)
            
            
        # load json data
        json_data_string = argd[self._JSON_DATA_KEY]
        json_data_unicode = json.loads(json_data_string)
        json_data = json_unicode_to_utf8(json_data_unicode)
        if(json_data.has_key("approvalid")):
            pass
            # todo remove approval request and update data
        else:
            res = run_sql("INSERT bibfigure_approvalrequests (recid, jsondata) VALUE(%s, %s)", (self.recid, json.dumps(json_data)))
        return json.dumps(json_data)
    
    def _lookup(self, component, path):
        """
        show json meta data: 
        /record/$recid/pageimages/meta-info
        
        render image of page based on this url scheme: 
        /record/$recid/pageimages/$pagenum[/$width]
        """
        
        if(component == "meta-info"):
            return self._meta_info, []
        elif(component == "debug"):
            return self.match_figures, []
        elif(component == "meta-info-save"):
            return self._meta_info_save, []
        elif(component == "extract-caption"):
            return self._extract_caption, []
        elif(component == "approve"):
            return self.approve_list, []
        else:
            self.page_num = int(component)
            if(len(path) > 0):
                if(int(path[0]) > 0):
                    self.img_width = int(path[0])
            self.debug = component
            return self._create_image, []
    
    def approve_list(self, req, form):       
        argd = wash_urlargd(form, { \
            'ln': (str, CFG_SITE_LANG), \
            'rev1' : (str, ''), \
            'rev2' : (str, ''), \
            'recid': (int, self.recid)})

        ln = argd['ln']
        _ = gettext_set_language(ln)
        uid = getUid(req)
        #_ = gettext_set_language(ln)
        body = "<table>"
        res = run_sql("SELECT approvalid, recid, jsondata FROM  bibfigure_approvalrequests")
        for row in res:
            approvalid, recid, jsondata = row
            
            body += '<tr><td><a href="/record/%d/pageimages/?approve=%d">Check and approve change request for record id %d</a></td></tr>' % (self.recid, approvalid, recid)
            

        body+="</table>"

        
        return page(title=_("Approval List"),
                body = body,
                #errors = ["test"],
                #warnings = warnings,
                #uid = uid,
                language=ln,
                #navtrail    = navtrail,
                #lastupdated = __lastupdated__,
                req=req)
    
    
    def match_figures(self, req, form):
        approvalid = 16
        doc = self._get_bibdoc()
        doc_id = doc.id
        doc_version = doc.get_latest_version()
        
        links = doc.get_incoming_relations('is_extracted_from')
        db_figures = []
        new_figures = []
        # get all the current figures
        for rel in links:
            bibdocFig  = BibDoc(rel.bibdoc1_id)
            figureRecid = bibdocFig.bibrec_links[0]["recid"]

            sb = simi.Figure.from_moreinfo(rel.more_info)
            sb.set_recid(figureRecid)
            
            db_figures.append(sb)
            
        # get the updated figures from the approval page
        # TODO: instead of loading it from the database, it should be loaded from the website again (like save button),
        # as the approver might change some. 
        res = run_sql("SELECT approvalid, recid, jsondata FROM  bibfigure_approvalrequests WHERE approvalid = %s", (str(approvalid), ))
        approvalid, recid, jsondata_string = res[0]
        json_data_unicode = json.loads(jsondata_string)
        json_data = json_unicode_to_utf8(json_data_unicode)
        count = 1
        while(json_data.has_key("figure%d" % count)):
            fig = json_data["figure%d" % count]
            sb = simi.Figure.from_dict(fig)
            new_figures.append(sb)
            count += 1
        
        bs = simi.FigureSimilarity(db_figures, new_figures)
        (new_list, update_list, delete_list, debug_list) = bs.match()
        fe = simi.FigureExtractor(self._get_main_pdf_data())
        
        xml_newl = []

        xml_newl.append('<collection xmlns="http://www.loc.gov/MARC21/slim">')
        # new files
        for i in range(0, len(new_list)):
            
            # extract image from best match (which might have been updated only slightly)
            tmpf_png = tempfile.NamedTemporaryFile(mode='w+b', suffix='.png', prefix='bibfigure_',
                               dir=CFG_TMPDIR, delete=False)
            png_data = fe.extract_figure_png(new_list[i])
            tmpf_png.write(png_data)
            tmpf_png.close()
            png_path = tmpf_png.name
            
            xml_newl.append(new_list[i].generate_MARCxml_new(doc_id, doc_version, png_path))
        xml_newl.append('</collection>')
        
        xml_new = "".join(xml_newl)
        tmpf_xml = tempfile.NamedTemporaryFile(mode='w', suffix='.xml', prefix='bibfigure_',
                               dir=CFG_TMPDIR, delete=False)
        tmpf_xml.write(xml_new)
        tmpf_xml.close()
        
        # updated files
        xml_updatel = []
        xml_updatel.append('<collection xmlns="http://www.loc.gov/MARC21/slim">')
        for i in range(0, len(update_list)):
            
            # extract image from best match (which might have been updated only slightly)
            tmpf_png = tempfile.NamedTemporaryFile(mode='w+b', suffix='.png', prefix='bibfigure_',
                               dir=CFG_TMPDIR, delete=False)
            png_data = fe.extract_figure_png(update_list[i].get_best_match())
            tmpf_png.write(png_data)
            tmpf_png.close()
            png_path = tmpf_png.name
            
            xml_updatel.append(update_list[i].generate_MARCxml_update(doc_id, doc_version, png_path))
        
        for i in range(0, len(delete_list)):
            xml_updatel.append(update_list[i].generate_MARCxml_delete())
        
        tmpf_xml = tempfile.NamedTemporaryFile(mode='w', suffix='.xml', prefix='bibfigure_',
                           dir=CFG_TMPDIR, delete=False)
        xml_updatel.append('</collection>')
        xml_update = "".join(xml_updatel)
        tmpf_xml.write(xml_update)
        tmpf_xml.close()
        
            
        return "%s \n\n%s \n\n%s \n\n" % (new_list, update_list, delete_list)
    
    def __call__(self, req, form):
        """Redirect calls without final slash."""
        return "session: %s" % form
        '''
        if self.recid:
            redirect_to_url(req, '%s/%s/%s/edit/' % (CFG_SITE_SECURE_URL,
                                                         CFG_SITE_RECORD,
                                                         self.recid))
        else:
            redirect_to_url(req, '%s/%s/edit/' % (CFG_SITE_SECURE_URL, CFG_SITE_RECORD))
        '''
