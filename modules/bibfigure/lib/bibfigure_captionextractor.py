'''
Created on Aug 21, 2012

@author: pete
'''
import Image, ImageDraw
import cStringIO

"""
box = (x, y, w, h)
"""
class CaptionExtractor(object):
    
    def __init__(self, boxes, rendered_width, extracted_width):
        self.boxes = boxes
        self.rendered_width = rendered_width;
        self.extracted_width = extracted_width;

    """
    checks if box2 is right of box1 and very close to it.
    @param box1: (x,y,w,h) of box1
    @param box2: (x,y,w,h) of box2
    @return: -1 if they are not next to each other, otherwise 
    distance in x direction 
    """
    def is_near(self, box1, box2):
        if(box1 == box2):
            return -1
        
        (x1, y1, w1, h1) = box1
        (x2, y2, w2, h2) = box2

        if(abs(x2 - (x1 + w1)) < 30 and \
           #x2 - (x1 + w1) >= 0 and \
           abs(y2 - y1) < 20):
            return abs(x2 - (x1 + w1))
        return -1
    
    """
    returns a list of boxes that are right of the box and very close
    @param box: (x, y, w, h) of the box
    @return: list of boxes that are right of the box and very close
    """
    def find_near(self, box):
        boxes = []
        for box2 in self.boxes:
            d = self.is_near(box, box2)
            if(d > -1):
                boxes.append(box2)
        # sort 
        sort = False  # We haven't started sorting yet

        while not sort:
            sort = True  # Assume the list is now sorted
            for element in range(0, len(boxes)-1):
                if boxes[element][0] > boxes[element + 1][0]:
                    sort = False  # We found two elements in the wrong order
                    hold = boxes[element + 1]
                    boxes[element + 1] = boxes[element]
                    boxes[element] = hold
        return boxes
    
    """
    processes all boxes until no box can be merged anymore
    """
    def merge_near_boxes(self):
        self.boxes2png("merge-0")
        processed = False
        
        while(not processed):
            processed = True
            for box in self.boxes:
                if(self.process_entry(box)):
                    processed = False
                    break;
        self.boxes2png("merge-1")
    
    """
    returns the caption text of all boxes that are still
    in the list ordered by their specific y coordinate (starting
    with lowest).
    @return: concatenated text of all boxes ordered by y-coordinate
    """
    def get_caption_text(self):
        # sort by y coordinate 
        # TODO: faster sorting algorithm
        sort = False  # We haven't started sorting yet
        
        boxes = self.boxes.keys()
        while not sort:
            sort = True  # Assume the list is now sorted
            for element in range(0, len(boxes)-1):
                if boxes[element][1] > boxes[element + 1][1]:
                    sort = False  # We found two elements in the wrong order
                    hold = boxes[element + 1]
                    boxes[element + 1] = boxes[element]
                    boxes[element] = hold
        text_builder = cStringIO.StringIO()
        
        for box in boxes: 
            text_builder.write(self.boxes[box])
        text = text_builder.getvalue()
        text_builder.close()
        return text
    
    """
    processes one box and merges it with other aligned boxes
    @param orig: (x, y, w, h) of the box to check
    """
    def process_entry(self, orig):
        target_box = {orig:self.boxes[orig]}
        
        connecting_boxes = self.find_near(orig)
        if ( len(connecting_boxes) == 0): 
            return False
        while(len(connecting_boxes) > 0):
            cbox = connecting_boxes.pop(0)
            target_box = self.merge(target_box, {cbox:self.boxes[cbox]})
            del self.boxes[cbox]
        del self.boxes[orig]
        self.boxes.update(target_box)
        return True
    
    """
    merge two boxes two a new box
    @param box1dict: {(x, y, w, h): text} of the box
    @param box2dict: {(x, y, w, h): text} of the box
    @return: {(x, y, w, h): text1+text2} of two boxes with the smallest 
    rectangle capturing both original rectangles 
    """
    def merge(self, box1dict, box2dict):
        
        box1 = box1dict.keys()[0]
        text1 = box1dict[box1]
        
        box2 = box2dict.keys()[0]
        text2 = box2dict[box2]
        # swap if box1 is not left of box2
        if(box1[0] > box2[0]):
            box1, box2 = box2, box1
            text1, text2 = text2, text1
        
        x1, y1, w1, h1 = box1
        x2, y2, w2, h2 = box2
        # merge the text
        text = text1 + text2
        # calculate the new bounding box
        # smallest x value
        x = x1
        w = w1 if (x1+w1 > x2 + w2 ) else (x2 + w2 - x1)
        
        y = y1 if (y1 < y2) else y2
        h = y1+h1 - y if (y1+h1 > y2+h2) else y2+h2 - y
        
        return {(x,y,w,h) : text}
    
    """
    calculates if two polygons intersect. Points have to be in  
    draw order 
    based on the algorithm: 
    http://mathforum.org/library/drmath/view/54386.html
    @param points1: list of points (x, y) in order the first polygon is drawn
    @param points2: list of points (x, y) in order the second polygon is drawn
    @return: True if at least one point of points1 lies in the area of the points2 polygon
    else False
    """
    def intersect(self, points1, points2):
        #(x1, y1, w1, h1) = box
        for p in points1:
            #print "p1", p
            (x2, y2) = p
            lastf = 0
            intersects = True
            for i in range(0, len(points2)):
                #print points2[i % len(points2)-1], points2[(i+1) % len(points2)-1]
                (x0, y0) = points2[i % len(points2)-1]
                (x1, y1) = points2[(i+1) % len(points2)-1]
                
                f = (.5)*(x1*y2 - y1*x2 -x0*y2 + y0*x2 + x0*y1 - y0*x1)
                if((lastf < 0 and f > 0) or \
                   (lastf > 0 and f < 0)):
                    intersects = False
                    break
                
                if(f != 0):
                    lastf = f
            if(intersects):
                return True
        return False
    
    """
    For debugging purposes, visualizes the current boxes with their text values
    and highlights boxes given in the highlight parameter
    @param picnum: output name [picnum].png
    @param highlight: list of (x, y, w, h) of boxes to highlight 
    """
    def boxes2png(self, picname, highlight = None):
        im = Image.new("RGB", (1200, 1700), "white")
        draw = ImageDraw.Draw(im)
        if(highlight is not None):
            for box in highlight:
                x, y, w, h = box
                draw.rectangle([(x, y), (x+w, y+h)], fill = "yellow")
        for box in self.boxes:
            x, y, w, h = box
            text = self.boxes[box]
            draw.rectangle([(x, y), (x+w, y+h)], outline = "red")
            draw.text((x, y), text, fill = "black")
        
        del draw 
        #im.save("/home/pete/src/invenio/modules/bibfigure/testimg/%s.png" % picname, "PNG")
    
    """
    removes boxes that have no corner points in the given
    area. 
    @param area: polygon as a list of points in draw order [(x_1, y_1), (x_2, y_2)...]
    """
    def remove_non_intersecting_boxes(self, area):
        self.boxes2png("remove-0")
        scaledArea = []
        scale = float(self.extracted_width) / float(self.rendered_width)
        for p in area:
            (x, y) = p
            scaledArea.append((x * scale, y * scale))
        
        deleteList = []
        for box in self.boxes:
            (x, y, w, h) = box
            vertices = [(x, y), (x+w, y), (x+w, y+h), (x, y+h)]
            if(not self.intersect(vertices, scaledArea) and \
               not self.intersect(scaledArea, vertices)):
                deleteList.append(box)
        
        for delbox in deleteList:
            del self.boxes[delbox]
        self.boxes2png("remove-1")
