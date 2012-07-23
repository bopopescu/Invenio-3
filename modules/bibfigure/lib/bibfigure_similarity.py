'''
Created on Sep 13, 2012

@author: pete
'''
import math
import bibfigure_config as config
import poppler
import Image
import cStringIO
import gtk
import base64
import cPickle
import random
"""
representation of a figure. 
"""
class Figure(object):
    def __init__(self):
        
        self.figure = {'caption': '',
                       'caption_location': {'boundary': {'height': 0,
                                                        'width': 0,
                                                           'x': 0,
                                                           'y': 0},
                                              'page_num': 1,
                                              'page_resolution': {'height': 1584,
                                                                  'width': 1224},
                                              'page_scale': 2},
                         'location': {'boundary': {'height': 0,
                                                   'width': 0,
                                                   'x': 0,
                                                   'y': 0},
                                      'page_num': 0,
                                      'page_resolution': {'height': 1, 'width': 1},
                                      'page_scale': 1},
                         'text_references': ''}
        self.recid = None
        self.matches = []

    """
    creates a rectangular bounding box around the given points
    aligned with the coordinate system
    @param points: list of points [(x, y), ...]
    @return: box (x, y, w, h)
    """
    def _boundingbox(self, points):
        smallest_x = points[0][0]
        smallest_y = points[0][1]
        biggest_x = points[0][0]
        biggest_y = points[0][1]
        for i in range(1, len(points)):
            x = points[i][0]
            y = points[i][1]
            if(x < smallest_x):
                smallest_x = x
            if(x > biggest_x):
                biggest_x = x
            if(y < smallest_y):
                smallest_y = y
            if(y > biggest_y):
                biggest_y = y
            
        x = smallest_x
        y = smallest_y
        w = biggest_x - smallest_x
        h = biggest_y - smallest_y
        
        box = (x, y, w, h)
        return box
    
    def get_caption(self):
        return self.figure["caption"]
    
    """
    returns the figure rectangle
    @return: box in the form (x, y, w, h, alpha)
    """
    def get_figure_box(self):
        box = self.figure["location"]["boundary"]
        alpha = box.get("alpha", 0.)
        return (box["x"], box["y"], box["width"], box["height"], alpha)
    
    """
    @param boxtuple: (x, y, w, h, alpha)
    """
    def set_figure_box(self, boxtuple):
        (x, y, w, h, alpha) = boxtuple
        box = self.figure["location"]["boundary"]
        box["x"] = x
        box["y"] = y
        box["width"] = w
        box["height"] = h
        box["alpha"] = alpha
    
    """
    calculates the corner points of the figure rectangle
    @return: list of corner points [(x, y), ...]
    """
    def get_figure_points(self):
        return self._boxpoints(self.get_figure_box(), self.get_figure_resolution())
    
    """
    returns a bounding box around the figure rectangle aligned with the main coordinate
    axes
    @return: (x, y, w, h)
    """
    def get_figure_boundingbox(self):
        return self._boundingbox(self.get_figure_points())
    
    """
    normalizes the corner points of the figure rectangle with
    the longest side of the page the figure is on
    """
    def get_figure_points_normalized(self):
        points =  self.get_figure_points()
        return self._normalize_points(points, self.get_figure_resolution())
        
    
    """
    @return: (width, height) of the page
    """
    def get_figure_resolution(self):
        res = self.figure["location"]["page_resolution"]
        return (res["width"], res["height"])
    
    """
    sets the record if of the figure in the invenio database
    """
    def set_recid(self, recid):
        self.recid = recid
    
    def get_figure_page(self):
        return self.figure["location"]["page_num"]
    
    
    """
    adds another figure as a matched figure if, e.g. the score between the two
    is low enough
    @param figure: Figure object that is close to self
    """
    def add_match(self, figure):
        self.matches.append(figure)
        
    def get_matches(self):
        return self.matches
    
    """
    calculates the scores of all available matches and returns 
    the best matching figure
    """
    def get_best_match(self):
        if(len(self.matches) == 0):
            return None
        elif(len(self.matches) == 1):
            return self.matches[0]
        min_score = float("Inf")
        min_match = None
        for m in self.matches:
            score = self.score(m)
            if(score < min_score):
                min_match = m
                min_score = score
        return min_match
            
        
    """
    ported from Piotr's javascript code, used for transforming
    rectangle corners into actual figure_points in figure_page coordinate system
    """
    def _getTransformedMargin(self, angle, scale, iwidth, iheight):
    
        calcAngle = math.pi * angle / 180.;
        width = round(scale * iwidth);
        height = round(scale * iheight);
    
        shx = 0;
        shy = 0;

        if (angle >= 0 and angle <= 90):
            shx = height * math.sin(calcAngle);
            shy = 0;
    
        if (angle >= 90  and angle <= 180):
            shx = math.sin(math.pi - calcAngle) * height  + width * math.cos(math.pi - calcAngle);
            shy = math.cos(math.pi - calcAngle) * height;
        
        if (angle >= -90 and angle <= 0):
            shx = 0;
            shy = - width * math.sin(calcAngle);
    
        if (angle >= -180 and angle <= -90):
            shx = math.cos(math.pi + calcAngle) * width;
            shy = math.sin(math.pi + calcAngle) * width + math.cos(math.pi + calcAngle) * height;
        return {"x": round(shx), \
                "y": round(shy)}
        
    """
    calculates the corner points in of a box in the given resolution
    @param box: (x, y, w, h, alpha)
    @param resolution: (width, height) of the page the box is on
    """
    def _boxpoints(self, box, resolution):
        (x, y, w, h, angle) = box
        return_points = []
        
        tm1 = self._getTransformedMargin(angle, 1., resolution[0], resolution[1]);
        tm2 = self._getTransformedMargin(0., 1., resolution[0], resolution[1]);
        points = [];
        # figure_points in draw direction
        points.append({"x": x, 
                       "y": y});
        
        points.append({"x": x+w, 
                       "y": y})
        
        points.append({"x": x + w, 
                       "y": y + h})
        
        points.append({"x": x, 
                       "y": y + h})
        
        for i in range(0, len(points)):
            p = points[i]
            p = self._translation(p, tm2["x"], tm2["y"]);
            p = self._rotation(p, -angle);
        
            s = {"x": -tm1["x"], 
                 "y": -tm1["y"]}

            s = self._rotation(s, -angle)
            p = self._translation(p, s["x"], s["y"])
            return_points.append((p["x"], p["y"]))
        return return_points
    
    """
    normalizes the points by the largest value of resolution
    """
    def _normalize_points(self, points, resolution):
        longest_side = resolution[0] if (resolution[0] > resolution[1]) else resolution[1]
        normalized = []
        for p in points:
            normalized.append((p[0]/float(longest_side), p[1]/float(longest_side)))
        return normalized
    
    def _translation(self, p, tx, ty):
        return {
            "x": p["x"] + tx, 
            "y": p["y"] + ty
        }

    def _rotation(self, p, angle):
        x = p["x"];
        y = p["y"];
        
        rangle = self._to_radians(angle)
        return {
            "x": math.cos(rangle) * x - math.sin(rangle) * y, 
            "y": math.sin(rangle) * x + math.cos(rangle) * y
        }
        
    def _to_radians(self, angle):
        return angle * (math.pi / 180.);
    
    """
    Defines a similarity measure based on norm2 between two polygons 
    with the same amount of figure_points. The minimum of the distance of the figure_points
    will be taken as the similarity measure
    @param a: list of figure_points (x, y) in order of drawing clockwise
    @param b: list of figure_points (x, y) in order of drawing clockwise
    """
    def norm2min(self, box_b):
        a = self.get_figure_points_normalized()
        b = box_b.get_figure_points_normalized()
        min_sum = float('inf')
        
        for j in range(0, len(a)):
            summed = 0.
            for i in range(0, len(a)):
                summed += self.norm2(a[i], b[(i+j) % len(b)-1])
            if(summed < min_sum):
                min_sum = summed
        return min_sum
    
    def norm2(self, a, b):
        return (a[0]-b[0])**2 + (a[1]-b[1])**2
    
    """
    compares a figure to another and returns a similarity score
    based on the euclidean distance between the corner figure_points
    @param box_b: second figure to compare to
    """
    def score(self, box_b):
        return self.norm2min(box_b)
    
    def get_dict(self):
        return self.figure
    
    @staticmethod
    def from_dict(fig):
        b = Figure()
        b.figure = fig
        return b
    
    @staticmethod
    def from_moreinfo(moreinfo):
        b = Figure()
        for entry in ["caption", "text_references"]:
            data = moreinfo.get_data('figures', entry)
            if(data is not None):
                b.figure[entry] = data
                
        for head in ["caption_location", "location"]: 
            data = moreinfo.get_data('figures', head)
            if(data is not None):
                for entry in ["boundary", "page_num", "page_resolution", "page_scale"]:
                    if(data.has_key(entry)):
                        b.figure[head][entry] = data[entry]
        return b
    
    
    """
    generates XML code to update a given figure. 
    be careful, for rendering you have to use figure.get_best_match() as this
    is the best matching updated figure. Otherwise you just store the same information 
    again. 
    @param doc_recid: Record of the document the figure belongs to
    @param doc_version: Version of the document
    @param png_path: Path to temporary rendered figure in png to upload with bibupload
    @return: MARCxml update code
    """
    def generate_MARCxml_update(self, doc_id, doc_version, png_path):
        update_dict = self.get_best_match().figure
        more_info64 = base64.encodestring(cPickle.dumps(update_dict))
        unique = random.randint(0,999999)
            
        xml = """<record>
        <controlfield tag="001">"""+str(self.recid)+"""</controlfield>
        
        <datafield tag="FFT" ind1=" " ind2=" ">
          <subfield code="a">"""+str(png_path)+"""</subfield>
          <subfield code="n">NAME OF THE PLOT ... IF WE HAVE IT (WE CAN LOOK AT THE BEGINNING OF THE CAPTION OR ASK USER)</subfield>
          <subfield code="i">"""+str(doc_id)+"""</subfield>
          <subfield code="v">TMP:"""+str(unique)+"""</subfield>
        </datafield>
    
        
         <datafield tag="BRT" ind1=" " ind2=" ">
                <subfield code="i">"""+str(doc_id)+"""</subfield>
        <subfield code="v">TMP:"""+str(unique)+"""</subfield>
        <subfield code="j">"""+str(doc_id)+"""</subfield>
                <subfield code="w">"""+str(doc_version)+"""</subfield>
                <subfield code="t">is_extracted_from</subfield>
                <subfield code="m">"""+str(more_info64)+"""</subfield>
        </datafield>
        </record>"""
        return xml
    
    def get_MARC_delete(self):
        xml = """<record>
                 <controlfield tag="001">"""+str(self.recid)+"""</controlfield>
                
                <datafield tag="980" ind1=" " ind2=" ">
                <subfield code="a">DELETED</subfield>
                </datafield>
                </record>"""
    
    """
    generates XML code to insert a new figure. 
    @param doc_recid: Record of the document the figure belongs to
    @param doc_version: Version of the document
    @param png_path: Path to temporary rendered figure in png to upload with bibupload
    """
    def generate_MARCxml_new(self, doc_recid, doc_version, png_path):
        more_info64 = base64.encodestring(cPickle.dumps(self.figure))
        unique1 = random.randint(0,999999)
        unique2 = random.randint(0,999999)
        while(unique1 == unique2):
            unique2 = random.randint(0,999999)
            
        xml = """<record>
        <datafield tag="FFT" ind1=" " ind2=" ">
          <subfield code="a">"""+str(png_path)+"""</subfield>
          <subfield code="n">NAME OF THE PLOT ... IF WE HAVE IT (WE CAN LOOK AT THE BEGINNING OF THE CAPTION OR ASK USER)</subfield>
          <subfield code="i">TMP:"""+str(unique1)+"""</subfield>
          <subfield code="v">TMP:"""+str(unique2)+"""</subfield>
        </datafield>
    
        
         <datafield tag="BRT" ind1=" " ind2=" ">
                <subfield code="i">TMP:"""+str(unique1)+"""</subfield>
        <subfield code="v">TMP:"""+str(unique2)+"""</subfield>
        <subfield code="j">"""+str(doc_recid)+"""</subfield>
                <subfield code="w">"""+str(doc_version)+"""</subfield>
                <subfield code="t">is_extracted_from</subfield>
                <subfield code="m">"""+str(more_info64)+"""</subfield>
        </datafield>
        </record>"""
        return xml
    
"""
provides information about changes in figures compared to the database
"""
class FigureSimilarity(object):
    """
    Provides similarity measurements to find changed figures and connect them to already existing boxes
    @param db_figures: original figure data loaded from invenio db
    @param new_figures: updated figures that have to be connected to the old ones
    """
    def __init__(self, db_figures, new_figures):
        self.db_figures = db_figures
        self.new_figures = new_figures
    """
    calculates the matches of db figures with the updated new_figures
    and puts them into a tuple of lists (new, update, delete)
    @return: (new_list, update_list, delete_list)
    """
    def match(self):
        # match figures with new figures
        for db_figure in self.db_figures:
            min_score = config.MATCH_MAX_SCORE
            min_figure = None
            for new_figure in self.new_figures:
                if(db_figure.get_figure_page() == new_figure.get_figure_page()):
                    score = db_figure.score(new_figure)
                    if (score < config.MATCH_MAX_SCORE and score < min_score):
                        min_figure = new_figure
                        min_score = score
                            
            # create association
            
            if(min_figure is not None):
                db_figure.add_match(min_figure)
                min_figure.add_match(db_figure)
                
                
        delete_list = []
        update_list = []
        new_list = []
        debug_list = []
        
        for db_figure in self.db_figures:
            if(len(db_figure.get_matches()) == 0):
                delete_list.append(db_figure)
            else:
                debug_list.append(db_figure.score(db_figure.get_best_match()))
                update_list.append(db_figure)
        
        for new_figure in self.new_figures:
            if(len(new_figure.get_matches()) == 0):
                new_list.append(new_figure)
        return (new_list, update_list, delete_list, debug_list)



"""
Class to extract figures from pdf documents as PNG files
"""
class FigureExtractor(object):
    def __init__(self, pdfdata):
        self.pdfdata = pdfdata
        self.doc = poppler.document_new_from_data(pdfdata, password = '')
        self.large_scale = 3.
        
        self.filter = Image.BILINEAR
    
    """
    extracts a given figure from the pdf document as png
    maximum height and width are configureable in the bibfigure_config.py
    @param figure: Figure object to extract
    @return: PNG binary data string, can be written to file
    """
    def extract_figure_png(self, figure):
        p = self.doc.get_page(figure.get_figure_page())
        pwidth, pheight = p.get_size()
        pwidth = int(pwidth)
        pheight = int(pheight)
        
        (x, y, w, h) = figure.get_figure_boundingbox()
        
        # fig -> popler
        scale_figure_to_poppler = pwidth / float(figure.get_figure_resolution()[0])
        scale_poppler_to_figure =  float(figure.get_figure_resolution()[0]) / pwidth
        
        
        pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, int(w*scale_figure_to_poppler* self.large_scale), int(h*scale_figure_to_poppler* self.large_scale))
        
        #p.render_to_pixbuf_for_printing(int(scale*x),int(scale*y),int(scale*w), int(scale*h), self.target_width / float(pwidth),0, pixbuf)
        p.render_to_pixbuf(int(scale_figure_to_poppler*x* self.large_scale),int(scale_figure_to_poppler*y* self.large_scale),int(scale_figure_to_poppler* w * self.large_scale), int(scale_figure_to_poppler*h * self.large_scale), self.large_scale,0, pixbuf)
        
        # There has to be a better way to get the image?
        lst=[]
        pixbuf.save_to_callback(lambda b,l: l.append(b), 'png', user_data=lst)
        #png = ''.join(lst)
        
        b = cStringIO.StringIO()
        for chunk in lst:
            b.write(chunk)
        b.seek(0)
        im = Image.open(b)
        (fx, fy, fw, fh, falpha) = figure.get_figure_box()
        im = im.rotate(-falpha, self.filter )
        
        iw, ih = im.size

        crop_vert = (iw - fw * scale_figure_to_poppler * self.large_scale ) / 2.
        crop_hor = (ih - fh * scale_figure_to_poppler * self.large_scale ) / 2.
        
        """
        TODO: fix the black bar
        if(int(crop_vert) < crop_vert):
            crop_vert += 1.
        if(int(crop_hor) < crop_hor):
            crop_hor += 1.
        """
        
        im = im.crop((int(crop_vert), int(crop_hor), int(iw - crop_vert), int(ih - crop_hor)))
        
        iw, ih = im.size
        
        new_scale = config.EXTRACT_FIGURE_MAX_X / iw if(config.EXTRACT_FIGURE_MAX_X / iw < config.EXTRACT_FIGURE_MAX_Y / ih) else config.EXTRACT_FIGURE_MAX_Y / ih
        im = im.resize((int(iw * new_scale), int(ih * new_scale)), self.filter)
        output = cStringIO.StringIO()
        im.save(output, "PNG")
        contents = output.getvalue()
        output.close()
        return contents
