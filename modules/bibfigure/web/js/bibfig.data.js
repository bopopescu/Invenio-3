/** The model of the data used by the plots selector
 */


/**
 * A class representing Images
 * @property url main url to image
 * @property width width of the image
 * @property height height of the image
 */
function Image(url, width, height){
    this.url = url;
    this.width = width;
    this.height = height;
}

/**
 * returns the url with the original width
 */
Image.prototype.getUrl = function(){
    return this.url + "/" + this.width;
}

/***
 * returns an url to a higher definition image (twice the size)
 */
Image.prototype.getUrlHD = function(){
    return this.url + "/" + (2.*this.width);
}

/**
   angle -> angle under which the rectangle is paralel to the x,y axis with x,y equal to given parameters
 */

function Rectangle(x, y, width, height, angle){
    this.x = x || 0.;
    this.y = y || 0.;
    this.width = width || 0.;
    this.height = height || 0.;
    this.angle = angle || 0.;
}

Rectangle.prototype.toString = function(){
    return "(x = " + this.x + ", y = " + this.y + ", width = "
    + this.width + ", height = " + this.height + ", angle = "+this.angle+" &deg;)";
};

/** Get a scale allowing to fit the rectangle into a given box.
 * The scale is equal to the ratio: new width/ new height
 */
Rectangle.prototype.getFittingScale = function(view){
    var ratio = this.width / this.height;
    var limitRatio = view.width / view.height;
    return ratio > limitRatio ?
    view.width / this.width
    : view.height / this.height;
};

Rectangle.prototype.copy = function(){
    return new Rectangle(this.x, this.y, this.width, this.height, this.angle);
    
}


/***
 * Prototype for boundary of caption or figure
 * @property page page number the figure is on (starting from 0)
 * @property rectangle rectangle of the figure/caption on the page  
 */
function Boundary(){
    this.id = "Boundary" + getNextIdentifier();
    this.page = null;
    this.rectangle = new Rectangle()
}

Boundary.prototype.setPage = function(page){
    this.page = page;
}

Boundary.prototype.getPage = function(){
    return this.page;
}

Boundary.prototype.setRectangle = function(rectangle){
    this.rectangle = rectangle;
}

Boundary.prototype.getRectangleString = function(){
    return ""+this.rectangle.x+", "+this.rectangle.y+", "+this.rectangle.width+", "+this.rectangle.height+", "+this.rectangle.angle;
}


function Figure(pdfDocument, page){
    this.pdfDocument = pdfDocument
    this.id = "Figure" + getNextIdentifier(); // for debugging reasons

    this.figureBoundary = new Boundary()
    this.captionBoundary = new Boundary();
    this.figureBoundary.setPage(page);
    this.captionBoundary.setPage(page);
    this.caption  = "";
}

Figure.prototype.getFigurePageResolution = function(){
    return {
        "x": this.figureBoundary.getPage().image.width, 
        "y": this.figureBoundary.getPage().image.height
    } 
    
}

Figure.prototype.getCaptionPageResolution = function(){
    return {
        "x": this.captionBoundary.getPage().image.width, 
        "y": this.captionBoundary.getPage().image.height
    } 
    
}

Figure.prototype.getCaptionPageResolutionString = function(){
    res = this.getCaptionPageResolution();
    return ""+res["x"]+", "+res["y"];
}

Figure.prototype.getFigurePageResolutionString = function(){
    res = this.getFigurePageResolution();
    return ""+res["x"]+", "+res["y"];
}

/***
 * Returns the figure boundary object with page and rectangle
 * @return figure boundary
 */
Figure.prototype.getFigureBoundary = function(){
    return this.figureBoundary;
}

Figure.prototype.setFigureBoundary = function(figBoundary){
    this.figureBoundary = figBoundary;
}

/***
 * Returns the caption boundary object with page and rectangle
 * @return caption boundary
 */
Figure.prototype.getCaptionBoundary = function(){
    return this.captionBoundary;
}

Figure.prototype.setCaptionBoundary = function(captBoundary){
    this.captionBoundary = captBoundary;
}

Figure.prototype.setCaption = function(caption){
    this.caption = caption;
}

Figure.prototype.getCaption = function(){
    return this.caption;
}

Figure.prototype.remove = function(){
    this.pdfDocument.removeFigure(this);
};

/***
 * Representation of a single page in the document
 */
function Page(pdfDocument){
    this.id = "Page" + getNextIdentifier();
    this.number = 0;
    this.image =  new Image("", 0, 0);

    this.minImage = new Image("", 0, 0);
    this.pdfDocument = pdfDocument;
}

/***
 * sets the number of the page
 */
Page.prototype.setNumber = function(num){
    this.number = num;
}

Page.prototype.getNumber = function(){
    return this.number;
}

/***
 * Object that represents the rendered PDF 
 * @property pages Collection of pages of the current document
 * @property figures Collection of figures in the current document
 */
function PdfDocument(){
    this.id = "PdfDocument" + getNextIdentifier();
    this.pages = []; // a collection of all pages belonging to the document
    this.figures = [];
}

/***
 * Creates a new page at the end of the document and returns it
 * also counts page counter one higher and sets page number to page
 * @return new Page object
 */
PdfDocument.prototype.createNewPage = function(){
    var newPage = new Page(this);
    newPage.setNumber(this.pages.length)
    this.pages.push(newPage);
    return newPage;
};

/***
 * Adds a new figure to the figure collection
 * @return new figure
 */
PdfDocument.prototype.createFigure = function(page){
    var newFigure = new Figure(this, page);
    this.figures.push(newFigure);
    return newFigure;
};

/***
 * Deletes a figure from the figure collection
 * @return true if figure was deleted, false if figure was not found
 */
PdfDocument.prototype.removeFigure = function(figure){
    for (var figureInd in this.figures){
        if (this.figures[figureInd] == figure){
            this.figures.splice(figureInd, 1);
            return true;
        }
    }
    return false;
};

/***
 * Returns the pages collection
 * @return collection of pages
 */
PdfDocument.prototype.getPages = function(){
    return this.pages;
};

/***
 * Returns a specific page
 * @param pageNum number of the page to retrieve
 * @return page with index pageNum
 */
PdfDocument.prototype.getPage = function(pageNum){
    return this.pages[pageNum];
};


PdfDocument.prototype.getFigures = function(){
    return this.figures;
}

/***
 * returns an array of figures in the current document in json format
 */
PdfDocument.prototype.getFiguresJSON = function(){
    var jfigs = {}
    var num = 1;
    var figures = this.getFigures();
    for(j = 0; j < figures.length; j++){
        var fig = figures[j];
        var jfig = {}
        
        figBoundary = fig.getFigureBoundary()
        captBoundary = fig.getCaptionBoundary()
        jfig["location"] = {}
        
        jfig["location"]["boundary"] = {
            "x": figBoundary.rectangle.x,
            "y": figBoundary.rectangle.y,
            "width": figBoundary.rectangle.width,
            "height": figBoundary.rectangle.height,
            "alpha": figBoundary.rectangle.angle
            };
        jfig["location"]["page_num"] = figBoundary.getPage().getNumber();
        jfig["location"]["page_resolution"] = {"width": figBoundary.getPage().image.width, "height": figBoundary.getPage().image.height}
        
            
        jfig["caption_location"] = {}
        jfig["caption_location"]["boundary"] = {
            "x": captBoundary.rectangle.x,
            "y": captBoundary.rectangle.y,
            "width": captBoundary.rectangle.width,
            "height": captBoundary.rectangle.height,
            "alpha": captBoundary.rectangle.angle
            };
        jfig["caption_location"]["page_num"] = captBoundary.getPage().getNumber();
        jfig["caption_location"]["page_resolution"] = {"width": captBoundary.getPage().image.width, "height": captBoundary.getPage().image.height}
        jfigs["figure"+num] = jfig;
        num++;
    }
    return jfigs;
};